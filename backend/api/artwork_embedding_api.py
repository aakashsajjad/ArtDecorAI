"""
FastAPI routes for artwork embedding operations
"""
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
import logging

from models.artwork_embedding import (
    ArtworkEmbeddingCreate,
    ArtworkEmbeddingUpdate,
    ArtworkEmbeddingResponse,
    ArtworkEmbeddingSearch
)
from pydantic import BaseModel
from crud.artwork_embedding_crud import artwork_embedding_crud
from database import db_connection

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/artwork-embeddings", tags=["artwork-embeddings"])


@router.post("/", response_model=ArtworkEmbeddingResponse, status_code=201)
async def create_embedding(embedding: ArtworkEmbeddingCreate):
    """Create a new artwork embedding"""
    try:
        result = await artwork_embedding_crud.create_embedding(embedding)
        return result
    except ValueError as e:
        logger.error(f"Validation error creating embedding: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating embedding: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{embedding_id}", response_model=ArtworkEmbeddingResponse)
async def get_embedding(embedding_id: UUID):
    """Get artwork embedding by ID"""
    try:
        embedding = await artwork_embedding_crud.get_embedding_by_id(embedding_id)
        if not embedding:
            raise HTTPException(status_code=404, detail="Artwork embedding not found")
        return embedding
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting embedding {embedding_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/artwork/{artwork_id}", response_model=ArtworkEmbeddingResponse)
async def get_embedding_by_artwork_id(artwork_id: UUID):
    """Get artwork embedding by artwork ID"""
    try:
        embedding = await artwork_embedding_crud.get_embedding_by_artwork_id(artwork_id)
        if not embedding:
            raise HTTPException(status_code=404, detail="Artwork embedding not found for this artwork")
        return embedding
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting embedding for artwork {artwork_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[ArtworkEmbeddingResponse])
async def get_embeddings(
    limit: int = Query(default=10, ge=1, le=100, description="Maximum number of results"),
    offset: int = Query(default=0, ge=0, description="Number of results to skip")
):
    """Get all artwork embeddings with pagination"""
    try:
        embeddings = await artwork_embedding_crud.get_all_embeddings(limit=limit, offset=offset)
        return embeddings
    except Exception as e:
        logger.error(f"Error getting embeddings: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{embedding_id}", response_model=ArtworkEmbeddingResponse)
async def update_embedding(embedding_id: UUID, embedding_update: ArtworkEmbeddingUpdate):
    """Update artwork embedding by ID"""
    try:
        embedding = await artwork_embedding_crud.update_embedding(embedding_id, embedding_update)
        if not embedding:
            raise HTTPException(status_code=404, detail="Artwork embedding not found")
        return embedding
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Validation error updating embedding: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating embedding {embedding_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{embedding_id}", status_code=204)
async def delete_embedding(embedding_id: UUID):
    """Delete artwork embedding by ID"""
    try:
        success = await artwork_embedding_crud.delete_embedding(embedding_id)
        if not success:
            raise HTTPException(status_code=404, detail="Artwork embedding not found")
        return JSONResponse(content={"message": "Artwork embedding deleted successfully"}, status_code=204)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting embedding {embedding_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/artwork/{artwork_id}", status_code=204)
async def delete_embedding_by_artwork_id(artwork_id: UUID):
    """Delete artwork embedding by artwork ID"""
    try:
        success = await artwork_embedding_crud.delete_embedding_by_artwork_id(artwork_id)
        if not success:
            raise HTTPException(status_code=404, detail="Artwork embedding not found for this artwork")
        return JSONResponse(content={"message": "Artwork embedding deleted successfully"}, status_code=204)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting embedding for artwork {artwork_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search", response_model=List[dict])
async def search_similar_embeddings(search_params: ArtworkEmbeddingSearch):
    """Search for similar artwork embeddings using vector similarity"""
    try:
        results = await artwork_embedding_crud.search_similar_embeddings(search_params)
        return results
    except ValueError as e:
        logger.error(f"Validation error searching embeddings: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error searching embeddings: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats/count", response_model=dict)
async def get_embedding_count():
    """Get total count of artwork embeddings"""
    try:
        count = await artwork_embedding_crud.count_embeddings()
        return {"total_embeddings": count}
    except Exception as e:
        logger.error(f"Error getting embedding count: {e}")
        raise HTTPException(status_code=500, detail=str(e))


class SampleEmbeddingRequest(BaseModel):
    """Request model for creating sample embedding"""
    artwork_id: Optional[UUID] = None


@router.post("/sample", status_code=201)
async def create_sample_embedding(request: Optional[SampleEmbeddingRequest] = None):
    """Create a sample artwork embedding using database.py method
    
    If artwork_id is not provided, a sample artwork will be created first.
    """
    try:
        artwork_id_str = str(request.artwork_id) if request and hasattr(request, 'artwork_id') and request.artwork_id else None
        result = db_connection.add_sample_embedding(artwork_id_str)
        
        if result.get("success"):
            return {
                "message": result.get("message"),
                "embedding_id": result.get("embedding_id"),
                "artwork_id": result.get("artwork_id")
            }
        else:
            raise HTTPException(
                status_code=500,
                detail=result.get("error"),
                headers={"X-Help": result.get("help", "")}
            )
    except Exception as e:
        logger.error(f"Error creating sample embedding: {e}")
        raise HTTPException(status_code=500, detail=str(e))

