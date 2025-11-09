from flask import render_template, redirect, url_for, flash
from . import app
from app.services.coingecko_service import CoinGeckoService

@app.route('/')
def index():
    # Fetch global market data
    global_data, error = CoinGeckoService.fetch_global_data()

    if error:
        global_data = None

    return render_template('index.html', global_data=global_data)

@app.route('/refresh-global-data')
def refresh_global_data():
    # Clear the global data from cache
    CoinGeckoService.clear_cache()
    flash('Market data refreshed successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')
