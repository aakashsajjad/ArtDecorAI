"""
Session model and data structures for ArtDecorAI
"""
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class SessionBase(BaseModel):
    """Base session model with common fields"""
    user_id: uuid.UUID = Field(..., description="User ID who created the session")
    query_text: Optional[str] = Field(None, description="User's query/search text")
    topk_ids: Optional[List[uuid.UUID]] = Field(default=[], description="Array of top K artwork IDs suggested")
    chosen_id: Optional[uuid.UUID] = Field(None, description="ID of the artwork chosen by the user")
    rationale: Optional[str] = Field(None, description="Explanation/rationale for the recommendation")


class SessionCreate(SessionBase):
    """Model for creating new session"""
    pass


class SessionUpdate(BaseModel):
    """Model for updating session"""
    query_text: Optional[str] = None
    topk_ids: Optional[List[uuid.UUID]] = None
    chosen_id: Optional[uuid.UUID] = None
    rationale: Optional[str] = None


class SessionResponse(SessionBase):
    """Model for session response"""
    id: uuid.UUID
    created_at: datetime
    
    class Config:
        from_attributes = True


class SessionSearch(BaseModel):
    """Model for searching sessions"""
    user_id: Optional[uuid.UUID] = None
    has_chosen_id: Optional[bool] = None
    has_topk_ids: Optional[bool] = None
    has_rationale: Optional[bool] = None
    limit: int = Field(default=10, ge=1, le=100)
    offset: int = Field(default=0, ge=0)

