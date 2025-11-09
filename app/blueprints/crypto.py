from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db_connect import get_db
from app.services.coingecko_service import CoinGeckoService

crypto = Blueprint('crypto', __name__)

@crypto.route('/', methods=['GET', 'POST'])
def crypto_tracker():
    db = get_db()
    cursor = db.cursor()

    # Initialize variables for fetched coin data
    coin_data = None

    # Handle POST request to fetch coin data from CoinGecko API
    if request.method == 'POST':
        # Check if this is a fetch request or save request
        if 'fetch_coin' in request.form:
            coin_id = request.form.get('coin_id', '').strip().lower()

            if coin_id:
                # Use the service layer to fetch coin data
                data, error = CoinGeckoService.fetch_coin(coin_id)

                if error:
                    # Handle error with friendly flash message
                    flash(error, 'danger')
                else:
                    # Success - prepare data for display
                    coin_data = {
                        'id': data['coin_id'],
                        'name': data['name'],
                        'symbol': data['symbol'],
                        'price': data['price'],
                        'market_cap': data['market_cap'],
                        'price_change_24h': data.get('price_change_24h', 0),
                        'image': data.get('image', '')
                    }
                    flash(f'Successfully fetched data for {coin_data["name"]}!', 'success')
            else:
                flash('Please enter a coin ID.', 'danger')

        # Handle save to watchlist
        elif 'save_coin' in request.form:
            coin_id = request.form['coin_id']
            name = request.form['name']
            symbol = request.form['symbol']
            price = request.form['price']
            market_cap = request.form['market_cap']
            note = request.form.get('note', '')

            # Insert into watchlist table
            cursor.execute(
                'INSERT INTO watchlist (coin_id, name, symbol, price, market_cap, note) VALUES (%s, %s, %s, %s, %s, %s)',
                (coin_id, name, symbol, price, market_cap, note)
            )
            db.commit()
            flash(f'{name} added to watchlist!', 'success')
            return redirect(url_for('crypto.crypto_tracker'))

    # Fetch all saved coins from watchlist
    cursor.execute('SELECT * FROM watchlist ORDER BY created_at DESC')
    watchlist = cursor.fetchall()

    return render_template('crypto.html', coin_data=coin_data, watchlist=watchlist)

@crypto.route('/update/<int:id>', methods=['POST'])
def update_note(id):
    db = get_db()
    cursor = db.cursor()

    note = request.form['note']

    cursor.execute('UPDATE watchlist SET note = %s WHERE id = %s', (note, id))
    db.commit()

    flash('Note updated successfully!', 'success')

    # Redirect to the page the user came from
    if 'watchlist' in request.referrer:
        return redirect(url_for('crypto.watchlist_page'))
    return redirect(url_for('crypto.crypto_tracker'))

@crypto.route('/watchlist')
def watchlist_page():
    db = get_db()
    cursor = db.cursor()

    # Fetch all saved coins from watchlist
    cursor.execute('SELECT * FROM watchlist ORDER BY created_at DESC')
    watchlist = cursor.fetchall()

    return render_template('watchlist.html', watchlist=watchlist)

@crypto.route('/top-coins')
def top_coins():
    # Fetch top 10 coins by volume using service layer
    coins, error = CoinGeckoService.fetch_top_coins_by_volume(limit=10)

    if error:
        flash(error, 'danger')
        coins = []

    return render_template('top_coins.html', coins=coins)

@crypto.route('/view/<int:id>')
def view_coin(id):
    db = get_db()
    cursor = db.cursor()

    # Fetch saved coin from database
    cursor.execute('SELECT * FROM watchlist WHERE id = %s', (id,))
    saved_coin = cursor.fetchone()

    if not saved_coin:
        flash('Coin not found in watchlist!', 'danger')
        return redirect(url_for('crypto.watchlist_page'))

    # Fetch current live data from CoinGecko API
    live_data, error = CoinGeckoService.fetch_coin(saved_coin['coin_id'])

    if error:
        # If API fails, show saved data only
        flash(f'Could not fetch live data: {error}', 'warning')
        live_data = None

    return render_template('view_coin.html', saved_coin=saved_coin, live_data=live_data)

@crypto.route('/refresh/<int:id>')
def refresh_coin(id):
    db = get_db()
    cursor = db.cursor()

    # Fetch the saved coin from database
    cursor.execute('SELECT * FROM watchlist WHERE id = %s', (id,))
    saved_coin = cursor.fetchone()

    if not saved_coin:
        flash('Coin not found in watchlist!', 'danger')
        return redirect(url_for('crypto.watchlist_page'))

    # Fetch fresh data from CoinGecko API
    live_data, error = CoinGeckoService.fetch_coin(saved_coin['coin_id'])

    if error:
        flash(f'Could not refresh {saved_coin["name"]}: {error}', 'danger')
    else:
        # Update the price and market cap in the database
        cursor.execute(
            'UPDATE watchlist SET price = %s, market_cap = %s WHERE id = %s',
            (live_data['price'], live_data['market_cap'], id)
        )
        db.commit()
        flash(f'{saved_coin["name"]} refreshed successfully!', 'success')

    # Redirect to the page the user came from
    if request.referrer and 'watchlist' in request.referrer:
        return redirect(url_for('crypto.watchlist_page'))
    elif request.referrer and 'view' in request.referrer:
        return redirect(url_for('crypto.view_coin', id=id))
    return redirect(url_for('crypto.crypto_tracker'))

@crypto.route('/delete/<int:id>', methods=['POST'])
def delete_coin(id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute('DELETE FROM watchlist WHERE id = %s', (id,))
    db.commit()

    flash('Coin removed from watchlist!', 'danger')

    # Redirect to the page the user came from
    if 'watchlist' in request.referrer:
        return redirect(url_for('crypto.watchlist_page'))
    return redirect(url_for('crypto.crypto_tracker'))
