from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://scanner:scanner123@db:5432/token_scanner"
    
    # Ethereum
    eth_rpc_url: str = "https://eth-mainnet.g.alchemy.com/v2/your-api-key"
    eth_ws_url: str = "wss://eth-mainnet.g.alchemy.com/v2/your-api-key"
    
    # Binance Smart Chain
    bsc_rpc_url: str = "https://bsc-dataseed.binance.org/"
    bsc_ws_url: str = "wss://bsc-ws-node.nariox.org:443"
    
    # Confirmation settings
    confirmation_blocks: int = 3
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()


