"""
Database setup script for Cryptocurrency Watchlist
Run this script to create the watchlist table in your MySQL database
"""

import pymysql
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_watchlist_table():
    """Creates the watchlist table in the database"""

    try:
        # Connect to database
        connection = pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            cursorclass=pymysql.cursors.DictCursor
        )

        print("Connected to database successfully!")

        cursor = connection.cursor()

        # Create watchlist table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS watchlist (
            id INT AUTO_INCREMENT PRIMARY KEY,
            coin_id VARCHAR(64) NOT NULL,
            name VARCHAR(128),
            symbol VARCHAR(32),
            price DECIMAL(18, 6),
            market_cap BIGINT,
            note VARCHAR(255) DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """

        cursor.execute(create_table_query)
        print("✓ Watchlist table created successfully!")

        # Create index for faster lookups (ignore if already exists)
        try:
            index_query = """
            CREATE INDEX idx_coin_id ON watchlist(coin_id)
            """
            cursor.execute(index_query)
            print("✓ Index created on coin_id column!")
        except pymysql.err.OperationalError as e:
            if "Duplicate key name" in str(e):
                print("✓ Index already exists on coin_id column!")
            else:
                raise

        connection.commit()
        print("\nDatabase setup complete! You can now run your Flask app.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection:
            connection.close()
            print("Database connection closed.")

if __name__ == "__main__":
    print("Setting up Cryptocurrency Watchlist database...\n")
    create_watchlist_table()
