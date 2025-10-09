from web3 import Web3
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential
from typing import Optional, Dict
from abi import ERC20_ABI


class TokenDetector:
    def __init__(self, w3: Web3, network: str):
        self.w3 = w3
        self.network = network
    
    def is_contract_creation(self, tx_hash: str) -> tuple[bool, Optional[str]]:
        """Check if transaction is a contract creation and return contract address"""
        try:
            tx_receipt = self.w3.eth.get_transaction_receipt(tx_hash)
            
            # Contract creation has contractAddress in receipt
            if tx_receipt and tx_receipt.get('contractAddress'):
                contract_address = tx_receipt['contractAddress']
                logger.debug(f"Contract created at {contract_address}")
                return True, contract_address
            
            return False, None
        
        except Exception as e:
            logger.error(f"Error checking contract creation: {e}")
            return False, None
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    def fetch_token_metadata(self, contract_address: str) -> Optional[Dict]:
        """Fetch ERC20 token metadata"""
        try:
            # Create contract instance
            contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(contract_address),
                abi=ERC20_ABI
            )
            
            metadata = {}
            
            # Try to fetch each field with error handling
            try:
                metadata['name'] = contract.functions.name().call()
            except Exception as e:
                logger.debug(f"Failed to get name: {e}")
                metadata['name'] = None
            
            try:
                metadata['symbol'] = contract.functions.symbol().call()
            except Exception as e:
                logger.debug(f"Failed to get symbol: {e}")
                metadata['symbol'] = None
            
            try:
                metadata['decimals'] = contract.functions.decimals().call()
            except Exception as e:
                logger.debug(f"Failed to get decimals: {e}")
                metadata['decimals'] = None
            
            try:
                metadata['total_supply'] = contract.functions.totalSupply().call()
            except Exception as e:
                logger.debug(f"Failed to get totalSupply: {e}")
                metadata['total_supply'] = None
            
            # If we got at least symbol or name, consider it a token
            if metadata.get('symbol') or metadata.get('name'):
                logger.info(f"✅ Token detected: {metadata.get('name', 'Unknown')} ({metadata.get('symbol', 'N/A')})")
                return metadata
            else:
                logger.debug(f"Contract {contract_address} is not a standard ERC20 token")
                return None
        
        except Exception as e:
            logger.error(f"Error fetching token metadata for {contract_address}: {e}")
            return None
    
    def get_transaction_details(self, tx_hash: str) -> Optional[Dict]:
        """Get transaction details including sender"""
        try:
            tx = self.w3.eth.get_transaction(tx_hash)
            if tx:
                return {
                    'from': tx['from'],
                    'to': tx.get('to'),
                    'hash': tx['hash'].hex()
                }
            return None
        except Exception as e:
            logger.error(f"Error getting transaction details: {e}")
            return None
    
    def is_token_confirmed(self, token_block: int, current_block: int, confirmations: int = 3) -> bool:
        """Check if token has enough confirmations"""
        return (current_block - token_block) >= confirmations


