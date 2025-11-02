# Understanding the Server URL: 0.0.0.0 vs localhost

## What is `0.0.0.0`?

When you see `http://0.0.0.0:8000`, this means:
- **The server is listening on ALL network interfaces**
- This allows the server to accept connections from:
  - Localhost (127.0.0.1)
  - Your local IP address
  - Other devices on your network
  - Docker containers (if applicable)

## How to Access the Server

### ❌ DON'T use this:
```
http://0.0.0.0:8000  ← This won't work in a browser!
```

### ✅ DO use one of these:

1. **localhost** (recommended for local access):
   ```
   http://localhost:8000
   ```

2. **127.0.0.1** (same as localhost):
   ```
   http://127.0.0.1:8000
   ```

3. **Your computer's IP address** (for network access):
   ```
   http://192.168.1.XXX:8000  ← Replace with your actual IP
   ```

---

## Quick Access Links

After starting the server, use these URLs:

### 🌐 Main Server
- http://localhost:8000
- http://localhost:8000/health

### 📚 API Documentation
- http://localhost:8000/docs (Swagger UI - Interactive)
- http://localhost:8000/redoc (ReDoc - Alternative docs)

### 🎨 Artwork Endpoints
- http://localhost:8000/api/artworks/ (GET all artworks)
- http://localhost:8000/api/artworks/sample (POST - Create sample)
- http://localhost:8000/api/artworks/{id} (GET specific artwork)

---

## Understanding Host Binding

### `host="0.0.0.0"` (Current Setting)
- ✅ Accepts connections from anywhere
- ✅ Works with localhost, 127.0.0.1, and your IP
- ✅ Good for development and testing
- ⚠️ Accessible from other devices on your network

### `host="127.0.0.1"` or `host="localhost"` (Alternative)
- ✅ Only accepts local connections
- ✅ More secure (only accessible from your computer)
- ❌ Cannot be accessed from other devices
- ❌ May not work with Docker

---

## Testing Your Server

### In Browser:
```
http://localhost:8000/docs
```

### Using curl:
```bash
curl http://localhost:8000/health
curl -X POST http://localhost:8000/api/artworks/sample
```

### Using Python:
```python
import requests

# Test health endpoint
response = requests.get("http://localhost:8000/health")
print(response.json())

# Test sample artwork creation
response = requests.post("http://localhost:8000/api/artworks/sample")
print(response.json())
```

---

## Summary

- **`0.0.0.0`** = Server listens on all interfaces (good for development)
- **`localhost`** or **`127.0.0.1`** = Use these to access the server in your browser
- The server is running correctly if you can access `http://localhost:8000/docs`

**Always use `localhost` or `127.0.0.1` when accessing the server, NOT `0.0.0.0`!**


