# How to Run FastAPI Server

## Quick Start

### Method 1: Using Batch File (Windows - Easiest)

```bash
cd backend
run_fastapi.bat
```

### Method 2: Using Python Script

```bash
cd backend
python run_fastapi.py
```

### Method 3: Using Uvicorn Directly

```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Method 4: Using Python Directly

```bash
cd backend
python main.py
```

---

## What Gets Started?

Once the server starts, you'll have access to:

- **API Server**: http://localhost:8000
- **Interactive API Docs (Swagger)**: http://localhost:8000/docs
- **Alternative Docs (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## Test the New Endpoints

### 1. Create Sample Artwork (New Endpoint!)

**Using Browser:**
- Go to: http://localhost:8000/docs
- Find `POST /api/artworks/sample`
- Click "Try it out" → "Execute"

**Using curl:**
```bash
curl -X POST "http://localhost:8000/api/artworks/sample"
```

**Using Python:**
```python
import requests

response = requests.post("http://localhost:8000/api/artworks/sample")
print(response.json())
```

**Expected Response:**
```json
{
  "message": "Sample record added successfully",
  "artwork_id": "123"
}
```

---

### 2. Create Custom Artwork (Standard Endpoint)

**Using Browser (Swagger UI):**
1. Go to: http://localhost:8000/docs
2. Find `POST /api/artworks/`
3. Click "Try it out"
4. Enter JSON in the request body:
```json
{
  "title": "My Beautiful Art",
  "brand": "My Gallery",
  "price": 199.99,
  "style_tags": ["modern", "abstract"],
  "dominant_palette": {
    "primary": "#3498db",
    "secondary": "#e74c3c"
  },
  "image_url": "https://example.com/art.jpg"
}
```
5. Click "Execute"

**Using curl:**
```bash
curl -X POST "http://localhost:8000/api/artworks/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Beautiful Art",
    "brand": "My Gallery",
    "price": 199.99,
    "style_tags": ["modern", "abstract"],
    "image_url": "https://example.com/art.jpg"
  }'
```

---

## Available Endpoints

### Artwork Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/artworks/` | Create new artwork |
| `POST` | `/api/artworks/sample` | Create sample artwork (NEW!) |
| `GET` | `/api/artworks/` | Get all artworks (paginated) |
| `GET` | `/api/artworks/{id}` | Get artwork by ID |
| `PUT` | `/api/artworks/{id}` | Update artwork |
| `DELETE` | `/api/artworks/{id}` | Delete artwork |
| `POST` | `/api/artworks/search` | Search artworks |
| `GET` | `/api/artworks/recent` | Get recent artworks |
| `GET` | `/api/artworks/stats/count` | Get artwork count |

### Utility Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Root endpoint |
| `GET` | `/health` | Health check |

---

## Prerequisites

Make sure you have:

1. **Python 3.8+** installed
2. **Dependencies** installed:
   ```bash
   pip install -r requirements.txt
   ```

   Or install individually:
   ```bash
   pip install fastapi uvicorn supabase python-dotenv pydantic
   ```

3. **Environment variables** configured:
   - `backend/.env` file with Supabase credentials
   - Or use Service Role Key to bypass RLS

---

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'uvicorn'"

**Solution:**
```bash
pip install uvicorn fastapi
```

### Error: "Port 8000 already in use"

**Solution 1:** Stop the existing server (Ctrl+C)

**Solution 2:** Use a different port:
```bash
python -m uvicorn main:app --reload --port 8001
```

### Error: "Database connection failed"

**Solution:** 
1. Check your `backend/.env` file has correct Supabase credentials
2. Run `python check_config.py` to verify configuration
3. See `FIX_NOW.md` for help with API keys

### Error: "new row violates row-level security policy"

**Solution:**
1. Add RLS policies in Supabase (see `COPY_THIS_SQL.sql`)
2. Or use Service Role Key in `backend/.env`

---

## Testing with Swagger UI

The easiest way to test endpoints is using Swagger UI:

1. Start the server
2. Open: http://localhost:8000/docs
3. You'll see all available endpoints
4. Click on any endpoint
5. Click "Try it out"
6. Fill in parameters/body
7. Click "Execute"
8. See the response!

---

## Example: Complete Workflow

```bash
# 1. Start server
cd backend
run_fastapi.bat

# 2. In another terminal, test the endpoint
curl -X POST http://localhost:8000/api/artworks/sample

# 3. Or open browser to:
# http://localhost:8000/docs

# 4. Test creating custom artwork
curl -X POST http://localhost:8000/api/artworks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Art", "price": 99.99}'

# 5. Get all artworks
curl http://localhost:8000/api/artworks/
```

---

## Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.

---

## Production Deployment

For production, use:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

Or use a process manager like:
- **Gunicorn** (with Uvicorn workers)
- **PM2** (for Node.js-like process management)
- **systemd** (Linux services)
- **Docker** (containerization)


