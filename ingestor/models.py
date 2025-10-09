from sqlalchemy import Column, Integer, String, BigInteger, Boolean, TIMESTAMP, Numeric, Text, Index
from sqlalchemy.sql import func
from database import Base


class Token(Base):
    __tablename__ = "tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    address = Column(Text, nullable=False)
    block_number = Column(BigInteger, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False, server_default=func.now())
    network = Column(String(10), nullable=False)
    
    # Token metadata
    name = Column(Text, nullable=True)
    symbol = Column(Text, nullable=True)
    decimals = Column(Integer, nullable=True)
    total_supply = Column(Numeric(precision=78, scale=0), nullable=True)
    
    # Additional info
    creator_address = Column(Text, nullable=True)
    tx_hash = Column(Text, nullable=True)
    confirmed = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    risk_score = Column(Integer, default=0)
    
    __table_args__ = (
        Index('idx_token_addr_network', 'address', 'network', unique=True),
        Index('idx_token_timestamp', 'timestamp'),
        Index('idx_token_network', 'network'),
        Index('idx_token_confirmed', 'confirmed'),
    )


