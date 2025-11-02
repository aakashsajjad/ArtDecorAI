"""
User profile model and data structures for ArtDecorAI
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal
import uuid


class ColorProfile(BaseModel):
    """Color profile JSON structure"""
    favorite_colors: Optional[List[str]] = Field(default=[], description="List of favorite color hex codes")
    avoid_colors: Optional[List[str]] = Field(default=[], description="List of colors to avoid")
    preferred_temperature: Optional[str] = Field(None, description="Color temperature preference: cool, warm, neutral")
    brightness_preference: Optional[str] = Field(None, description="Brightness preference: low, medium, high")


class BudgetRange(BaseModel):
    """Budget range JSON structure"""
    min: Optional[Decimal] = Field(None, ge=0, description="Minimum budget")
    max: Optional[Decimal] = Field(None, ge=0, description="Maximum budget")
    currency: Optional[str] = Field(default="USD", description="Currency code")


class UserProfileBase(BaseModel):
    """Base user profile model with common fields"""
    user_id: uuid.UUID = Field(..., description="User ID (unique identifier)")
    preferred_styles: Optional[List[str]] = Field(default=[], description="List of preferred style tags")
    color_profile_json: Optional[Dict[str, Any]] = Field(None, description="Color profile preferences as JSON")
    budget_range: Optional[Dict[str, Any]] = Field(None, description="Budget range as JSON")


class UserProfileCreate(UserProfileBase):
    """Model for creating new user profile"""
    pass


class UserProfileUpdate(BaseModel):
    """Model for updating user profile"""
    preferred_styles: Optional[List[str]] = None
    color_profile_json: Optional[Dict[str, Any]] = None
    budget_range: Optional[Dict[str, Any]] = None


class UserProfileResponse(UserProfileBase):
    """Model for user profile response"""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserProfileSearch(BaseModel):
    """Model for searching user profiles"""
    preferred_styles: Optional[List[str]] = None
    has_color_profile: Optional[bool] = None
    has_budget_range: Optional[bool] = None
    limit: int = Field(default=10, ge=1, le=100)
    offset: int = Field(default=0, ge=0)

