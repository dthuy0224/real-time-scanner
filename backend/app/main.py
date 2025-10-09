from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc, text
from datetime import datetime, timedelta
from typing import List, Optional
from loguru import logger
import sys

from app.database import get_db, engine, Base
from app.models import Token
from app.schemas import TokenResponse, StatsResponse, HealthResponse
from app.config import get_settings

# Configure logger
logger.remove()
logger.add(sys.stdout, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>")

settings = get_settings()

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="RealTime Token Scanner API",
    description="API for tracking newly deployed tokens on ETH and BSC",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "RealTime Token Scanner API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "unhealthy"
    
    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "database": db_status,
        "timestamp": datetime.utcnow()
    }


@app.get("/tokens/new", response_model=List[TokenResponse])
async def get_new_tokens(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    network: Optional[str] = Query(None, regex="^(ETH|BSC)$"),
    confirmed_only: bool = Query(True),
    db: Session = Depends(get_db)
):
    """Get list of newly detected tokens with pagination"""
    try:
        query = db.query(Token)
        
        # Filter by network if specified
        if network:
            query = query.filter(Token.network == network)
        
        # Filter confirmed tokens only
        if confirmed_only:
            query = query.filter(Token.confirmed == True)
        
        # Order by timestamp descending (newest first)
        query = query.order_by(desc(Token.timestamp))
        
        # Pagination
        offset = (page - 1) * page_size
        tokens = query.offset(offset).limit(page_size).all()
        
        logger.info(f"Retrieved {len(tokens)} tokens (page {page}, network: {network or 'all'})")
        
        return tokens
    
    except Exception as e:
        logger.error(f"Error fetching tokens: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tokens/{token_id}", response_model=TokenResponse)
async def get_token_by_id(token_id: int, db: Session = Depends(get_db)):
    """Get specific token by ID"""
    token = db.query(Token).filter(Token.id == token_id).first()
    
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")
    
    return token


@app.get("/tokens/address/{address}", response_model=TokenResponse)
async def get_token_by_address(
    address: str,
    network: str = Query(..., regex="^(ETH|BSC)$"),
    db: Session = Depends(get_db)
):
    """Get token by contract address and network"""
    token = db.query(Token).filter(
        and_(Token.address == address.lower(), Token.network == network)
    ).first()
    
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")
    
    return token


@app.get("/stats/summary", response_model=StatsResponse)
async def get_stats_summary(db: Session = Depends(get_db)):
    """Get statistics summary"""
    try:
        now = datetime.utcnow()
        last_24h = now - timedelta(hours=24)
        last_hour = now - timedelta(hours=1)
        
        # Total tokens
        total_tokens = db.query(func.count(Token.id)).scalar()
        
        # Tokens in last 24 hours
        tokens_24h = db.query(func.count(Token.id)).filter(
            Token.timestamp >= last_24h
        ).scalar()
        
        # Tokens in last hour
        tokens_1h = db.query(func.count(Token.id)).filter(
            Token.timestamp >= last_hour
        ).scalar()
        
        # By network
        by_network = {}
        network_stats = db.query(
            Token.network,
            func.count(Token.id)
        ).group_by(Token.network).all()
        
        for network, count in network_stats:
            by_network[network] = count
        
        # Hourly distribution (last 24 hours)
        hourly_dist = []
        for i in range(24):
            hour_start = now - timedelta(hours=i+1)
            hour_end = now - timedelta(hours=i)
            
            count = db.query(func.count(Token.id)).filter(
                and_(Token.timestamp >= hour_start, Token.timestamp < hour_end)
            ).scalar()
            
            hourly_dist.append({
                "hour": hour_start.strftime("%Y-%m-%d %H:00"),
                "count": count
            })
        
        hourly_dist.reverse()  # Oldest to newest
        
        return {
            "total_tokens": total_tokens,
            "tokens_last_24h": tokens_24h,
            "tokens_last_hour": tokens_1h,
            "by_network": by_network,
            "hourly_distribution": hourly_dist
        }
    
    except Exception as e:
        logger.error(f"Error generating stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/alerts/recent")
async def get_recent_alerts(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get recent high-risk or notable tokens"""
    try:
        # Get tokens with risk score > 0 or unverified
        tokens = db.query(Token).filter(
            Token.risk_score > 0
        ).order_by(desc(Token.timestamp)).limit(limit).all()
        
        return [token.to_dict() for token in tokens]
    
    except Exception as e:
        logger.error(f"Error fetching alerts: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.api_host, port=settings.api_port)


