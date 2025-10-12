import asyncio
import sys
from web3 import Web3
from web3.middleware import geth_poa_middleware
from loguru import logger
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from typing import Set

from config import get_settings
from database import SessionLocal, Base, engine
from models import Token
from token_detector import TokenDetector

# Configure structured logger
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> - <level>{message}</level>",
    level="INFO"
)

settings = get_settings()

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)


class BlockchainMonitor:
    def __init__(self, rpc_url: str, ws_url: str, network: str):
        self.network = network
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        
        # Use the global logger
        self.logger = logger
        
        # Inject POA middleware for BSC and other POA chains
        if network == "BSC":
            self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
            self.logger.info(f"✅ POA middleware injected for {network}")
        
        self.detector = TokenDetector(self.w3, network, self.logger)
        self.pending_tokens: Set[str] = set()  # Track pending confirmations
        
        self.logger.info(f"🔗 Connected to {network}: {self.w3.is_connected()}")
    
    def save_token_to_db(self, token_data: dict, confirmed: bool = False):
        """Save token to database"""
        db = SessionLocal()
        try:
            # Check if token already exists
            existing = db.query(Token).filter(
                Token.address == token_data['address'].lower(),
                Token.network == self.network
            ).first()
            
            if existing:
                # Update confirmation status if needed
                if confirmed and not existing.confirmed:
                    existing.confirmed = True
                    db.commit()
                    self.logger.info(f"✅ Token {existing.symbol} confirmed")
                return
            
            # Create new token record
            token = Token(
                address=token_data['address'].lower(),
                block_number=token_data['block_number'],
                timestamp=datetime.utcnow(),
                network=self.network,
                name=token_data.get('name'),
                symbol=token_data.get('symbol'),
                decimals=token_data.get('decimals'),
                total_supply=token_data.get('total_supply'),
                creator_address=token_data.get('creator_address'),
                tx_hash=token_data.get('tx_hash'),
                confirmed=confirmed,
                is_verified=False,
                risk_score=self.calculate_risk_score(token_data)
            )
            
            db.add(token)
            db.commit()
            
            self.logger.success(
                f"💾 Saved token: {token.name or 'Unknown'} ({token.symbol or 'N/A'}) "
                f"at {token.address[:10]}... on {self.network}"
            )
        
        except IntegrityError:
            db.rollback()
            self.logger.warning(f"Token {token_data['address']} already exists in DB")
        
        except Exception as e:
            db.rollback()
            self.logger.error(f"Error saving token: {e}")
        
        finally:
            db.close()
    
    def calculate_risk_score(self, token_data: dict) -> int:
        """Calculate basic risk score for token"""
        score = 0
        
        # Low supply might be suspicious
        if token_data.get('total_supply'):
            supply = int(token_data['total_supply'])
            if supply < 1000:
                score += 3
        
        # Non-standard decimals
        if token_data.get('decimals') and token_data['decimals'] != 18:
            score += 1
        
        # Missing name or symbol
        if not token_data.get('name'):
            score += 2
        if not token_data.get('symbol'):
            score += 2
        
        return min(score, 10)  # Cap at 10
    
    async def process_block(self, block_number: int):
        """Process a single block for contract deployments"""
        try:
            block = self.w3.eth.get_block(block_number, full_transactions=True)
            
            if not block or not block.transactions:
                return
            
            self.logger.info(f"📦 Processing block {block_number} ({len(block.transactions)} txs) on {self.network}")
            
            for tx in block.transactions:
                # Check if it's a contract creation (to address is None)
                if tx['to'] is None:
                    tx_hash = tx['hash'].hex()
                    
                    # Get contract address from receipt
                    is_creation, contract_address = self.detector.is_contract_creation(tx_hash)
                    
                    if is_creation and contract_address:
                        self.logger.info(f"🆕 New contract deployed: {contract_address}")
                        
                        # Try to fetch token metadata
                        metadata = self.detector.fetch_token_metadata(contract_address)
                        
                        if metadata:
                            # Get transaction details
                            tx_details = self.detector.get_transaction_details(tx_hash)
                            
                            token_data = {
                                'address': contract_address,
                                'block_number': block_number,
                                'name': metadata.get('name'),
                                'symbol': metadata.get('symbol'),
                                'decimals': metadata.get('decimals'),
                                'total_supply': metadata.get('total_supply'),
                                'creator_address': tx_details.get('from') if tx_details else None,
                                'tx_hash': tx_hash
                            }
                            
                            # Check if we have enough confirmations
                            current_block = self.w3.eth.block_number
                            is_confirmed = self.detector.is_token_confirmed(
                                block_number, 
                                current_block, 
                                settings.confirmation_blocks
                            )
                            
                            # Save to database
                            self.save_token_to_db(token_data, confirmed=is_confirmed)
                            
                            # Track for later confirmation if not confirmed yet
                            if not is_confirmed:
                                self.pending_tokens.add(f"{contract_address}:{block_number}")
        
        except Exception as e:
            self.logger.error(f"Error processing block {block_number}: {e}")
    
    async def check_pending_confirmations(self):
        """Check pending tokens for confirmations"""
        if not self.pending_tokens:
            return
        
        current_block = self.w3.eth.block_number
        confirmed_tokens = set()
        
        for pending in list(self.pending_tokens):
            address, block_num = pending.split(':')
            block_num = int(block_num)
            
            if self.detector.is_token_confirmed(block_num, current_block, settings.confirmation_blocks):
                # Update token as confirmed
                db = SessionLocal()
                try:
                    token = db.query(Token).filter(
                        Token.address == address.lower(),
                        Token.network == self.network
                    ).first()
                    
                    if token and not token.confirmed:
                        token.confirmed = True
                        db.commit()
                        self.logger.success(f"✅ Confirmed: {token.symbol or token.address[:10]}...")
                        confirmed_tokens.add(pending)
                
                except Exception as e:
                    self.logger.error(f"Error confirming token: {e}")
                    db.rollback()
                finally:
                    db.close()
        
        # Remove confirmed tokens from pending
        self.pending_tokens -= confirmed_tokens
    
    async def monitor_blocks(self):
        """Monitor new blocks continuously"""
        self.logger.info(f"🚀 Starting block monitor for {self.network}")
        
        # Check if connected before starting
        if not self.w3.is_connected():
            self.logger.error(f"❌ Cannot monitor {self.network}: Not connected to RPC")
            return
        
        consecutive_errors = 0
        max_consecutive_errors = 10
        
        try:
            last_processed_block = self.w3.eth.block_number
            self.logger.info(f"Starting from block {last_processed_block}")
        except Exception as e:
            self.logger.error(f"❌ Cannot get initial block number for {self.network}: {e}")
            return
        
        while True:
            try:
                # Reset error counter on successful operation
                consecutive_errors = 0
                
                current_block = self.w3.eth.block_number
                
                # Process new blocks
                if current_block > last_processed_block:
                    for block_num in range(last_processed_block + 1, current_block + 1):
                        try:
                            await self.process_block(block_num)
                        except Exception as block_error:
                            self.logger.error(f"Failed to process block {block_num}: {block_error}")
                            # Continue with next block instead of crashing
                            continue
                    
                    last_processed_block = current_block
                
                # Check pending confirmations
                try:
                    await self.check_pending_confirmations()
                except Exception as confirm_error:
                    self.logger.error(f"Error checking pending confirmations: {confirm_error}")
                    # Continue monitoring even if confirmation check fails
                
                # Wait before next check
                await asyncio.sleep(12)  # ~12 seconds per block for ETH
            
            except Exception as e:
                consecutive_errors += 1
                self.logger.error(f"Error in monitor loop (attempt {consecutive_errors}/{max_consecutive_errors}): {e}")
                
                # If too many consecutive errors, wait longer before retrying
                if consecutive_errors >= max_consecutive_errors:
                    self.logger.error(f"Too many consecutive errors for {self.network}. Waiting 60 seconds before retrying...")
                    await asyncio.sleep(60)
                    consecutive_errors = 0  # Reset after long wait
                else:
                    # Exponential backoff: 5s, 10s, 20s, etc.
                    wait_time = min(5 * (2 ** (consecutive_errors - 1)), 60)
                    await asyncio.sleep(wait_time)


async def main():
    """Main function to run both ETH and BSC monitors"""
    logger.info("🎯 RealTime Token Scanner - Ingestor Service")
    logger.info(f"Database: {settings.database_url.split('@')[1]}")
    
    # Create monitors for both networks
    eth_monitor = BlockchainMonitor(
        settings.eth_rpc_url,
        settings.eth_ws_url,
        "ETH"
    )
    
    bsc_monitor = BlockchainMonitor(
        settings.bsc_rpc_url,
        settings.bsc_ws_url,
        "BSC"
    )
    
    # Run both monitors concurrently
    await asyncio.gather(
        eth_monitor.monitor_blocks(),
        bsc_monitor.monitor_blocks()
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Shutting down gracefully...")
        sys.exit(0)


