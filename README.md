# Cryptocurrency Tracker

Flask web application that fetches live cryptocurrency data from the CoinGecko API and allows users to maintain a personal watchlist with full CRUD operations. Features a professional Coinbase-inspired UI with dark theme support, dual navigation (desktop/mobile), and global market metrics.

## API Chosen & Why

**CoinGecko API** - Free tier with generous rate limits, simple JSON responses, broad cryptocurrency coverage (13,000+ coins), and no authentication required for basic endpoints. Provides comprehensive data including price, market cap, 24h changes, and global market statistics.

## What the Crypto Blueprint Does

1. **Fetch** - Form accepts `coin_id` (e.g., bitcoin, ethereum) → calls CoinGecko `/coins/{id}` endpoint → fetches price, market cap, symbol, image
2. **Display** - Shows fetched data with 24h price change percentage
3. **Save** - User can save coin to MySQL `watchlist` table with optional note
4. **Read** - View all saved coins, or view individual coin details with live vs. saved price comparison
5. **Update** - Edit notes on saved coins, refresh individual coin prices
6. **Delete** - Remove coins from watchlist

Additional features: Top 10 coins by volume, global market metrics on home page.

## Setup Instructions

### Dependencies

Install required packages:

```bash
pip install -r requirements.txt
```

Key dependencies: `Flask`, `requests`, `python-dotenv`, `PyMySQL`

### Environment Variables

Create a `.env` file with the following keys:

```bash
# JawsDB MySQL Connection
DB_HOST=your_jawsdb_host.rds.amazonaws.com
DB_USER=your_username
DB_PASSWORD=your_password
DB_PORT=3306
DB_NAME=your_database_name

# Optional: Alternative database URL format
# DATABASE_URL=mysql://user:pass@host:3306/dbname
# JAWSDB_URL=mysql://user:pass@host:3306/dbname

# CoinGecko API (optional - use for higher rate limits)
COINGECKO_API_KEY=your_api_key_here

# Default vs_currency for price queries
DEFAULT_VS=usd
```

**CoinGecko API Key**: Optional for free tier usage. If provided, it will be included in request headers. Get one at [CoinGecko API](https://www.coingecko.com/en/api).

### Database Setup

Create the `watchlist` table:

```sql
CREATE TABLE watchlist (
    id INT AUTO_INCREMENT PRIMARY KEY,
    coin_id VARCHAR(64) NOT NULL,
    name VARCHAR(128),
    symbol VARCHAR(32),
    price DECIMAL(18, 6),
    market_cap BIGINT,
    note VARCHAR(255) DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

Or run the setup script:

```bash
python database/setup_crypto_db.py
```

## How to Run

### Development Server

```bash
python app.py
```

Or using Flask CLI:

```bash
flask run
```

The application will start on `http://127.0.0.1:5000`

**Note**: If port 5000 is in use (macOS AirPlay Receiver), kill the process:

```bash
lsof -ti:5000 | xargs kill -9
```

## Project Structure

```
app/
├── blueprints/
│   └── crypto.py          # Crypto routes & CRUD operations
├── services/
│   └── coingecko_service.py  # API calls with 120s caching
├── static/css/
│   └── app.css            # Coinbase-inspired theme with dark mode
├── templates/
│   ├── base.html          # Base template with dual navigation
│   ├── index.html         # Home page with market metrics
│   ├── crypto.html        # Main tracker & fetch form
│   ├── watchlist.html     # Saved coins table
│   ├── view_coin.html     # Individual coin details
│   └── top_coins.html     # Top 10 by volume
├── db_connect.py          # MySQL connection helper
└── routes.py              # Main app routes

database/
└── setup_crypto_db.py     # Table creation script
```

## Features

- **Live Price Tracking** - Real-time cryptocurrency data from CoinGecko
- **Watchlist Management** - Save, edit notes, refresh prices, delete coins
- **Global Market Metrics** - Total market cap, 24h volume, BTC/ETH dominance
- **Top 10 Coins** - View highest volume cryptocurrencies
- **Dark Theme** - Auto-detects system preference or manual toggle
- **Mobile Responsive** - Bottom tab navigation for mobile devices
- **Caching** - 120-second TTL cache to reduce API calls

---

© 2025 Ethan | Built with Flask & CoinGecko
