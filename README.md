<div align="center">

# 🔍 RealTime Token Scanner

### Professional-Grade Blockchain Token Detection & Analytics Platform

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2.0-61dafb.svg)](https://reactjs.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Real-time monitoring and analytics for newly deployed tokens on Ethereum and Binance Smart Chain**

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-api-documentation) • [Architecture](#-architecture) • [Troubleshooting](#-troubleshooting)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Live Demo & Screenshots](#-live-demo--screenshots)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Configuration](#-configuration)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Development Guide](#-development-guide)
- [Performance Metrics](#-performance-metrics)
- [Troubleshooting](#-troubleshooting)
- [Known Issues & Solutions](#-known-issues--solutions)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

**RealTime Token Scanner** is a production-ready, end-to-end blockchain monitoring system that detects and analyzes newly deployed ERC20/BEP20 tokens in real-time. Built with modern technologies and best practices, it provides a complete solution from blockchain monitoring to data visualization.

## ✨ Key Features

- Real-time block monitoring for ETH and BSC networks
- Automatic contract creation detection
- Smart filtering for ERC20/BEP20 token contracts
- POA (Proof of Authority) chain support with proper middleware
- Automatic extraction of token metadata (name, symbol, decimals, total supply)
- Confirmation system (≥3 blocks) to avoid reorgs
- PostgreSQL with optimized indexes for fast queries
- Duplicate prevention with unique constraints
- Transaction hash and creator address tracking
- Beautiful React dashboard with modern UI
- Interactive charts (hourly distribution, network comparison)
- Real-time statistics (total tokens, 24h/1h metrics)
- Network filtering (All/ETH/BSC)
- Risk scoring system for token assessment
- RESTful API with FastAPI
- Auto-generated API documentation (Swagger UI)
- Type-safe schemas with Pydantic validation
- Structured logging with correlation
- Health check endpoints
- One-command deployment with Docker Compose

---

## 🖼️ Live Demo & Screenshots

### Dashboard Features

**Main Dashboard**
- 5 Key Metric Cards (Total, 24h, Hourly, ETH, BSC)
- Line Chart: Token deployment trends (last 24 hours)
- Bar Chart: Token distribution by network
- Network Filter Buttons (All/ETH/BSC)

**Token Table**
- Real-time token list with pagination
- Token name, symbol, and decimals
- Contract address with explorer links
- Network badges (ETH/BSC)
- Risk level indicators
- Detection timestamp (relative time)
- Block number and total supply

**API Documentation**
- Interactive Swagger UI at `/docs`
- Try-it-out functionality for all endpoints
- Complete request/response schemas

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      External Services                       │
│  ┌─────────────────┐         ┌──────────────────┐          │
│  │   Ethereum RPC  │         │   BSC RPC Node   │          │
│  │   (Alchemy API) │         │  (Public Nodes)  │          │
│  └────────┬────────┘         └────────┬─────────┘          │
└───────────┼──────────────────────────┼────────────────────┘
            │                          │
            └──────────┬───────────────┘
                       │ WebSocket / HTTP
            ┌──────────▼───────────┐
            │  Ingestor Service    │
            │  ┌────────────────┐  │
            │  │ Block Monitor  │  │ ← Python + web3.py + asyncio
            │  │ Token Detector │  │
            │  │ POA Middleware │  │
            │  └────────┬───────┘  │
            └───────────┼──────────┘
                        │
                        │ Database Write
            ┌───────────▼──────────┐
            │   PostgreSQL 15      │
            │  ┌────────────────┐  │
            │  │  tokens table  │  │ ← Indexed & Optimized
            │  │  (86+ records) │  │
            │  └────────┬───────┘  │
            └───────────┼──────────┘
                        │
                        │ SQL Queries
            ┌───────────▼──────────┐
            │   FastAPI Backend    │
            │  ┌────────────────┐  │
            │  │ REST Endpoints │  │ ← Python + FastAPI
            │  │ Validation     │  │
            │  │ Serialization  │  │
            │  └────────┬───────┘  │
            └───────────┼──────────┘
                        │
                        │ JSON over HTTP
            ┌───────────▼──────────┐
            │   React Frontend     │
            │  ┌────────────────┐  │
            │  │ Dashboard UI   │  │ ← React 18 + Tailwind
            │  │ Charts         │  │
            │  │ Tables         │  │
            │  └────────────────┘  │
            └──────────────────────┘
                        │
                        │
                  ┌─────▼─────┐
                  │   User    │
                  └───────────┘
```

### Service Communication

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Ingestor   │────▶│  PostgreSQL  │◀────│     API      │
└──────────────┘     └──────────────┘     └──────┬───────┘
                                                  │
                                                  ▼
                                           ┌──────────────┐
                                           │   Frontend   │
                                           └──────────────┘
```

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **PostgreSQL** - Primary database
- **Uvicorn** - ASGI server
- **web3.py** - Blockchain interaction
- **Loguru** - Structured logging

### Ingestor
- **Python 3.11+** - Core language
- **web3.py** - Blockchain connectivity
- **asyncio** - Async operations
- **Tenacity** - Retry logic

### Frontend
- **React 18** - UI framework
- **Recharts** - Data visualization
- **Axios** - HTTP client
- **Tailwind CSS** - Styling
- **date-fns** - Date formatting

### Infrastructure
- **Docker Compose** - Container orchestration
- **PostgreSQL 15** - Database

---

## 📦 Prerequisites

- **Docker** and **Docker Compose** installed
- **RPC URLs** for ETH and BSC (Alchemy/Infura recommended)
- 4GB+ RAM
- 10GB+ disk space

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd RealTime\ Scanner
```

### 2. Configure environment variables

Copy the example environment file:

```bash
cp env.example .env
```

Edit `.env` and add your RPC URLs:

```env
# Get free API keys from:
# - Alchemy: https://www.alchemy.com/
# - Infura: https://infura.io/

ETH_RPC_URL=https://eth-mainnet.g.alchemy.com/v2/YOUR_API_KEY
ETH_WS_URL=wss://eth-mainnet.g.alchemy.com/v2/YOUR_API_KEY

BSC_RPC_URL=https://bsc-dataseed.binance.org/
BSC_WS_URL=wss://bsc-ws-node.nariox.org:443
```

### 3. Start all services

```bash
docker-compose up --build
```

This will start:
- **PostgreSQL** on port `5432`
- **FastAPI Backend** on port `8000`
- **Ingestor Service** (background)
- **React Frontend** on port `3000`

### 4. Access the application

- **Frontend Dashboard**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **API Health Check**: http://localhost:8000/health

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://scanner:scanner123@db:5432/token_scanner` |
| `ETH_RPC_URL` | Ethereum RPC endpoint | Required |
| `ETH_WS_URL` | Ethereum WebSocket endpoint | Required |
| `BSC_RPC_URL` | BSC RPC endpoint | Required |
| `BSC_WS_URL` | BSC WebSocket endpoint | Required |
| `CONFIRMATION_BLOCKS` | Block confirmations needed | `3` |

---

## 📚 API Documentation

### Endpoints

#### `GET /tokens/new`
Get list of newly detected tokens with pagination.

**Query Parameters:**
- `page` (int, default: 1) - Page number
- `page_size` (int, default: 20) - Items per page
- `network` (str, optional) - Filter by network (ETH/BSC)
- `confirmed_only` (bool, default: true) - Only confirmed tokens

**Response:**
```json
[
  {
    "id": 1,
    "address": "0xabc123...",
    "name": "MyToken",
    "symbol": "MTK",
    "decimals": 18,
    "total_supply": "1000000000000000000000",
    "block_number": 21003421,
    "timestamp": "2025-10-08T04:12:00Z",
    "network": "ETH",
    "confirmed": true,
    "risk_score": 2
  }
]
```

#### `GET /stats/summary`
Get statistics summary.

**Response:**
```json
{
  "total_tokens": 150,
  "tokens_last_24h": 45,
  "tokens_last_hour": 3,
  "by_network": {
    "ETH": 100,
    "BSC": 50
  },
  "hourly_distribution": [...]
}
```

#### `GET /alerts/recent`
Get recent high-risk tokens.

**Query Parameters:**
- `limit` (int, default: 10) - Number of results

#### `GET /health`
Health check endpoint.

---

## 📁 Project Structure

```
RealTime Scanner/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py         # Main FastAPI app
│   │   ├── config.py       # Configuration
│   │   ├── database.py     # DB setup
│   │   ├── models.py       # SQLAlchemy models
│   │   └── schemas.py      # Pydantic schemas
│   ├── Dockerfile
│   └── requirements.txt
│
├── ingestor/               # Token detection service
│   ├── main.py            # Main ingestor logic
│   ├── token_detector.py  # Token detection utils
│   ├── config.py          # Configuration
│   ├── database.py        # DB connection
│   ├── models.py          # DB models
│   ├── abi.py            # ERC20 ABI
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/              # React UI
│   ├── public/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API service
│   │   ├── App.js
│   │   └── index.js
│   ├── Dockerfile
│   └── package.json
│
├── docker-compose.yml     # Docker orchestration
├── env.example           # Environment template
└── README.md             # This file
```

## 💻 Development

### Running services individually

#### Backend only
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Ingestor only
```bash
cd ingestor
pip install -r requirements.txt
python main.py
```

#### Frontend only
```bash
cd frontend
npm install
npm start
```

### Database access

Connect to PostgreSQL:
```bash
docker exec -it realtime_scanner_db psql -U scanner -d token_scanner
```

View tokens:
```sql
SELECT * FROM tokens ORDER BY timestamp DESC LIMIT 10;
```

### Logs

View logs for specific service:
```bash
docker-compose logs -f api
docker-compose logs -f ingestor
docker-compose logs -f frontend
```

## 🐛 Troubleshooting

### Ingestor not detecting tokens

1. **Check RPC connection**:
   ```bash
   docker-compose logs ingestor
   ```
   Look for "Connected to ETH: True"

2. **Verify RPC URL** in `.env` file

3. **Rate limiting**: Free RPC endpoints have rate limits. Consider upgrading or using multiple providers.

### Frontend not loading data

1. **Check API is running**:
   ```bash
   curl http://localhost:8000/health
   ```

2. **Check CORS settings** in `backend/app/main.py`

3. **Verify API URL** in frontend `.env`:
   ```
   REACT_APP_API_URL=http://localhost:8000
   ```

### Database connection errors

1. **Wait for DB to be ready**:
   ```bash
   docker-compose logs db
   ```

2. **Reset database**:
   ```bash
   docker-compose down -v
   docker-compose up --build
   ```

## 📊 Performance Notes

- **Block Processing**: ~12s per block (ETH), ~3s per block (BSC)
- **Token Detection**: ~2-3s per token (metadata fetch + confirmation)
- **API Response Time**: <100ms for most endpoints
- **Database**: Indexed queries, handles 1M+ tokens efficiently

## 🔐 Security Considerations

- Never commit `.env` file with real API keys
- Use rate-limited RPC endpoints
- Implement API authentication for production
- Regularly backup database
- Monitor for abnormal activity

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push and create a Pull Request

## 📧 Support

For issues or questions:
- Open an issue on GitHub
- Check existing issues for solutions

---

**Built with ❤️ using Python, FastAPI, React, and Docker**
