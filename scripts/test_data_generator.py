"""
Test Data Generator for RealTime Token Scanner
Generates sample token data for testing purposes
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from datetime import datetime, timedelta
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Token, Base

# Database connection
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://scanner:scanner123@localhost:5432/token_scanner')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Sample token names and symbols
TOKEN_NAMES = [
    "SafeMoon", "ElonCoin", "DogeKiller", "ShibaSwap", "MoonToken",
    "RocketFuel", "DiamondHands", "ToTheMoon", "WhaleToken", "PumpCoin",
    "MetaVerse", "CryptoGem", "DeFiToken", "YieldFarm", "StakingPro",
    "BurnToken", "ReflectCoin", "SafeVault", "MegaMoon", "UltraCoin"
]

SYMBOL_PREFIXES = ["SAFE", "MOON", "DOGE", "SHIB", "ELON", "META", "DEFI", "YIELD", "BURN", "MEGA"]
SYMBOL_SUFFIXES = ["", "X", "V2", "PRO", "MAX"]

NETWORKS = ["ETH", "BSC"]


def generate_random_address():
    """Generate a random Ethereum-like address"""
    return "0x" + ''.join(random.choices('0123456789abcdef', k=40))


def generate_token_data(network, timestamp):
    """Generate random token data"""
    name = random.choice(TOKEN_NAMES) + random.choice(["", " V2", " Token", " Coin"])
    symbol = random.choice(SYMBOL_PREFIXES) + random.choice(SYMBOL_SUFFIXES)
    
    return {
        'address': generate_random_address(),
        'block_number': random.randint(15000000, 21000000) if network == "ETH" else random.randint(20000000, 35000000),
        'timestamp': timestamp,
        'network': network,
        'name': name,
        'symbol': symbol,
        'decimals': random.choice([18, 9, 6, 8]),
        'total_supply': random.randint(1000000, 1000000000000) * (10 ** 18),
        'creator_address': generate_random_address(),
        'tx_hash': "0x" + ''.join(random.choices('0123456789abcdef', k=64)),
        'confirmed': random.choice([True, True, True, False]),  # 75% confirmed
        'is_verified': random.choice([True, False, False]),  # 33% verified
        'risk_score': random.randint(0, 10)
    }


def generate_test_tokens(num_tokens=100):
    """Generate test tokens and insert into database"""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    print(f"🔧 Generating {num_tokens} test tokens...")
    
    try:
        now = datetime.utcnow()
        tokens_created = 0
        
        for i in range(num_tokens):
            # Random timestamp within last 7 days
            hours_ago = random.randint(0, 168)  # 7 days
            timestamp = now - timedelta(hours=hours_ago)
            
            # Random network
            network = random.choice(NETWORKS)
            
            # Generate token data
            token_data = generate_token_data(network, timestamp)
            
            # Check if token already exists
            existing = db.query(Token).filter(
                Token.address == token_data['address'],
                Token.network == network
            ).first()
            
            if not existing:
                token = Token(**token_data)
                db.add(token)
                tokens_created += 1
                
                if (i + 1) % 10 == 0:
                    print(f"  Created {i + 1}/{num_tokens} tokens...")
        
        db.commit()
        print(f"✅ Successfully created {tokens_created} test tokens!")
        
        # Show stats
        total = db.query(Token).count()
        eth_count = db.query(Token).filter(Token.network == "ETH").count()
        bsc_count = db.query(Token).filter(Token.network == "BSC").count()
        
        print(f"\n📊 Database Stats:")
        print(f"  Total tokens: {total}")
        print(f"  ETH tokens: {eth_count}")
        print(f"  BSC tokens: {bsc_count}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
    finally:
        db.close()


def clear_all_tokens():
    """Clear all tokens from database"""
    db = SessionLocal()
    try:
        count = db.query(Token).count()
        db.query(Token).delete()
        db.commit()
        print(f"🗑️  Cleared {count} tokens from database")
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate test data for RealTime Token Scanner')
    parser.add_argument('--clear', action='store_true', help='Clear all existing tokens')
    parser.add_argument('--num', type=int, default=100, help='Number of tokens to generate (default: 100)')
    
    args = parser.parse_args()
    
    if args.clear:
        clear_all_tokens()
    
    generate_test_tokens(args.num)


