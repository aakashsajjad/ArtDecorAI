"""
FastAPI routes for artwork operations
"""
from typing import List, Optional
from uuid import UUID
from decimal import Decimal
from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
import logging

from models.artwork import ArtworkCreate, ArtworkUpdate, ArtworkResponse, ArtworkSearch
from crud.artwork_crud import artwork_crud

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/artworks", tags=["artworks"])

@router.post("/", response_model=ArtworkResponse, status_code=201)
async def create_artwork(artwork: ArtworkCreate):
    """Create a new artwork"""
    try:
        result = await artwork_crud.create_artwork(artwork)
        return result
    except Exception as e:
        logger.error(f"Error creating artwork: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{artwork_id}", response_model=ArtworkResponse)
async def get_artwork(artwork_id: UUID):
    """Get artwork by ID"""
    try:
        artwork = await artwork_crud.get_artwork_by_id(artwork_id)
        if not artwork:
            raise HTTPException(status_code=404, detail="Artwork not found")
        return artwork
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting artwork {artwork_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[ArtworkResponse])
async def get_artworks(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0)
):
    """Get all artworks with pagination"""
    try:
        artworks = await artwork_crud.get_all_artworks(limit=limit, offset=offset)
        return artworks
    except Exception as e:
        logger.error(f"Error getting artworks: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{artwork_id}", response_model=ArtworkResponse)
async def update_artwork(artwork_id: UUID, artwork_update: ArtworkUpdate):
    """Update artwork by ID"""
    try:
        artwork = await artwork_crud.update_artwork(artwork_id, artwork_update)
        if not artwork:
            raise HTTPException(status_code=404, detail="Artwork not found")
        return artwork
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating artwork {artwork_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{artwork_id}", status_code=204)
async def delete_artwork(artwork_id: UUID):
    """Delete artwork by ID"""
    try:
        success = await artwork_crud.delete_artwork(artwork_id)
        if not success:
            raise HTTPException(status_code=404, detail="Artwork not found")
        return JSONResponse(content={"message": "Artwork deleted successfully"}, status_code=204)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting artwork {artwork_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search", response_model=List[ArtworkResponse])
async def search_artworks(search_params: ArtworkSearch):
    """Search artworks with filters"""
    try:
        artworks = await artwork_crud.search_artworks(search_params)
        return artworks
    except Exception as e:
        logger.error(f"Error searching artworks: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search/style", response_model=List[ArtworkResponse])
async def get_artworks_by_style(
    style_tags: List[str] = Query(..., description="Style tags to search for")
):
    """Get artworks by style tags"""
    try:
        artworks = await artwork_crud.get_artworks_by_style(style_tags)
        return artworks
    except Exception as e:
        logger.error(f"Error getting artworks by style: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search/price", response_model=List[ArtworkResponse])
async def get_artworks_by_price_range(
    min_price: Decimal = Query(..., ge=0, description="Minimum price"),
    max_price: Decimal = Query(..., ge=0, description="Maximum price")
):
    """Get artworks within price range"""
    try:
        artworks = await artwork_crud.get_artworks_by_price_range(min_price, max_price)
        return artworks
    except Exception as e:
        logger.error(f"Error getting artworks by price range: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search/brand", response_model=List[ArtworkResponse])
async def get_artworks_by_brand(brand: str = Query(..., description="Brand name")):
    """Get artworks by brand"""
    try:
        artworks = await artwork_crud.get_artworks_by_brand(brand)
        return artworks
    except Exception as e:
        logger.error(f"Error getting artworks by brand: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/count", response_model=dict)
async def get_artwork_count():
    """Get total count of artworks"""
    try:
        count = await artwork_crud.count_artworks()
        return {"total_artworks": count}
    except Exception as e:
        logger.error(f"Error getting artwork count: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recent", response_model=List[ArtworkResponse])
async def get_recent_artworks(
    limit: int = Query(default=5, ge=1, le=20, description="Number of recent artworks to return")
):
    """Get recently added artworks"""
    try:
        artworks = await artwork_crud.get_recent_artworks(limit)
        return artworks
    except Exception as e:
        logger.error(f"Error getting recent artworks: {e}")
        raise HTTPException(status_code=500, detail=str(e))
