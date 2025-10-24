"""
Standalone FastAPI application for ArtDecorAI backend
This version works without Supabase connection
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import uvicorn
from typing import List, Optional
from decimal import Decimal
from datetime import datetime
from uuid import uuid4
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="ArtDecorAI API - Standalone",
    description="AI-Powered Home Décor Recommendation Platform (Standalone Version)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for demonstration
artworks_db = [
    {
        "id": str(uuid4()),
        "title": "Modern Abstract Waves",
        "brand": "Contemporary Gallery",
        "price": 299.99,
        "style_tags": ["abstract", "modern", "blue"],
        "dominant_palette": {
            "primary": "#1e3a8a",
            "secondary": "#3b82f6",
            "accent": "#93c5fd"
        },
        "image_url": "https://images.unsplash.com/photo-1541961017774-22349e4a1262?w=400",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    {
        "id": str(uuid4()),
        "title": "Minimalist Black Lines",
        "brand": "Minimal Designs",
        "price": 199.99,
        "style_tags": ["minimalist", "black", "geometric"],
        "dominant_palette": {
            "primary": "#000000",
            "secondary": "#404040",
            "accent": "#808080"
        },
        "image_url": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    {
        "id": str(uuid4()),
        "title": "Vintage Botanical Print",
        "brand": "Botanical Arts",
        "price": 149.99,
        "style_tags": ["vintage", "botanical", "green"],
        "dominant_palette": {
            "primary": "#166534",
            "secondary": "#22c55e",
            "accent": "#84cc16"
        },
        "image_url": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
]

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "ArtDecorAI API - Standalone Version",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "note": "This is a standalone version that works without Supabase"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "in-memory",
        "artworks_count": len(artworks_db),
        "timestamp": datetime.now().isoformat()
    }

# Artwork CRUD Endpoints

@app.post("/api/artworks/")
async def create_artwork(artwork_data: dict):
    """Create a new artwork"""
    try:
        new_artwork = {
            "id": str(uuid4()),
            "title": artwork_data.get("title", ""),
            "brand": artwork_data.get("brand"),
            "price": float(artwork_data.get("price", 0)) if artwork_data.get("price") else None,
            "style_tags": artwork_data.get("style_tags", []),
            "dominant_palette": artwork_data.get("dominant_palette"),
            "image_url": artwork_data.get("image_url"),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        artworks_db.append(new_artwork)
        logger.info(f"Created artwork: {new_artwork['id']}")
        return new_artwork
    except Exception as e:
        logger.error(f"Error creating artwork: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/artworks/{artwork_id}")
async def get_artwork(artwork_id: str):
    """Get artwork by ID"""
    try:
        artwork = next((a for a in artworks_db if a["id"] == artwork_id), None)
        if not artwork:
            raise HTTPException(status_code=404, detail="Artwork not found")
        return artwork
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting artwork {artwork_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/artworks/")
async def get_artworks(limit: int = 10, offset: int = 0):
    """Get all artworks with pagination"""
    try:
        start = offset
        end = offset + limit
        paginated_artworks = artworks_db[start:end]
        return paginated_artworks
    except Exception as e:
        logger.error(f"Error getting artworks: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/artworks/{artwork_id}")
async def update_artwork(artwork_id: str, artwork_data: dict):
    """Update artwork by ID"""
    try:
        artwork_index = next((i for i, a in enumerate(artworks_db) if a["id"] == artwork_id), None)
        if artwork_index is None:
            raise HTTPException(status_code=404, detail="Artwork not found")
        
        # Update only provided fields
        update_data = {k: v for k, v in artwork_data.items() if v is not None}
        update_data["updated_at"] = datetime.now().isoformat()
        
        artworks_db[artwork_index].update(update_data)
        
        logger.info(f"Updated artwork: {artwork_id}")
        return artworks_db[artwork_index]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating artwork {artwork_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/artworks/{artwork_id}")
async def delete_artwork(artwork_id: str):
    """Delete artwork by ID"""
    try:
        artwork_index = next((i for i, a in enumerate(artworks_db) if a["id"] == artwork_id), None)
        if artwork_index is None:
            raise HTTPException(status_code=404, detail="Artwork not found")
        
        deleted_artwork = artworks_db.pop(artwork_index)
        logger.info(f"Deleted artwork: {artwork_id}")
        return {"message": "Artwork deleted successfully", "deleted_artwork": deleted_artwork}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting artwork {artwork_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/artworks/search")
async def search_artworks(search_params: dict):
    """Search artworks with filters"""
    try:
        filtered_artworks = artworks_db.copy()
        
        # Apply filters
        if search_params.get("style_tags"):
            style_tags = search_params["style_tags"]
            if isinstance(style_tags, str):
                style_tags = [style_tags]
            filtered_artworks = [a for a in filtered_artworks 
                               if any(tag in a.get("style_tags", []) for tag in style_tags)]
        
        if search_params.get("min_price"):
            min_price = float(search_params["min_price"])
            filtered_artworks = [a for a in filtered_artworks 
                               if a.get("price") and a["price"] >= min_price]
        
        if search_params.get("max_price"):
            max_price = float(search_params["max_price"])
            filtered_artworks = [a for a in filtered_artworks 
                               if a.get("price") and a["price"] <= max_price]
        
        if search_params.get("brand"):
            brand = search_params["brand"].lower()
            filtered_artworks = [a for a in filtered_artworks 
                               if a.get("brand") and brand in a["brand"].lower()]
        
        # Apply pagination
        limit = search_params.get("limit", 10)
        offset = search_params.get("offset", 0)
        start = offset
        end = offset + limit
        
        return filtered_artworks[start:end]
    except Exception as e:
        logger.error(f"Error searching artworks: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/artworks/search/style")
async def get_artworks_by_style(style_tags: List[str]):
    """Get artworks by style tags"""
    try:
        filtered_artworks = [a for a in artworks_db 
                           if any(tag in a.get("style_tags", []) for tag in style_tags)]
        return filtered_artworks
    except Exception as e:
        logger.error(f"Error getting artworks by style: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/artworks/search/price")
async def get_artworks_by_price_range(min_price: float, max_price: float):
    """Get artworks within price range"""
    try:
        filtered_artworks = [a for a in artworks_db 
                           if a.get("price") and min_price <= a["price"] <= max_price]
        return filtered_artworks
    except Exception as e:
        logger.error(f"Error getting artworks by price range: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/artworks/search/brand")
async def get_artworks_by_brand(brand: str):
    """Get artworks by brand"""
    try:
        filtered_artworks = [a for a in artworks_db 
                           if a.get("brand") and brand.lower() in a["brand"].lower()]
        return filtered_artworks
    except Exception as e:
        logger.error(f"Error getting artworks by brand: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/artworks/stats/count")
async def get_artwork_count():
    """Get total count of artworks"""
    try:
        return {"total_artworks": len(artworks_db)}
    except Exception as e:
        logger.error(f"Error getting artwork count: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/artworks/recent")
async def get_recent_artworks(limit: int = 5):
    """Get recently added artworks"""
    try:
        sorted_artworks = sorted(artworks_db, key=lambda x: x["created_at"], reverse=True)
        return sorted_artworks[:limit]
    except Exception as e:
        logger.error(f"Error getting recent artworks: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    print("🎨 ArtDecorAI API - Standalone Version")
    print("=" * 50)
    print("✅ No database connection required")
    print("✅ In-memory storage enabled")
    print("✅ CORS configured for frontend")
    print("✅ All CRUD operations available")
    print("=" * 50)
    print("🌐 API will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("=" * 50)
    
    uvicorn.run(
        "main_standalone:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
