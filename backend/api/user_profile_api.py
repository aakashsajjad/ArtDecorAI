"""
FastAPI routes for user profile operations
"""
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
import logging

from models.user_profile import (
    UserProfileCreate,
    UserProfileUpdate,
    UserProfileResponse,
    UserProfileSearch
)
from crud.user_profile_crud import user_profile_crud

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/user-profiles", tags=["user-profiles"])


@router.post("/", response_model=UserProfileResponse, status_code=201)
async def create_user_profile(profile: UserProfileCreate):
    """Create a new user profile"""
    try:
        result = await user_profile_crud.create_user_profile(profile)
        return result
    except Exception as e:
        logger.error(f"Error creating user profile: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{profile_id}", response_model=UserProfileResponse)
async def get_user_profile(profile_id: UUID):
    """Get user profile by ID"""
    try:
        profile = await user_profile_crud.get_user_profile_by_id(profile_id)
        if not profile:
            raise HTTPException(status_code=404, detail="User profile not found")
        return profile
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user profile {profile_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user/{user_id}", response_model=UserProfileResponse)
async def get_user_profile_by_user_id(user_id: UUID):
    """Get user profile by user ID"""
    try:
        profile = await user_profile_crud.get_user_profile_by_user_id(user_id)
        if not profile:
            raise HTTPException(status_code=404, detail="User profile not found for this user")
        return profile
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user profile for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[UserProfileResponse])
async def get_user_profiles(
    limit: int = Query(default=10, ge=1, le=100, description="Maximum number of results"),
    offset: int = Query(default=0, ge=0, description="Number of results to skip")
):
    """Get all user profiles with pagination"""
    try:
        profiles = await user_profile_crud.get_all_user_profiles(limit=limit, offset=offset)
        return profiles
    except Exception as e:
        logger.error(f"Error getting user profiles: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{profile_id}", response_model=UserProfileResponse)
async def update_user_profile(profile_id: UUID, profile_update: UserProfileUpdate):
    """Update user profile by ID"""
    try:
        profile = await user_profile_crud.update_user_profile(profile_id, profile_update)
        if not profile:
            raise HTTPException(status_code=404, detail="User profile not found")
        return profile
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user profile {profile_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/user/{user_id}", response_model=UserProfileResponse)
async def update_user_profile_by_user_id(user_id: UUID, profile_update: UserProfileUpdate):
    """Update user profile by user ID"""
    try:
        profile = await user_profile_crud.update_user_profile_by_user_id(user_id, profile_update)
        if not profile:
            raise HTTPException(status_code=404, detail="User profile not found for this user")
        return profile
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user profile for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upsert", response_model=UserProfileResponse)
async def upsert_user_profile(profile: UserProfileCreate):
    """Upsert (insert or update) user profile by user_id
    
    This is useful when you want to create or update a profile in one operation.
    """
    try:
        result = await user_profile_crud.upsert_user_profile(profile)
        return result
    except Exception as e:
        logger.error(f"Error upserting user profile: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{profile_id}", status_code=204)
async def delete_user_profile(profile_id: UUID):
    """Delete user profile by ID"""
    try:
        success = await user_profile_crud.delete_user_profile(profile_id)
        if not success:
            raise HTTPException(status_code=404, detail="User profile not found")
        return JSONResponse(content={"message": "User profile deleted successfully"}, status_code=204)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting user profile {profile_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/user/{user_id}", status_code=204)
async def delete_user_profile_by_user_id(user_id: UUID):
    """Delete user profile by user ID"""
    try:
        success = await user_profile_crud.delete_user_profile_by_user_id(user_id)
        if not success:
            raise HTTPException(status_code=404, detail="User profile not found for this user")
        return JSONResponse(content={"message": "User profile deleted successfully"}, status_code=204)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting user profile for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search", response_model=List[UserProfileResponse])
async def search_user_profiles(search_params: UserProfileSearch):
    """Search user profiles with filters"""
    try:
        profiles = await user_profile_crud.search_user_profiles(search_params)
        return profiles
    except Exception as e:
        logger.error(f"Error searching user profiles: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search/style", response_model=List[UserProfileResponse])
async def get_user_profiles_by_style(
    style_tags: List[str] = Query(..., description="Style tags to search for")
):
    """Get user profiles by preferred style tags"""
    try:
        profiles = await user_profile_crud.get_user_profiles_by_style(style_tags)
        return profiles
    except Exception as e:
        logger.error(f"Error getting user profiles by style: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats/count", response_model=dict)
async def get_user_profile_count():
    """Get total count of user profiles"""
    try:
        count = await user_profile_crud.count_user_profiles()
        return {"total_user_profiles": count}
    except Exception as e:
        logger.error(f"Error getting user profile count: {e}")
        raise HTTPException(status_code=500, detail=str(e))

