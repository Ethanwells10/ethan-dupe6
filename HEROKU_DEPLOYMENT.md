# Heroku Deployment Guide - Module 6 Crypto Tracker

## Prerequisites

1. **Heroku Account** - Sign up at https://heroku.com
2. **Heroku CLI** - Install from https://devcenter.heroku.com/articles/heroku-cli
3. **Git** - Already initialized in this project

## Step 1: Login to Heroku

```bash
heroku login
```

This will open your browser to authenticate.

## Step 2: Create Heroku App (if not already created)

```bash
# Create new app
heroku create your-app-name

# OR connect to existing app
heroku git:remote -a your-existing-app-name
```

## Step 3: Configure Environment Variables

### Option A: Using Heroku Dashboard (Recommended for Beginners)

1. Go to https://dashboard.heroku.com/apps
2. Select your app
3. Click **Settings** tab
4. Scroll to **Config Vars**
5. Click **Reveal Config Vars**
6. Add each variable (see table below)

### Option B: Using Heroku CLI

Run the provided script:

```bash
bash heroku_setup.sh
```

OR manually set each variable:

```bash
heroku config:set DB_HOST=bmsyhziszmhf61g1.cbetxkdyhwsb.us-east-1.rds.amazonaws.com
heroku config:set DB_USER=c936k0s59gjf2gul
heroku config:set DB_PASSWORD=r8asisqkuxx5fzvh
heroku config:set DB_PORT=3306
heroku config:set DB_NAME=mlt6f8vuctglmgem
heroku config:set COINGECKO_API_KEY=your_key_here
heroku config:set DEFAULT_VS=usd
```

### Config Vars Table

| Config Var | Value |
|------------|-------|
| `DB_HOST` | `bmsyhziszmhf61g1.cbetxkdyhwsb.us-east-1.rds.amazonaws.com` |
| `DB_USER` | `c936k0s59gjf2gul` |
| `DB_PASSWORD` | `r8asisqkuxx5fzvh` |
| `DB_PORT` | `3306` |
| `DB_NAME` | `mlt6f8vuctglmgem` |
| `COINGECKO_API_KEY` | `your_key_here` (or your actual CoinGecko API key) |
| `DEFAULT_VS` | `usd` |

## Step 4: Verify Configuration

```bash
heroku config
```

You should see all your environment variables listed (password values will be hidden).

## Step 5: Deploy to Heroku

```bash
# Add all changes to git
git add .

# Commit changes
git commit -m "Ready for Heroku deployment - Module 6"

# Push to Heroku
git push heroku master
```

## Step 6: Run Database Setup on Heroku

```bash
# Run the database setup script on Heroku
heroku run python database/setup_crypto_db.py
```

This creates the `watchlist` table in your MySQL database.

## Step 7: Open Your App

```bash
heroku open
```

Your app will open at: `https://your-app-name.herokuapp.com`

Navigate to `/crypto/` to access the cryptocurrency tracker.

## Useful Heroku Commands

```bash
# View logs
heroku logs --tail

# Restart app
heroku restart

# Check app status
heroku ps

# Run Python shell on Heroku
heroku run python

# View config vars
heroku config

# Update a single config var
heroku config:set COINGECKO_API_KEY=CG-new-key-here
```

## Troubleshooting

### App crashes on Heroku?
```bash
heroku logs --tail
```
Check for errors in the logs.

### Database connection failed?
Verify your JawsDB config vars match your `.env` file.

### Config vars not updating?
After changing config vars, restart the app:
```bash
heroku restart
```

### Port binding error?
Heroku assigns the port dynamically. The app should use `PORT` from environment:
```python
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

## Important Notes

- ✅ `.env` file is in `.gitignore` (never committed)
- ✅ Use Heroku Config Vars instead of `.env` in production
- ✅ Config Vars are injected as environment variables
- ✅ Your app reads them the same way using `os.getenv()`

## Your App URLs

- **Local Development**: `http://127.0.0.1:5000/crypto/`
- **Heroku Production**: `https://your-app-name.herokuapp.com/crypto/`

---

**Questions?** Check Heroku docs: https://devcenter.heroku.com/articles/config-vars
