# CoinGecko Service Layer Documentation

## Overview

The `CoinGeckoService` provides a clean, cached interface to the CoinGecko API with built-in error handling and rate limit protection.

## Location

`app/services/coingecko_service.py`

## Features

### ✅ API Configuration
- **Base URL**: `https://api.coingecko.com/api/v3`
- **API Key Support**: Automatically includes `x-cg-api-key` header if `COINGECKO_API_KEY` is set in `.env`
- **Parameters**: Uses optimized parameters (`market_data=true`, `localization=false`, `tickers=false`, `sparkline=false`)

### ✅ In-Memory Caching
- **TTL**: 120 seconds (2 minutes)
- **Purpose**: Prevents rate limiting and improves performance
- **Behavior**: Returns cached data if available and not expired

### ✅ Error Handling
Gracefully handles:
- **404 errors**: "Coin not found" with helpful message
- **Network errors**: Connection failures and timeouts
- **API errors**: Non-200 status codes
- **Invalid responses**: JSON parsing errors

### ✅ Data Extraction
Returns only essential fields:
- `coin_id` - CoinGecko identifier
- `name` - Coin name
- `symbol` - Symbol (uppercase)
- `price` - Current price in USD
- `market_cap` - Market capitalization in USD
- `image` (bonus) - Small coin image URL
- `price_change_24h` (bonus) - 24-hour price change percentage

## Usage

### Basic Usage

```python
from app.services.coingecko_service import CoinGeckoService

# Fetch coin data
data, error = CoinGeckoService.fetch_coin('bitcoin')

if error:
    # Handle error
    flash(error, 'danger')
else:
    # Use data
    print(f"Price: ${data['price']}")
    print(f"Market Cap: ${data['market_cap']}")
```

### In Your Blueprint

```python
from app.services.coingecko_service import CoinGeckoService

@app.route('/crypto', methods=['POST'])
def crypto_tracker():
    coin_id = request.form.get('coin_id')

    # Fetch with service layer
    data, error = CoinGeckoService.fetch_coin(coin_id)

    if error:
        flash(error, 'danger')
        return redirect(url_for('crypto_tracker'))

    # Success - use data
    return render_template('crypto.html', coin_data=data)
```

### Cache Management

```python
# Get cache statistics
info = CoinGeckoService.get_cache_info()
print(f"Cached coins: {info['cached_coins']}")
print(f"Cache size: {info['cache_size']}")

# Clear cache (useful for testing)
CoinGeckoService.clear_cache()
```

## Return Format

### Success Response
```python
data = {
    'coin_id': 'bitcoin',
    'name': 'Bitcoin',
    'symbol': 'BTC',
    'price': 103644.00,
    'market_cap': 2066505386828,
    'image': 'https://...',
    'price_change_24h': 2.5
}
error = None
```

### Error Response
```python
data = None
error = "Coin 'fakecoin' not found. Try bitcoin, ethereum, cardano, etc."
```

## Cache Behavior

### First Request
```
User requests 'bitcoin'
  → API call to CoinGecko (~500ms)
  → Cache result
  → Return data
```

### Subsequent Request (within TTL)
```
User requests 'bitcoin' again
  → Check cache (valid)
  → Return cached data (~0ms)
```

### After TTL Expires
```
User requests 'bitcoin' after 2 minutes
  → Check cache (expired)
  → API call to CoinGecko (~500ms)
  → Update cache
  → Return data
```

## Error Messages

| Error Type | User-Friendly Message |
|------------|----------------------|
| 404 Not Found | `Coin "xyz" not found. Try bitcoin, ethereum, cardano, etc.` |
| Timeout | `Request timed out. Please try again.` |
| Network Error | `Network error. Please check your internet connection.` |
| Other API Error | `API error: Unable to fetch data (Status XXX)` |
| Invalid JSON | `Invalid response from API. Please try again.` |
| Unexpected | `Unexpected error: [details]` |

## Configuration

### Environment Variables

In `.env`:
```bash
# Optional - only needed for higher rate limits
COINGECKO_API_KEY=CG-your-api-key-here

# Optional - default is 'usd'
DEFAULT_VS=usd
```

### Cache TTL

Modify in `coingecko_service.py`:
```python
CACHE_TTL = 120  # seconds (60-300 recommended)
```

## Benefits

1. **Rate Limit Protection**: Caching prevents excessive API calls
2. **Improved Performance**: Cached responses are instant
3. **Clean Separation**: Business logic separated from API details
4. **Error Handling**: Graceful degradation with user-friendly messages
5. **Easy Testing**: Service can be mocked in tests
6. **Maintainability**: Changes to API only affect service layer

## Testing

```bash
python -c "from app.services.coingecko_service import CoinGeckoService; \
data, error = CoinGeckoService.fetch_coin('bitcoin'); \
print(f'Success: {data[\"name\"]}' if not error else f'Error: {error}')"
```

---

**Service layer meets all Segment E requirements:** ✅
- Wraps CoinGecko API calls
- Uses correct base URL
- Adds API key header conditionally
- In-memory cache with 120s TTL
- Returns only needed fields
- Handles 404 and network errors gracefully
- Surfaces friendly flash messages
