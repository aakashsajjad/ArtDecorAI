"""
FastAPI main application for ArtDecorAI backend
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import uvicorn
from datetime import datetime

# Try to import database connection, but don't fail if it's not available
try:
    from database import db_connection
    from api.artwork_api import router as artwork_router
    DATABASE_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Database modules not available: {e}")
    DATABASE_AVAILABLE = False
    db_connection = None
    artwork_router = None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="ArtDecorAI API",
    description="AI-Powered Home Décor Recommendation Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers only if available
if DATABASE_AVAILABLE and artwork_router:
    app.include_router(artwork_router)
    logger.info("Artwork API router included")
else:
    logger.warning("Artwork API router not available - using standalone mode")

@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup"""
    if DATABASE_AVAILABLE and db_connection:
        try:
            if db_connection.test_connection():
                logger.info("Database connection established successfully")
            else:
                logger.warning("Database connection failed - running in standalone mode")
        except Exception as e:
            logger.warning(f"Database connection error: {e} - running in standalone mode")
    else:
        logger.info("Running in standalone mode without database")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "ArtDecorAI API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        if DATABASE_AVAILABLE and db_connection:
            db_status = db_connection.test_connection()
            return {
                "status": "healthy" if db_status else "degraded",
                "database": "connected" if db_status else "disconnected",
                "mode": "standalone" if not db_status else "database",
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "status": "healthy",
                "database": "not_configured",
                "mode": "standalone",
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "degraded",
            "database": "error",
            "mode": "standalone",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

# Basic artwork endpoints for standalone mode
if not DATABASE_AVAILABLE:
    # In-memory storage for demonstration
    artworks_db = [
        {
            "id": "1",
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
            "id": "2",
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
        }
    ]

    @app.get("/api/artworks/")
    async def get_artworks_standalone():
        """Get all artworks (standalone mode)"""
        return artworks_db

    @app.get("/api/artworks/{artwork_id}")
    async def get_artwork_standalone(artwork_id: str):
        """Get artwork by ID (standalone mode)"""
        artwork = next((a for a in artworks_db if a["id"] == artwork_id), None)
        if not artwork:
            raise HTTPException(status_code=404, detail="Artwork not found")
        return artwork

    @app.post("/api/artworks/")
    async def create_artwork_standalone(artwork_data: dict):
        """Create artwork (standalone mode)"""
        new_artwork = {
            "id": str(len(artworks_db) + 1),
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
        return new_artwork

    @app.put("/api/artworks/{artwork_id}")
    async def update_artwork_standalone(artwork_id: str, artwork_data: dict):
        """Update artwork (standalone mode)"""
        artwork_index = next((i for i, a in enumerate(artworks_db) if a["id"] == artwork_id), None)
        if artwork_index is None:
            raise HTTPException(status_code=404, detail="Artwork not found")
        
        update_data = {k: v for k, v in artwork_data.items() if v is not None}
        update_data["updated_at"] = datetime.now().isoformat()
        artworks_db[artwork_index].update(update_data)
        return artworks_db[artwork_index]

    @app.delete("/api/artworks/{artwork_id}")
    async def delete_artwork_standalone(artwork_id: str):
        """Delete artwork (standalone mode)"""
        artwork_index = next((i for i, a in enumerate(artworks_db) if a["id"] == artwork_id), None)
        if artwork_index is None:
            raise HTTPException(status_code=404, detail="Artwork not found")
        
        deleted_artwork = artworks_db.pop(artwork_index)
        return {"message": "Artwork deleted successfully", "deleted_artwork": deleted_artwork}

    @app.get("/api/artworks/stats/count")
    async def get_artwork_count_standalone():
        """Get artwork count (standalone mode)"""
        return {"total_artworks": len(artworks_db)}

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
