"""
Artwork model and data structures for ArtDecorAI
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal
import uuid

class ArtworkBase(BaseModel):
    """Base artwork model with common fields"""
    title: str = Field(..., min_length=1, max_length=255, description="Artwork title")
    brand: Optional[str] = Field(None, max_length=100, description="Artwork brand")
    price: Optional[Decimal] = Field(None, ge=0, description="Artwork price")
    style_tags: Optional[List[str]] = Field(default=[], description="Style tags")
    dominant_palette: Optional[Dict[str, Any]] = Field(None, description="Color palette data")
    image_url: Optional[str] = Field(None, max_length=500, description="Image URL")

class ArtworkCreate(ArtworkBase):
    """Model for creating new artwork"""
    pass

class ArtworkUpdate(BaseModel):
    """Model for updating artwork"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    brand: Optional[str] = Field(None, max_length=100)
    price: Optional[Decimal] = Field(None, ge=0)
    style_tags: Optional[List[str]] = None
    dominant_palette: Optional[Dict[str, Any]] = None
    image_url: Optional[str] = Field(None, max_length=500)

class ArtworkResponse(ArtworkBase):
    """Model for artwork response"""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ArtworkSearch(BaseModel):
    """Model for artwork search parameters"""
    style_tags: Optional[List[str]] = None
    min_price: Optional[Decimal] = None
    max_price: Optional[Decimal] = None
    brand: Optional[str] = None
    limit: int = Field(default=10, ge=1, le=100)
    offset: int = Field(default=0, ge=0)

class ArtworkFilter(BaseModel):
    """Model for advanced artwork filtering"""
    style_tags: Optional[List[str]] = None
    price_range: Optional[Dict[str, Decimal]] = None
    brand: Optional[str] = None
    color_palette: Optional[Dict[str, Any]] = None
    created_after: Optional[datetime] = None
    created_before: Optional[datetime] = None
