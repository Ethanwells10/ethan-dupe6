-- Cryptocurrency Watchlist Table
-- This table stores saved cryptocurrency data from CoinGecko API

CREATE TABLE IF NOT EXISTS watchlist (
    id INT AUTO_INCREMENT PRIMARY KEY,
    coin_id VARCHAR(64) NOT NULL,
    name VARCHAR(128),
    symbol VARCHAR(32),
    price DECIMAL(18, 6),
    market_cap BIGINT,
    note VARCHAR(255) DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for faster lookups by coin_id (optional - may fail if already exists)
-- CREATE INDEX idx_coin_id ON watchlist(coin_id);
