# Nepal Traffic Intelligence - Railway + Vercel Deployment Guide

## Backend Deployment (Railway)

### Step 1: Prepare Backend
Create a `Procfile` in your project root:
```
web: uvicorn backend.api.main:app --host 0.0.0.0 --port $PORT
```

### Step 2: Railway Setup
1. Create Railway account
2. Connect your GitHub repo
3. Add a new "Python" service
4. Configure environment variables if needed
5. Deploy!

## Frontend Deployment (Vercel)

### Step 1: Prepare Frontend
Create `frontend/.env.production`:
```
VITE_API_URL=https://your-railway-backend.railway.app
```

### Step 2: Update Frontend API URL
In `frontend/src/App.jsx`, use environment variable:
```javascript
const API_URL = import.meta.env.VITE_API_URL + '/traffic/live';
const HISTORY_URL = import.meta.env.VITE_API_URL + '/traffic/history';
const STREAM_URL = import.meta.env.VITE_API_URL + '/traffic/stream';
```

### Step 3: Vercel Setup
1. Create Vercel account
2. Connect your GitHub repo
3. Configure root directory to `frontend`
4. Set environment variable `VITE_API_URL` to your Railway backend URL
5. Deploy!
