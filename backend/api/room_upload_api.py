"""
FastAPI routes for room upload operations
"""
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
import logging

from models.room_upload import (
    RoomUploadCreate,
    RoomUploadUpdate,
    RoomUploadResponse,
    RoomUploadSearch
)
from crud.room_upload_crud import room_upload_crud

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/room-uploads", tags=["room-uploads"])


@router.post("/", response_model=RoomUploadResponse, status_code=201)
async def create_room_upload(room_upload: RoomUploadCreate):
    """Create a new room upload"""
    try:
        result = await room_upload_crud.create_room_upload(room_upload)
        return result
    except Exception as e:
        logger.error(f"Error creating room upload: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{upload_id}", response_model=RoomUploadResponse)
async def get_room_upload(upload_id: UUID):
    """Get room upload by ID"""
    try:
        upload = await room_upload_crud.get_room_upload_by_id(upload_id)
        if not upload:
            raise HTTPException(status_code=404, detail="Room upload not found")
        return upload
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting room upload {upload_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user/{user_id}", response_model=List[RoomUploadResponse])
async def get_room_uploads_by_user_id(
    user_id: UUID,
    limit: int = Query(default=10, ge=1, le=100, description="Maximum number of results"),
    offset: int = Query(default=0, ge=0, description="Number of results to skip")
):
    """Get room uploads by user ID with pagination"""
    try:
        uploads = await room_upload_crud.get_room_uploads_by_user_id(user_id, limit=limit, offset=offset)
        return uploads
    except Exception as e:
        logger.error(f"Error getting room uploads for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[RoomUploadResponse])
async def get_room_uploads(
    limit: int = Query(default=10, ge=1, le=100, description="Maximum number of results"),
    offset: int = Query(default=0, ge=0, description="Number of results to skip")
):
    """Get all room uploads with pagination"""
    try:
        uploads = await room_upload_crud.get_all_room_uploads(limit=limit, offset=offset)
        return uploads
    except Exception as e:
        logger.error(f"Error getting room uploads: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{upload_id}", response_model=RoomUploadResponse)
async def update_room_upload(upload_id: UUID, upload_update: RoomUploadUpdate):
    """Update room upload by ID"""
    try:
        upload = await room_upload_crud.update_room_upload(upload_id, upload_update)
        if not upload:
            raise HTTPException(status_code=404, detail="Room upload not found")
        return upload
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating room upload {upload_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{upload_id}", status_code=204)
async def delete_room_upload(upload_id: UUID):
    """Delete room upload by ID"""
    try:
        success = await room_upload_crud.delete_room_upload(upload_id)
        if not success:
            raise HTTPException(status_code=404, detail="Room upload not found")
        return JSONResponse(content={"message": "Room upload deleted successfully"}, status_code=204)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting room upload {upload_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/user/{user_id}", status_code=200)
async def delete_room_uploads_by_user_id(user_id: UUID):
    """Delete all room uploads for a user"""
    try:
        deleted_count = await room_upload_crud.delete_room_uploads_by_user_id(user_id)
        return {
            "message": f"Deleted {deleted_count} room upload(s) for user",
            "deleted_count": deleted_count
        }
    except Exception as e:
        logger.error(f"Error deleting room uploads for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search", response_model=List[RoomUploadResponse])
async def search_room_uploads(search_params: RoomUploadSearch):
    """Search room uploads with filters"""
    try:
        uploads = await room_upload_crud.search_room_uploads(search_params)
        return uploads
    except Exception as e:
        logger.error(f"Error searching room uploads: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search/type/{room_type}", response_model=List[RoomUploadResponse])
async def get_room_uploads_by_type(
    room_type: str,
    limit: int = Query(default=10, ge=1, le=100, description="Maximum number of results"),
    offset: int = Query(default=0, ge=0, description="Number of results to skip")
):
    """Get room uploads by room type"""
    try:
        uploads = await room_upload_crud.get_room_uploads_by_type(room_type, limit=limit, offset=offset)
        return uploads
    except Exception as e:
        logger.error(f"Error getting room uploads by type: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats/count", response_model=dict)
async def get_room_upload_count(user_id: Optional[UUID] = Query(None, description="Optional user ID to filter by")):
    """Get total count of room uploads"""
    try:
        count = await room_upload_crud.count_room_uploads(user_id=user_id)
        return {
            "total_room_uploads": count,
            "user_id": str(user_id) if user_id else None
        }
    except Exception as e:
        logger.error(f"Error getting room upload count: {e}")
        raise HTTPException(status_code=500, detail=str(e))

