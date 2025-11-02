# FastAPI Artwork Insertion Guide

## How FastAPI Inserts Data into Artwork Table

### Architecture Flow

```
Client Request → FastAPI Endpoint → CRUD Layer → Database
```

---

## 1. FastAPI Endpoint (artwork_api.py)

### Standard Insert Endpoint

```python
@router.post("/", response_model=ArtworkResponse, status_code=201)
async def create_artwork(artwork: ArtworkCreate):
    """Create a new artwork"""
    try:
        result = await artwork_crud.create_artwork(artwork)
        return result
    except Exception as e:
        logger.error(f"Error creating artwork: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

**Endpoint**: `POST /api/artworks/`

**Request Body** (JSON):
```json
{
  "title": "Modern Abstract Art",
  "brand": "ArtDecorAI",
  "price": 299.99,
  "style_tags": ["modern", "abstract"],
  "dominant_palette": {
    "primary": "#3498db",
    "secondary": "#e74c3c"
  },
  "image_url": "https://example.com/art.jpg"
}
```

---

### New Sample Insert Endpoint (using database.py)

```python
@router.post("/sample", status_code=201)
async def create_sample_artwork():
    """Create a sample artwork using database.py method"""
    result = db_connection.add_sample_record()
    return result
```

**Endpoint**: `POST /api/artworks/sample`

**No request body needed** - creates a sample artwork automatically

---

## 2. Pydantic Model (models/artwork.py)

### ArtworkCreate Model

```python
class ArtworkCreate(ArtworkBase):
    """Model for creating new artwork"""
    pass

class ArtworkBase(BaseModel):
    title: str
    brand: Optional[str] = None
    price: Optional[Decimal] = None
    style_tags: Optional[List[str]] = []
    dominant_palette: Optional[Dict[str, Any]] = None
    image_url: Optional[str] = None
```

**Purpose**: Validates incoming request data before insertion

---

## 3. CRUD Layer (crud/artwork_crud.py)

### create_artwork Method

```python
async def create_artwork(self, artwork: ArtworkCreate) -> ArtworkResponse:
    """Create a new artwork"""
    # Convert Pydantic model to dict
    artwork_data = artwork.model_dump()
    
    # Ensure all Decimal values are JSON serializable
    artwork_data = self._convert_decimals_to_primitives(artwork_data)
    
    # Insert into database
    result = self.db.table("artwork").insert(artwork_data).execute()
    
    if not result.data:
        raise Exception("Failed to create artwork")
    
    return ArtworkResponse(**result.data[0])
```

**Purpose**: 
- Converts Pydantic model to dictionary
- Handles data type conversions (Decimal → float)
- Executes Supabase insert operation
- Returns formatted response

---

## 4. Database Connection (database.py)

### Direct Insert Method

```python
def add_sample_record(self) -> dict:
    """Add a sample artwork record to the database"""
    sample_data = {
        "title": "Sample Modern Art Piece",
        "brand": "ArtDecorAI",
        "price": 299.99,
        "style_tags": json.dumps(["modern", "abstract", "minimalist"]),
        "dominant_palette": json.dumps({...}),
        "image_url": "https://example.com/sample-art.jpg"
    }
    
    result = self.client.table("artwork").insert(sample_data).execute()
    return {"success": True, "artwork_id": str(result.data[0]['id'])}
```

**Purpose**: Direct database insertion bypassing CRUD layer

---

## Usage Examples

### Using FastAPI Endpoint (Standard Way)

```bash
# Start FastAPI server
cd backend
python -m uvicorn main:app --reload

# Make POST request
curl -X POST "http://localhost:8000/api/artworks/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Beautiful Abstract",
    "brand": "Modern Gallery",
    "price": 199.99,
    "style_tags": ["abstract", "modern"],
    "image_url": "https://example.com/art.jpg"
  }'
```

### Using Sample Endpoint

```bash
curl -X POST "http://localhost:8000/api/artworks/sample"
```

### Using Python Script

```python
from database import db_connection

# Direct insertion
result = db_connection.add_sample_record()
print(result)
```

### Using CRUD Layer

```python
from crud.artwork_crud import artwork_crud
from models.artwork import ArtworkCreate

artwork = ArtworkCreate(
    title="My Art",
    brand="My Brand",
    price=99.99
)

result = await artwork_crud.create_artwork(artwork)
```

---

## Data Flow Summary

1. **Client** sends POST request with JSON data
2. **FastAPI** validates data using `ArtworkCreate` Pydantic model
3. **API Route** calls `artwork_crud.create_artwork()`
4. **CRUD Layer** converts model to dict and inserts via Supabase client
5. **Database** stores the record and returns the result
6. **Response** is formatted as `ArtworkResponse` and sent back to client

---

## Key Differences

| Method | Use Case | Validation | Response Format |
|--------|----------|------------|----------------|
| FastAPI Endpoint | Production API calls | ✅ Pydantic validation | ArtworkResponse |
| CRUD Layer | Internal operations | ✅ Pydantic validation | ArtworkResponse |
| database.py | Quick inserts, testing | ⚠️ Manual validation | Dict with success status |

---

## Notes

- **Async/Await**: FastAPI endpoints use async functions
- **Error Handling**: Exceptions are caught and returned as HTTP errors
- **Data Validation**: Pydantic models ensure data types are correct
- **Type Safety**: Uses UUID, Decimal, List types for type safety
- **RLS Policies**: Make sure INSERT policies are set in Supabase!


