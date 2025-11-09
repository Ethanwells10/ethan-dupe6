# Quick Start Guide

## 1. Start the Flask App

```bash
# Activate virtual environment
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate     # Windows

# Run the app
python app.py
```

You should see output like:
```
* Running on http://127.0.0.1:5000
```

## 2. Access the Application

Open your browser and go to one of these URLs:

### ✅ Available Routes:

- **Home Page**: `http://127.0.0.1:5000/`
- **Crypto Tracker**: `http://127.0.0.1:5000/crypto/`
- **About Page**: `http://127.0.0.1:5000/about`
- **Examples**: `http://127.0.0.1:5000/example/`

### 🎯 Main Feature (Module 6):

**Cryptocurrency Tracker**: http://127.0.0.1:5000/crypto/

## Troubleshooting

### "Not Found" Error?

1. **Make sure Flask is running** - You should see "Running on..." in your terminal
2. **Check the URL** - Must include `http://127.0.0.1:5000/`
3. **Try the crypto page directly**: http://127.0.0.1:5000/crypto/

### Database Connection Issues?

Make sure your `.env` file has the correct database credentials.

### Port Already in Use?

```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9  # Mac/Linux

# Then restart the app
python app.py
```

## Navigation

Once the app loads:
- Click **"Home"** in navbar to go to homepage
- Click **"Crypto"** in navbar to access the cryptocurrency tracker
