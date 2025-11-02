"""
Artwork embedding model and data structures for ArtDecorAI
"""
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
import uuid


class ArtworkEmbeddingBase(BaseModel):
    """Base artwork embedding model with common fields"""
    artwork_id: uuid.UUID = Field(..., description="ID of the associated artwork")
    vector: List[float] = Field(..., description="Vector embedding (384 dimensions)")


class ArtworkEmbeddingCreate(ArtworkEmbeddingBase):
    """Model for creating new artwork embedding"""
    
    @field_validator('vector')
    @classmethod
    def validate_vector_dimensions(cls, v: List[float]) -> List[float]:
        """Validate that vector has exactly 384 dimensions"""
        if len(v) != 384:
            raise ValueError(f"Vector must have exactly 384 dimensions, got {len(v)}")
        return v


class ArtworkEmbeddingUpdate(BaseModel):
    """Model for updating artwork embedding"""
    vector: Optional[List[float]] = Field(None, description="Vector embedding (384 dimensions)")
    
    @field_validator('vector')
    @classmethod
    def validate_vector_dimensions(cls, v: Optional[List[float]]) -> Optional[List[float]]:
        """Validate that vector has exactly 384 dimensions if provided"""
        if v is not None and len(v) != 384:
            raise ValueError(f"Vector must have exactly 384 dimensions, got {len(v)}")
        return v


class ArtworkEmbeddingResponse(ArtworkEmbeddingBase):
    """Model for artwork embedding response"""
    id: uuid.UUID
    created_at: datetime
    
    class Config:
        from_attributes = True


class ArtworkEmbeddingSearch(BaseModel):
    """Model for searching artworks by embedding similarity"""
    query_vector: List[float] = Field(..., description="Query vector for similarity search (384 dimensions)")
    limit: int = Field(default=10, ge=1, le=100, description="Maximum number of results")
    threshold: Optional[float] = Field(default=0.0, ge=0.0, le=1.0, description="Minimum similarity threshold")
    
    @field_validator('query_vector')
    @classmethod
    def validate_vector_dimensions(cls, v: List[float]) -> List[float]:
        """Validate that query vector has exactly 384 dimensions"""
        if len(v) != 384:
            raise ValueError(f"Query vector must have exactly 384 dimensions, got {len(v)}")
        return v

