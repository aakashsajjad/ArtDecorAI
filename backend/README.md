# ArtDecorAI Backend

Python backend for the ArtDecorAI platform with comprehensive CRUD operations for artwork management.

## Features

- **Complete CRUD Operations** for artwork table
- **Advanced Search & Filtering** by style, price, brand
- **FastAPI REST API** with automatic documentation
- **Pydantic Models** for data validation
- **Supabase Integration** for database operations
- **Comprehensive Error Handling** and logging
- **Async/Await Support** for better performance

## Project Structure

```
backend/
├── api/
│   └── artwork_api.py          # FastAPI routes for artwork operations
├── crud/
│   └── artwork_crud.py         # CRUD operations for artwork table
├── models/
│   └── artwork.py              # Pydantic models for artwork data
├── examples/
│   └── artwork_examples.py     # Example usage of CRUD operations
├── database.py                 # Database connection and configuration
├── main.py                     # FastAPI application entry point
├── requirements.txt            # Python dependencies
├── env.example                 # Environment variables template
└── README.md                   # This file
```

## Installation

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Environment Variables:**
   ```bash
   cp env.example .env
   # Edit .env with your Supabase credentials
   ```

3. **Start the API Server:**
   ```bash
   python main.py
   ```

## API Endpoints

### Artwork Operations

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/artworks/` | Create new artwork |
| `GET` | `/api/artworks/{id}` | Get artwork by ID |
| `GET` | `/api/artworks/` | Get all artworks (paginated) |
| `PUT` | `/api/artworks/{id}` | Update artwork |
| `DELETE` | `/api/artworks/{id}` | Delete artwork |
| `POST` | `/api/artworks/search` | Search artworks with filters |
| `GET` | `/api/artworks/search/style` | Get artworks by style tags |
| `GET` | `/api/artworks/search/price` | Get artworks by price range |
| `GET` | `/api/artworks/search/brand` | Get artworks by brand |
| `GET` | `/api/artworks/stats/count` | Get total artwork count |
| `GET` | `/api/artworks/recent` | Get recently added artworks |

### Health & Status

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Root endpoint |
| `GET` | `/health` | Health check |
| `GET` | `/docs` | API documentation (Swagger) |
| `GET` | `/redoc` | Alternative API documentation |

## Usage Examples

### 1. Create Artwork

```python
from models.artwork import ArtworkCreate
from crud.artwork_crud import artwork_crud

artwork_data = ArtworkCreate(
    title="Modern Abstract Waves",
    brand="Contemporary Gallery",
    price=Decimal("299.99"),
    style_tags=["abstract", "modern", "blue"],
    dominant_palette={
        "primary": "#1e3a8a",
        "secondary": "#3b82f6",
        "accent": "#93c5fd"
    },
    image_url="https://example.com/artwork1.jpg"
)

artwork = await artwork_crud.create_artwork(artwork_data)
```

### 2. Search Artworks

```python
from models.artwork import ArtworkSearch

search_params = ArtworkSearch(
    style_tags=["abstract", "modern"],
    min_price=Decimal("100.00"),
    max_price=Decimal("500.00"),
    limit=10
)

artworks = await artwork_crud.search_artworks(search_params)
```

### 3. Update Artwork

```python
from models.artwork import ArtworkUpdate

update_data = ArtworkUpdate(
    price=Decimal("349.99"),
    style_tags=["abstract", "modern", "blue", "contemporary"]
)

updated_artwork = await artwork_crud.update_artwork(artwork_id, update_data)
```

### 4. Get Artworks by Style

```python
artworks = await artwork_crud.get_artworks_by_style(["abstract", "modern"])
```

### 5. Get Artworks by Price Range

```python
artworks = await artwork_crud.get_artworks_by_price_range(
    Decimal("200.00"), 
    Decimal("400.00")
)
```

## Data Models

### ArtworkCreate
```python
{
    "title": "string (required)",
    "brand": "string (optional)",
    "price": "decimal (optional)",
    "style_tags": ["string"] (optional),
    "dominant_palette": {} (optional),
    "image_url": "string (optional)"
}
```

### ArtworkUpdate
```python
{
    "title": "string (optional)",
    "brand": "string (optional)",
    "price": "decimal (optional)",
    "style_tags": ["string"] (optional),
    "dominant_palette": {} (optional),
    "image_url": "string (optional)"
}
```

### ArtworkSearch
```python
{
    "style_tags": ["string"] (optional),
    "min_price": "decimal (optional)",
    "max_price": "decimal (optional)",
    "brand": "string (optional)",
    "limit": "integer (default: 10)",
    "offset": "integer (default: 0)"
}
```

## Error Handling

The API includes comprehensive error handling:

- **404 Not Found** - When artwork doesn't exist
- **400 Bad Request** - Invalid input data
- **500 Internal Server Error** - Database or server errors
- **Validation Errors** - Pydantic model validation

## Logging

All operations are logged with appropriate levels:

- **INFO** - Successful operations
- **WARNING** - Non-critical issues
- **ERROR** - Failed operations
- **DEBUG** - Detailed debugging information

## Running Examples

```bash
# Run the example script
python examples/artwork_examples.py
```

This will demonstrate all CRUD operations with sample data.

## API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Development

### Adding New Endpoints

1. Create new models in `models/`
2. Add CRUD operations in `crud/`
3. Create API routes in `api/`
4. Update `main.py` to include new routers

### Database Schema

The artwork table includes:

- `id` - UUID primary key
- `title` - Artwork title (required)
- `brand` - Brand name (optional)
- `price` - Price in decimal (optional)
- `style_tags` - Array of style tags (optional)
- `dominant_palette` - JSON color palette (optional)
- `image_url` - Image URL (optional)
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

## Production Deployment

1. **Environment Variables**: Set production Supabase credentials
2. **Database**: Ensure Supabase project is properly configured
3. **Security**: Enable Row Level Security (RLS) policies
4. **Monitoring**: Set up logging and error tracking
5. **Scaling**: Consider load balancing for high traffic

## Contributing

1. Follow the existing code structure
2. Add comprehensive error handling
3. Include logging for all operations
4. Write tests for new functionality
5. Update documentation

## License

This project is part of the ArtDecorAI platform.
