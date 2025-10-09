from sqlalchemy import Column, Integer, String, BigInteger, Boolean, TIMESTAMP, Numeric, Text, Index
from sqlalchemy.sql import func
from app.database import Base


class Token(Base):
    __tablename__ = "tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    address = Column(Text, nullable=False)
    block_number = Column(BigInteger, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False, server_default=func.now())
    network = Column(String(10), nullable=False)  # ETH, BSC
    
    # Token metadata
    name = Column(Text, nullable=True)
    symbol = Column(Text, nullable=True)
    decimals = Column(Integer, nullable=True)
    total_supply = Column(Numeric(precision=78, scale=0), nullable=True)  # Large numbers for tokens
    
    # Additional info
    creator_address = Column(Text, nullable=True)
    tx_hash = Column(Text, nullable=True)
    confirmed = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    
    # Risk scoring (optional for future)
    risk_score = Column(Integer, default=0)
    
    __table_args__ = (
        Index('idx_token_addr_network', 'address', 'network', unique=True),
        Index('idx_token_timestamp', 'timestamp'),
        Index('idx_token_network', 'network'),
        Index('idx_token_confirmed', 'confirmed'),
    )
    
    def to_dict(self):
        return {
            "id": self.id,
            "address": self.address,
            "block_number": self.block_number,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "network": self.network,
            "name": self.name,
            "symbol": self.symbol,
            "decimals": self.decimals,
            "total_supply": str(self.total_supply) if self.total_supply else None,
            "creator_address": self.creator_address,
            "tx_hash": self.tx_hash,
            "confirmed": self.confirmed,
            "is_verified": self.is_verified,
            "risk_score": self.risk_score
        }


