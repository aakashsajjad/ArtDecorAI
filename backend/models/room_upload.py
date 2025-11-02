"""
Room upload model and data structures for ArtDecorAI
"""
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class PaletteData(BaseModel):
    """Palette JSON structure"""
    primary: Optional[str] = Field(None, description="Primary color hex code")
    secondary: Optional[str] = Field(None, description="Secondary color hex code")
    accent: Optional[str] = Field(None, description="Accent color hex code")
    neutral: Optional[str] = Field(None, description="Neutral color hex code")


class LightingData(BaseModel):
    """Lighting JSON structure"""
    brightness: Optional[float] = Field(None, ge=0.0, le=1.0, description="Brightness level (0.0-1.0)")
    temperature: Optional[str] = Field(None, description="Light temperature: warm, cool, neutral")
    natural_light: Optional[bool] = Field(None, description="Whether natural light is present")


class RoomUploadBase(BaseModel):
    """Base room upload model with common fields"""
    user_id: uuid.UUID = Field(..., description="User ID who uploaded the room")
    room_type: Optional[str] = Field(None, max_length=100, description="Type of room (e.g., living_room, bedroom, kitchen)")
    s3_url: Optional[str] = Field(None, max_length=500, description="S3 URL of the uploaded room image")
    palette_json: Optional[Dict[str, Any]] = Field(None, description="Color palette data as JSON")
    lighting_json: Optional[Dict[str, Any]] = Field(None, description="Lighting information as JSON")


class RoomUploadCreate(RoomUploadBase):
    """Model for creating new room upload"""
    pass


class RoomUploadUpdate(BaseModel):
    """Model for updating room upload"""
    room_type: Optional[str] = Field(None, max_length=100)
    s3_url: Optional[str] = Field(None, max_length=500)
    palette_json: Optional[Dict[str, Any]] = None
    lighting_json: Optional[Dict[str, Any]] = None


class RoomUploadResponse(RoomUploadBase):
    """Model for room upload response"""
    id: uuid.UUID
    created_at: datetime
    
    class Config:
        from_attributes = True


class RoomUploadSearch(BaseModel):
    """Model for searching room uploads"""
    user_id: Optional[uuid.UUID] = None
    room_type: Optional[str] = None
    has_palette: Optional[bool] = None
    has_lighting: Optional[bool] = None
    limit: int = Field(default=10, ge=1, le=100)
    offset: int = Field(default=0, ge=0)

