from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional
from decimal import Decimal


class TokenBase(BaseModel):
    address: str
    network: str
    name: Optional[str] = None
    symbol: Optional[str] = None
    decimals: Optional[int] = None
    total_supply: Optional[str] = None


class TokenCreate(TokenBase):
    block_number: int
    creator_address: Optional[str] = None
    tx_hash: Optional[str] = None


class TokenResponse(TokenBase):
    id: int
    block_number: int
    timestamp: datetime
    creator_address: Optional[str] = None
    tx_hash: Optional[str] = None
    confirmed: bool
    is_verified: bool
    risk_score: int
    
    @field_validator('total_supply', mode='before')
    @classmethod
    def convert_decimal_to_string(cls, v):
        """Convert Decimal to string for total_supply"""
        if v is None:
            return None
        if isinstance(v, Decimal):
            return str(v)
        return v
    
    class Config:
        from_attributes = True


class StatsResponse(BaseModel):
    total_tokens: int
    tokens_last_24h: int
    tokens_last_hour: int
    by_network: dict
    hourly_distribution: list


class HealthResponse(BaseModel):
    status: str
    database: str
    timestamp: datetime


