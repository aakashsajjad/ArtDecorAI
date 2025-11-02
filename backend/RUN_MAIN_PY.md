# How to Run main.py

## Quick Start

### Method 1: Direct Python Command (Easiest)

```bash
cd backend
python main.py
```

### Method 2: Using Python Module

```bash
cd backend
python -m main
```

### Method 3: Using Uvicorn Directly

```bash
cd backend
uvicorn main:app --reload
```

---

## What Happens When You Run main.py?

When you execute `python main.py`, it will:

1. ✅ Load environment variables from `.env` file
2. ✅ Initialize database connection
3. ✅ Start FastAPI server with Uvicorn
4. ✅ Server will be available at:
   - **Binding**: `0.0.0.0:8000` (listens on all interfaces)
   - **Access**: `http://localhost:8000` or `http://127.0.0.1:8000`

---

## Expected Output

When you run `python main.py`, you should see something like:

```
INFO:     Will watch for changes in these directories: ['C:\\...\\backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

## Access Your Server

After the server starts, open in your browser:

- 🌐 **Main Server**: http://localhost:8000
- 📚 **API Docs (Swagger)**: http://localhost:8000/docs
- 📖 **Alternative Docs (ReDoc)**: http://localhost:8000/redoc
- ❤️ **Health Check**: http://localhost:8000/health

---

## Test Your Endpoints

### Using Browser (Swagger UI)
1. Go to: http://localhost:8000/docs
2. You'll see all available endpoints
3. Click on any endpoint → "Try it out" → "Execute"

### Using curl
```bash
# Health check
curl http://localhost:8000/health

# Create sample artwork
curl -X POST http://localhost:8000/api/artworks/sample

# Get all artworks
curl http://localhost:8000/api/artworks/
```

---

## Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.

---

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'uvicorn'"

**Solution:**
```bash
pip install fastapi uvicorn
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

### Error: "Port 8000 already in use"

**Solution 1:** Stop the existing server
```bash
# Find process using port 8000
netstat -ano | findstr :8000
# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

**Solution 2:** Use a different port
```bash
python -m uvicorn main:app --reload --port 8001
```

Then access at: http://localhost:8001

### Error: "Database connection failed"

**Solution:**
1. Check if `backend/.env` file exists
2. Verify Supabase credentials are correct
3. Run `python check_config.py` to diagnose

The server will still start but will run in "standalone mode" without database.

---

## Complete Example

```bash
# 1. Navigate to backend directory
cd backend

# 2. Run the server
python main.py

# 3. Wait for "Application startup complete" message

# 4. Open browser to: http://localhost:8000/docs

# 5. Test endpoints using Swagger UI

# 6. Stop server with Ctrl+C
```

---

## Available Endpoints After Starting

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint |
| GET | `/health` | Health check |
| POST | `/api/artworks/` | Create artwork |
| POST | `/api/artworks/sample` | Create sample artwork |
| GET | `/api/artworks/` | Get all artworks |
| GET | `/api/artworks/{id}` | Get artwork by ID |
| GET | `/api/artworks/recent` | Get recent artworks |
| GET | `/api/artworks/stats/count` | Get artwork count |

---

## Development Mode

The server runs with `--reload` flag, which means:
- ✅ Automatically restarts when you change code
- ✅ Hot reload for faster development
- ✅ Great for development, not recommended for production

---

## Production Mode

For production, remove `--reload`:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## Summary

**To run**: `python main.py`  
**Access at**: `http://localhost:8000/docs`  
**Stop with**: `Ctrl+C`

That's it! 🚀


