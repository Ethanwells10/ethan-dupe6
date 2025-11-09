#!/bin/bash
# Heroku Config Vars Setup Script
# Run this to configure all environment variables in Heroku

echo "=== Setting Heroku Config Vars ==="

# Make sure you're logged in to Heroku first
# Run: heroku login

# Set database configuration
heroku config:set DB_HOST=bmsyhziszmhf61g1.cbetxkdyhwsb.us-east-1.rds.amazonaws.com
heroku config:set DB_USER=c936k0s59gjf2gul
heroku config:set DB_PASSWORD=r8asisqkuxx5fzvh
heroku config:set DB_PORT=3306
heroku config:set DB_NAME=mlt6f8vuctglmgem

# Set CoinGecko API configuration
heroku config:set COINGECKO_API_KEY=your_key_here
heroku config:set DEFAULT_VS=usd

echo ""
echo "=== Verify Config Vars ==="
heroku config

echo ""
echo "Done! Your Heroku app is configured."
echo "Remember to replace 'your_key_here' with your actual CoinGecko API key if needed."
