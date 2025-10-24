# How to Run Artwork CRUD Operations

This guide shows you how to run the Python CRUD operations for the artwork table in the ArtDecorAI project.

## 🚀 Quick Start (Recommended)

### Method 1: Direct CRUD Demo (No Database Required)

This is the easiest way to see all CRUD operations in action:

```bash
# Navigate to backend directory
cd backend

# Run the direct CRUD demo
python direct_crud_demo.py
```

**What this does:**
- ✅ Creates sample artworks
- ✅ Demonstrates all CRUD operations
- ✅ Shows search and filtering
- ✅ Works without any database setup

### Method 2: FastAPI Server (REST API)

Run the complete FastAPI server with REST endpoints:

```bash
# Navigate to backend directory
cd backend

# Install dependencies (if not already done)
pip install -r requirements.txt

# Start the FastAPI server
python main.py
```

**Access the API:**
- 🌐 API Server: http://localhost:8000
- 📚 API Documentation: http://localhost:8000/docs
- 🔄 Alternative Docs: http://localhost:8000/redoc

## 📋 CRUD Operations Available

### 1. CREATE Operations
```python
# Create new artwork
POST /api/artworks/
{
    "title": "Modern Abstract Waves",
    "brand": "Contemporary Gallery",
    "price": 299.99,
    "style_tags": ["abstract", "modern", "blue"],
    "dominant_palette": {
        "primary": "#1e3a8a",
        "secondary": "#3b82f6"
    },
    "image_url": "https://example.com/artwork1.jpg"
}
```

### 2. READ Operations
```python
# Get artwork by ID
GET /api/artworks/{id}

# Get all artworks (paginated)
GET /api/artworks/?limit=10&offset=0

# Get recent artworks
GET /api/artworks/recent?limit=5

# Count total artworks
GET /api/artworks/stats/count
```

### 3. UPDATE Operations
```python
# Update artwork
PUT /api/artworks/{id}
{
    "price": 349.99,
    "style_tags": ["abstract", "modern", "blue", "contemporary"]
}
```

### 4. DELETE Operations
```python
# Delete artwork
DELETE /api/artworks/{id}
```

### 5. SEARCH Operations
```python
# Search with filters
POST /api/artworks/search
{
    "style_tags": ["abstract", "modern"],
    "min_price": 100.00,
    "max_price": 500.00,
    "limit": 10
}

# Search by style
GET /api/artworks/search/style?style_tags=abstract&style_tags=modern

# Search by price range
GET /api/artworks/search/price?min_price=100&max_price=500

# Search by brand
GET /api/artworks/search/brand?brand=Contemporary
```

## 🛠️ Testing the API

### Using curl (Command Line)

```bash
# Create artwork
curl -X POST "http://localhost:8000/api/artworks/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Artwork",
    "brand": "Test Gallery",
    "price": 199.99,
    "style_tags": ["abstract", "modern"]
  }'

# Get all artworks
curl -X GET "http://localhost:8000/api/artworks/"

# Get artwork by ID (replace {id} with actual ID)
curl -X GET "http://localhost:8000/api/artworks/{id}"

# Update artwork
curl -X PUT "http://localhost:8000/api/artworks/{id}" \
  -H "Content-Type: application/json" \
  -d '{"price": 249.99}'

# Delete artwork
curl -X DELETE "http://localhost:8000/api/artworks/{id}"
```

### Using Python requests

```python
import requests
import json

# Base URL
base_url = "http://localhost:8000"

# Create artwork
artwork_data = {
    "title": "Python Test Artwork",
    "brand": "Python Gallery",
    "price": 299.99,
    "style_tags": ["python", "test", "demo"]
}

response = requests.post(f"{base_url}/api/artworks/", json=artwork_data)
print(f"Created artwork: {response.json()}")

# Get all artworks
response = requests.get(f"{base_url}/api/artworks/")
print(f"All artworks: {response.json()}")

# Search artworks
search_data = {
    "style_tags": ["python", "test"],
    "min_price": 200.00,
    "max_price": 400.00
}

response = requests.post(f"{base_url}/api/artworks/search", json=search_data)
print(f"Search results: {response.json()}")
```

## 🔧 Advanced Usage

### Custom CRUD Operations

You can also use the CRUD classes directly in your Python code:

```python
from crud.artwork_crud import artwork_crud
from models.artwork import ArtworkCreate, ArtworkUpdate, ArtworkSearch

# Create artwork
artwork_data = ArtworkCreate(
    title="Custom Artwork",
    brand="Custom Gallery",
    price=Decimal("199.99"),
    style_tags=["custom", "artwork"]
)

artwork = await artwork_crud.create_artwork(artwork_data)

# Search artworks
search_params = ArtworkSearch(
    style_tags=["custom"],
    min_price=Decimal("100.00"),
    max_price=Decimal("300.00")
)

results = await artwork_crud.search_artworks(search_params)
```

## 🐛 Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Make sure you're in the backend directory
   ```bash
   cd backend
   python direct_crud_demo.py
   ```

2. **ImportError**: Install required dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. **Connection Error**: For the full API, you need Supabase running
   - Use the direct demo for testing without database
   - Or set up Supabase locally/cloud instance

4. **Port Already in Use**: Change the port in main.py
   ```python
   uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
   ```

### Environment Setup

Create a `.env` file in the backend directory:

```env
SUPABASE_URL=http://localhost:54321
SUPABASE_ANON_KEY=your-anon-key
```

## 📊 Expected Output

When you run `python direct_crud_demo.py`, you should see:

```
🎨 ArtDecorAI - Artwork CRUD Operations Demo
============================================================
📝 This demonstrates all CRUD operations for the artwork table
============================================================

1️⃣ CREATE - Creating new artworks...
✅ Created artwork: [UUID]
   Title: Modern Abstract Waves
   Brand: Contemporary Gallery
   Price: $299.99
   Styles: ['abstract', 'modern', 'blue']

2️⃣ READ - Getting artwork by ID...
✅ Retrieved artwork: Modern Abstract Waves

3️⃣ READ - Getting all artworks...
✅ Retrieved 3 artworks:
   - Modern Abstract Waves by Contemporary Gallery - $299.99
   - Minimalist Black Lines by Minimal Designs - $199.99
   - Vintage Botanical Print by Botanical Arts - $149.99

... (more operations)

🎉 All CRUD operations completed successfully!
```

## 🎯 Next Steps

1. **Run the demo**: `python direct_crud_demo.py`
2. **Start the API**: `python main.py`
3. **Test endpoints**: Visit http://localhost:8000/docs
4. **Integrate with frontend**: Use the API endpoints in your Next.js app
5. **Add to Supabase**: Connect to a real Supabase database

## 📚 Additional Resources

- **API Documentation**: http://localhost:8000/docs
- **Supabase Setup**: See `SUPABASE_SETUP.md`
- **Database Schema**: See `supabase/migrations/`
- **Examples**: See `examples/artwork_examples.py`
