# 🚀 Quick Start Guide

Get RealTime Token Scanner up and running in 5 minutes!

## Prerequisites

- Docker & Docker Compose installed
- RPC API keys (free tier is fine)

## Step 1: Get API Keys

### Option A: Alchemy (Recommended)

1. Go to [https://www.alchemy.com/](https://www.alchemy.com/)
2. Sign up for free account
3. Create new app for Ethereum Mainnet
4. Copy the HTTP and WebSocket URLs

### Option B: Infura

1. Go to [https://infura.io/](https://infura.io/)
2. Sign up and create new project
3. Copy endpoints for Ethereum Mainnet

## Step 2: Setup Environment

```bash
# Clone repository
git clone <your-repo>
cd "RealTime Scanner"

# Copy environment template
cp env.example .env

# Edit .env file (use your favorite editor)
nano .env  # or code .env
```

**Edit these lines in .env:**

```env
ETH_RPC_URL=https://eth-mainnet.g.alchemy.com/v2/YOUR_ACTUAL_API_KEY
ETH_WS_URL=wss://eth-mainnet.g.alchemy.com/v2/YOUR_ACTUAL_API_KEY
BSC_RPC_URL=https://bsc-dataseed.binance.org/
BSC_WS_URL=wss://bsc-ws-node.nariox.org:443
```

## Step 3: Launch Application

### Using Docker Compose (Easiest)

```bash
docker-compose up --build
```

### Using Make (If available)

```bash
make build
make up-logs
```

Wait for services to start (~30 seconds). You'll see:

```
✅ realtime_scanner_db     ... started
✅ realtime_scanner_api    ... started
✅ realtime_scanner_ingestor ... started
✅ realtime_scanner_ui     ... started
```

## Step 4: Access Application

Open your browser:

- **🌐 Dashboard**: http://localhost:3000
- **📚 API Docs**: http://localhost:8000/docs
- **🔍 Health Check**: http://localhost:8000/health

## Step 5: Verify It's Working

### Check API Health

```bash
curl http://localhost:8000/health
```

Expected output:
```json
{
  "status": "healthy",
  "database": "healthy",
  "timestamp": "2025-10-08T10:30:00"
}
```

### Check Ingestor Logs

```bash
docker-compose logs ingestor
```

You should see:
```
🔗 Connected to ETH: True
🔗 Connected to BSC: True
🚀 Starting block monitor for ETH
🚀 Starting block monitor for BSC
```

### View Dashboard

Go to http://localhost:3000 and you should see:
- Stats cards at the top
- Network filter buttons
- Charts showing token distribution
- Table of detected tokens (may be empty initially)

## Troubleshooting

### Issue: Services not starting

**Solution:**
```bash
# Check Docker is running
docker ps

# View logs
docker-compose logs
```

### Issue: API not connecting to database

**Solution:**
```bash
# Restart services
docker-compose restart

# Or rebuild
docker-compose down
docker-compose up --build
```

### Issue: Frontend shows "No tokens found"

This is normal! The ingestor needs time to detect tokens. Options:

**Option 1: Wait** (tokens will appear as they're deployed on blockchain)

**Option 2: Generate test data**
```bash
# Install Python dependencies
pip install sqlalchemy psycopg2-binary

# Generate 50 test tokens
python scripts/test_data_generator.py --num 50

# Refresh dashboard
```

### Issue: RPC rate limit errors

**Solution:**
- Upgrade to paid Alchemy/Infura plan
- Reduce `CONFIRMATION_BLOCKS` in .env
- Use multiple RPC providers

## Testing With Sample Data

To quickly see the dashboard in action:

```bash
# Generate 100 sample tokens
docker-compose exec api python /app/../scripts/test_data_generator.py --num 100

# Or from host (if Python installed)
python scripts/test_data_generator.py --num 100

# Refresh browser at http://localhost:3000
```

## Useful Commands

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f ingestor
```

### Database Access
```bash
# Connect to PostgreSQL
docker-compose exec db psql -U scanner -d token_scanner

# Query tokens
SELECT name, symbol, network, timestamp FROM tokens ORDER BY timestamp DESC LIMIT 10;
```

### Stop Services
```bash
# Stop (keep data)
docker-compose down

# Stop and remove data
docker-compose down -v
```

### Restart Services
```bash
docker-compose restart
```

## Next Steps

1. **Customize** - Edit network filters, add more chains
2. **Deploy** - Use production RPC endpoints
3. **Monitor** - Set up alerts for high-value tokens
4. **Extend** - Add price tracking, DEX integration

## Support

- 📖 Full docs: See [README.md](README.md)
- 🐛 Issues: Open GitHub issue
- 💬 Questions: Check existing issues

---

**Happy token hunting! 🔍🚀**


