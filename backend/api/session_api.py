"""
FastAPI routes for session operations
"""
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
import logging

from models.session import (
    SessionCreate,
    SessionUpdate,
    SessionResponse,
    SessionSearch
)
from crud.session_crud import session_crud

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/sessions", tags=["sessions"])


@router.post("/", response_model=SessionResponse, status_code=201)
async def create_session(session: SessionCreate):
    """Create a new session"""
    try:
        result = await session_crud.create_session(session)
        return result
    except Exception as e:
        logger.error(f"Error creating session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(session_id: UUID):
    """Get session by ID"""
    try:
        session = await session_crud.get_session_by_id(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        return session
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting session {session_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user/{user_id}", response_model=List[SessionResponse])
async def get_sessions_by_user_id(
    user_id: UUID,
    limit: int = Query(default=10, ge=1, le=100, description="Maximum number of results"),
    offset: int = Query(default=0, ge=0, description="Number of results to skip")
):
    """Get sessions by user ID with pagination"""
    try:
        sessions = await session_crud.get_sessions_by_user_id(user_id, limit=limit, offset=offset)
        return sessions
    except Exception as e:
        logger.error(f"Error getting sessions for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[SessionResponse])
async def get_sessions(
    limit: int = Query(default=10, ge=1, le=100, description="Maximum number of results"),
    offset: int = Query(default=0, ge=0, description="Number of results to skip")
):
    """Get all sessions with pagination"""
    try:
        sessions = await session_crud.get_all_sessions(limit=limit, offset=offset)
        return sessions
    except Exception as e:
        logger.error(f"Error getting sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{session_id}", response_model=SessionResponse)
async def update_session(session_id: UUID, session_update: SessionUpdate):
    """Update session by ID"""
    try:
        session = await session_crud.update_session(session_id, session_update)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        return session
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating session {session_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{session_id}", status_code=204)
async def delete_session(session_id: UUID):
    """Delete session by ID"""
    try:
        success = await session_crud.delete_session(session_id)
        if not success:
            raise HTTPException(status_code=404, detail="Session not found")
        return JSONResponse(content={"message": "Session deleted successfully"}, status_code=204)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting session {session_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/user/{user_id}", status_code=200)
async def delete_sessions_by_user_id(user_id: UUID):
    """Delete all sessions for a user"""
    try:
        deleted_count = await session_crud.delete_sessions_by_user_id(user_id)
        return {
            "message": f"Deleted {deleted_count} session(s) for user",
            "deleted_count": deleted_count
        }
    except Exception as e:
        logger.error(f"Error deleting sessions for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search", response_model=List[SessionResponse])
async def search_sessions(search_params: SessionSearch):
    """Search sessions with filters"""
    try:
        sessions = await session_crud.search_sessions(search_params)
        return sessions
    except Exception as e:
        logger.error(f"Error searching sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search/chosen", response_model=List[SessionResponse])
async def get_sessions_with_chosen_artwork(
    user_id: Optional[UUID] = Query(None, description="Optional user ID to filter by"),
    limit: int = Query(default=10, ge=1, le=100, description="Maximum number of results"),
    offset: int = Query(default=0, ge=0, description="Number of results to skip")
):
    """Get sessions where user has chosen an artwork"""
    try:
        sessions = await session_crud.get_sessions_with_chosen_artwork(user_id=user_id, limit=limit, offset=offset)
        return sessions
    except Exception as e:
        logger.error(f"Error getting sessions with chosen artwork: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats/count", response_model=dict)
async def get_session_count(user_id: Optional[UUID] = Query(None, description="Optional user ID to filter by")):
    """Get total count of sessions"""
    try:
        count = await session_crud.count_sessions(user_id=user_id)
        return {
            "total_sessions": count,
            "user_id": str(user_id) if user_id else None
        }
    except Exception as e:
        logger.error(f"Error getting session count: {e}")
        raise HTTPException(status_code=500, detail=str(e))

