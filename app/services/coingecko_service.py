"""
CoinGecko API Service Layer
Provides a clean interface to fetch cryptocurrency data with caching and error handling.
"""

import requests
import os
import time
from typing import Optional, Dict

# Base URL for CoinGecko API
BASE_URL = "https://api.coingecko.com/api/v3"

# In-memory cache with TTL
_cache = {}
CACHE_TTL = 120  # 120 seconds (2 minutes)


class CoinGeckoService:
    """Service class for interacting with CoinGecko API"""

    @staticmethod
    def _get_headers() -> Dict[str, str]:
        """
        Build request headers, including API key if set
        Returns dict of headers
        """
        headers = {}
        api_key = os.getenv('COINGECKO_API_KEY')

        # Only add API key if it's set and not the placeholder
        if api_key and api_key != 'your_key_here':
            headers['x-cg-api-key'] = api_key

        return headers

    @staticmethod
    def _is_cache_valid(coin_id: str) -> bool:
        """
        Check if cached data exists and is still valid (not expired)
        """
        if coin_id not in _cache:
            return False

        cached_time = _cache[coin_id].get('timestamp', 0)
        return (time.time() - cached_time) < CACHE_TTL

    @staticmethod
    def _get_from_cache(coin_id: str) -> Optional[Dict]:
        """
        Retrieve data from cache if valid
        """
        if CoinGeckoService._is_cache_valid(coin_id):
            return _cache[coin_id]['data']
        return None

    @staticmethod
    def _save_to_cache(coin_id: str, data: Dict):
        """
        Save data to cache with current timestamp
        """
        _cache[coin_id] = {
            'data': data,
            'timestamp': time.time()
        }

    @staticmethod
    def fetch_coin(coin_id: str) -> tuple[Optional[Dict], Optional[str]]:
        """
        Fetch cryptocurrency data from CoinGecko API

        Args:
            coin_id: CoinGecko coin identifier (e.g., 'bitcoin', 'ethereum')

        Returns:
            Tuple of (data_dict, error_message)
            - If successful: (data, None)
            - If error: (None, error_message)
        """

        # Check cache first
        cached_data = CoinGeckoService._get_from_cache(coin_id)
        if cached_data:
            return cached_data, None

        # Build request
        url = f"{BASE_URL}/coins/{coin_id}"
        params = {
            'market_data': 'true',
            'localization': 'false',
            'tickers': 'false',
            'sparkline': 'false'
        }
        headers = CoinGeckoService._get_headers()

        try:
            # Make API request
            response = requests.get(url, params=params, headers=headers, timeout=10)

            # Handle 404 - coin not found
            if response.status_code == 404:
                return None, f'Coin "{coin_id}" not found. Try bitcoin, ethereum, cardano, etc.'

            # Handle other error status codes
            if response.status_code != 200:
                return None, f'API error: Unable to fetch data (Status {response.status_code})'

            # Parse response
            data = response.json()

            # Extract only the fields we need
            coin_data = {
                'coin_id': data.get('id'),
                'name': data.get('name'),
                'symbol': data.get('symbol', '').upper(),
                'price': data.get('market_data', {}).get('current_price', {}).get('usd', 0),
                'market_cap': data.get('market_data', {}).get('market_cap', {}).get('usd', 0),
                # Bonus: Include image and 24h change for display
                'image': data.get('image', {}).get('small', ''),
                'price_change_24h': data.get('market_data', {}).get('price_change_percentage_24h', 0)
            }

            # Cache the result
            CoinGeckoService._save_to_cache(coin_id, coin_data)

            return coin_data, None

        except requests.exceptions.Timeout:
            return None, 'Request timed out. Please try again.'

        except requests.exceptions.ConnectionError:
            return None, 'Network error. Please check your internet connection.'

        except requests.exceptions.RequestException as e:
            return None, f'API request failed: {str(e)}'

        except ValueError:  # JSON decode error
            return None, 'Invalid response from API. Please try again.'

        except Exception as e:
            return None, f'Unexpected error: {str(e)}'

    @staticmethod
    def clear_cache():
        """Clear all cached data (useful for testing)"""
        _cache.clear()

    @staticmethod
    def fetch_top_coins_by_volume(limit: int = 10) -> tuple[Optional[list], Optional[str]]:
        """
        Fetch top cryptocurrencies by trading volume

        Args:
            limit: Number of coins to return (default: 10)

        Returns:
            Tuple of (list_of_coins, error_message)
            - If successful: (coins_list, None)
            - If error: (None, error_message)
        """

        # Check cache first
        cache_key = f'top_volume_{limit}'
        cached_data = CoinGeckoService._get_from_cache(cache_key)
        if cached_data:
            return cached_data, None

        # Build request
        url = f"{BASE_URL}/coins/markets"
        params = {
            'vs_currency': 'usd',
            'order': 'volume_desc',
            'per_page': limit,
            'page': 1,
            'sparkline': 'false',
            'locale': 'en'
        }
        headers = CoinGeckoService._get_headers()

        try:
            # Make API request
            response = requests.get(url, params=params, headers=headers, timeout=10)

            # Handle error status codes
            if response.status_code != 200:
                return None, f'API error: Unable to fetch top coins (Status {response.status_code})'

            # Parse response
            data = response.json()

            # Extract data for each coin
            coins_list = []
            for coin in data:
                coin_info = {
                    'rank': coin.get('market_cap_rank', 0),
                    'coin_id': coin.get('id'),
                    'name': coin.get('name'),
                    'symbol': coin.get('symbol', '').upper(),
                    'price': coin.get('current_price', 0),
                    'market_cap': coin.get('market_cap', 0),
                    'volume_24h': coin.get('total_volume', 0),
                    'price_change_24h': coin.get('price_change_percentage_24h', 0),
                    'image': coin.get('image', '')
                }
                coins_list.append(coin_info)

            # Cache the result
            CoinGeckoService._save_to_cache(cache_key, coins_list)

            return coins_list, None

        except requests.exceptions.Timeout:
            return None, 'Request timed out. Please try again.'

        except requests.exceptions.ConnectionError:
            return None, 'Network error. Please check your internet connection.'

        except requests.exceptions.RequestException as e:
            return None, f'API request failed: {str(e)}'

        except ValueError:  # JSON decode error
            return None, 'Invalid response from API. Please try again.'

        except Exception as e:
            return None, f'Unexpected error: {str(e)}'

    @staticmethod
    def fetch_global_data() -> tuple[Optional[Dict], Optional[str]]:
        """
        Fetch global cryptocurrency market data

        Returns:
            Tuple of (global_data_dict, error_message)
            - If successful: (data, None)
            - If error: (None, error_message)
        """

        # Check cache first
        cache_key = 'global_market_data'
        cached_data = CoinGeckoService._get_from_cache(cache_key)
        if cached_data:
            return cached_data, None

        # Build request
        url = f"{BASE_URL}/global"
        headers = CoinGeckoService._get_headers()

        try:
            # Make API request
            response = requests.get(url, headers=headers, timeout=10)

            # Handle error status codes
            if response.status_code != 200:
                return None, f'API error: Unable to fetch global data (Status {response.status_code})'

            # Parse response
            data = response.json()
            global_data = data.get('data', {})

            # Extract key metrics
            market_data = {
                'total_market_cap': global_data.get('total_market_cap', {}).get('usd', 0),
                'total_volume_24h': global_data.get('total_volume', {}).get('usd', 0),
                'market_cap_change_24h': global_data.get('market_cap_change_percentage_24h_usd', 0),
                'active_cryptocurrencies': global_data.get('active_cryptocurrencies', 0),
                'markets': global_data.get('markets', 0),
                'btc_dominance': global_data.get('market_cap_percentage', {}).get('btc', 0),
                'eth_dominance': global_data.get('market_cap_percentage', {}).get('eth', 0)
            }

            # Cache the result
            CoinGeckoService._save_to_cache(cache_key, market_data)

            return market_data, None

        except requests.exceptions.Timeout:
            return None, 'Request timed out. Please try again.'

        except requests.exceptions.ConnectionError:
            return None, 'Network error. Please check your internet connection.'

        except requests.exceptions.RequestException as e:
            return None, f'API request failed: {str(e)}'

        except ValueError:  # JSON decode error
            return None, 'Invalid response from API. Please try again.'

        except Exception as e:
            return None, f'Unexpected error: {str(e)}'

    @staticmethod
    def get_cache_info() -> Dict:
        """Get cache statistics (useful for debugging)"""
        return {
            'cached_coins': list(_cache.keys()),
            'cache_size': len(_cache),
            'ttl_seconds': CACHE_TTL
        }
