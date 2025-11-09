# Cryptocurrency Tracker Setup - Module 6

## What Was Added

This update adds a minimal cryptocurrency tracker blueprint to your existing Flask starter kit.

### New Files Created:

1. **app/blueprints/crypto.py** - Crypto blueprint with CoinGecko API integration
2. **app/templates/crypto.html** - Crypto tracker interface
3. **database/setup_crypto_db.py** - Python script to create database table
4. **database/create_watchlist_table.sql** - SQL script (alternative setup method)

### Files Modified:

1. **requirements.txt** - Added `requests==2.32.3` for API calls
2. **app/__init__.py** - Registered crypto blueprint at `/crypto`
3. **app/templates/base.html** - Updated branding to "MY NAME — Module 6", navbar (Home | Crypto), and added footer

### Database Table:

**watchlist** table with:
- `id` (INT, AUTO_INCREMENT, PRIMARY KEY)
- `coin_id` (VARCHAR) - CoinGecko coin identifier
- `name` (VARCHAR) - Coin name
- `symbol` (VARCHAR) - Coin symbol
- `current_price` (DECIMAL) - Current price in USD
- `market_cap` (BIGINT) - Market capitalization
- `notes` (TEXT) - User notes
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

## Features

✅ **Fetch coin data** from CoinGecko API by coin ID (bitcoin, ethereum, etc.)
✅ **Display coin info** - price, market cap, 24h change
✅ **Save to watchlist** - store coins in MySQL database
✅ **Update notes** - add/edit notes for saved coins
✅ **Delete coins** - remove coins from watchlist
✅ **Bootstrap UI** - clean, professional interface with GCSU branding

## How to Use

### 1. Run the App

```bash
source venv/bin/activate  # On Mac/Linux
# OR
venv\Scripts\activate     # On Windows

python app.py
```

### 2. Access the Crypto Tracker

Navigate to: `http://127.0.0.1:5000/crypto`

### 3. Fetch Cryptocurrency Data

- Enter a CoinGecko coin ID (e.g., `bitcoin`, `ethereum`, `cardano`, `solana`)
- Click "Fetch Data"
- View the coin's current price, market cap, and 24h change

### 4. Save to Watchlist

- After fetching, add optional notes
- Click "Save to Watchlist"
- Coin data is stored in your MySQL database

### 5. Manage Your Watchlist

- View all saved coins in the table
- Edit notes for any coin
- Delete coins you no longer want to track

## CoinGecko Coin IDs

Common coin IDs to try:
- bitcoin
- ethereum
- cardano
- solana
- polkadot
- ripple
- dogecoin
- avalanche-2
- polygon
- chainlink

Full list: https://api.coingecko.com/api/v3/coins/list

## Notes

- No API key required for CoinGecko free tier
- Database credentials loaded from `.env` file
- All templates in `app/templates/` (no subfolders)
- Minimal changes to existing starter code

## Branding

- Header: "MY NAME — Module 6"
- Navbar: Home | Crypto
- Footer: Professional GCSU branding

---

**Ready to go!** Visit `/crypto` to start tracking cryptocurrency prices.
