"""
CRUD operations for user_profile table
"""
from database import db_connection
from typing import List, Optional, Dict, Any
from uuid import UUID
import logging
from datetime import datetime

from models.user_profile import (
    UserProfileCreate,
    UserProfileUpdate,
    UserProfileResponse,
    UserProfileSearch
)

logger = logging.getLogger(__name__)


class UserProfileCRUD:
    """CRUD operations for user_profile table"""
    
    def __init__(self):
        self.db = db_connection.client
        self.table_name = "user_profile"
    
    @staticmethod
    def _convert_decimals_to_primitives(value: Any) -> Any:
        """Recursively convert Decimal values to float so payload is JSON serializable."""
        from decimal import Decimal
        
        if isinstance(value, Decimal):
            return float(value)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return float(value) if isinstance(value, (int, float)) else value
        if isinstance(value, list):
            return [UserProfileCRUD._convert_decimals_to_primitives(item) for item in value]
        if isinstance(value, dict):
            return {k: UserProfileCRUD._convert_decimals_to_primitives(v) for k, v in value.items()}
        return value
    
    async def create_user_profile(self, profile: UserProfileCreate) -> UserProfileResponse:
        """Create a new user profile"""
        try:
            # Convert Pydantic model to dict
            profile_data = profile.model_dump()
            
            # Ensure all values are JSON serializable
            profile_data = self._convert_decimals_to_primitives(profile_data)
            
            # Insert into database
            result = self.db.table(self.table_name).insert(profile_data).execute()
            
            if not result.data:
                raise Exception("Failed to create user profile")
            
            logger.info(f"Created user profile: {result.data[0]['id']} for user: {profile_data['user_id']}")
            return UserProfileResponse(**result.data[0])
            
        except Exception as e:
            logger.error(f"Error creating user profile: {e}")
            raise
    
    async def get_user_profile_by_id(self, profile_id: UUID) -> Optional[UserProfileResponse]:
        """Get user profile by ID"""
        try:
            result = self.db.table(self.table_name).select("*").eq("id", str(profile_id)).execute()
            
            if not result.data:
                logger.warning(f"User profile not found: {profile_id}")
                return None
            
            return UserProfileResponse(**result.data[0])
            
        except Exception as e:
            logger.error(f"Error getting user profile {profile_id}: {e}")
            raise
    
    async def get_user_profile_by_user_id(self, user_id: UUID) -> Optional[UserProfileResponse]:
        """Get user profile by user ID"""
        try:
            result = self.db.table(self.table_name).select("*").eq("user_id", str(user_id)).execute()
            
            if not result.data:
                logger.warning(f"User profile not found for user: {user_id}")
                return None
            
            # Return the first profile (user_id is unique)
            return UserProfileResponse(**result.data[0])
            
        except Exception as e:
            logger.error(f"Error getting user profile for user {user_id}: {e}")
            raise
    
    async def get_all_user_profiles(self, limit: int = 10, offset: int = 0) -> List[UserProfileResponse]:
        """Get all user profiles with pagination"""
        try:
            result = self.db.table(self.table_name).select("*").range(offset, offset + limit - 1).execute()
            
            profiles = [UserProfileResponse(**item) for item in result.data]
            logger.info(f"Retrieved {len(profiles)} user profiles")
            return profiles
            
        except Exception as e:
            logger.error(f"Error getting all user profiles: {e}")
            raise
    
    async def update_user_profile(self, profile_id: UUID, profile_update: UserProfileUpdate) -> Optional[UserProfileResponse]:
        """Update user profile by ID"""
        try:
            # Convert to dict, excluding None values
            update_data = profile_update.model_dump(exclude_unset=True)
            
            if not update_data:
                logger.warning(f"No fields to update for user profile {profile_id}")
                return await self.get_user_profile_by_id(profile_id)
            
            # Ensure all values are JSON serializable
            update_data = self._convert_decimals_to_primitives(update_data)
            
            # Add updated_at timestamp
            update_data["updated_at"] = datetime.utcnow().isoformat()
            
            result = self.db.table(self.table_name).update(update_data).eq("id", str(profile_id)).execute()
            
            if not result.data:
                logger.warning(f"User profile not found for update: {profile_id}")
                return None
            
            logger.info(f"Updated user profile: {profile_id}")
            return UserProfileResponse(**result.data[0])
            
        except Exception as e:
            logger.error(f"Error updating user profile {profile_id}: {e}")
            raise
    
    async def update_user_profile_by_user_id(self, user_id: UUID, profile_update: UserProfileUpdate) -> Optional[UserProfileResponse]:
        """Update user profile by user ID"""
        try:
            # Convert to dict, excluding None values
            update_data = profile_update.model_dump(exclude_unset=True)
            
            if not update_data:
                logger.warning(f"No fields to update for user profile {user_id}")
                return await self.get_user_profile_by_user_id(user_id)
            
            # Ensure all values are JSON serializable
            update_data = self._convert_decimals_to_primitives(update_data)
            
            # Add updated_at timestamp
            update_data["updated_at"] = datetime.utcnow().isoformat()
            
            result = self.db.table(self.table_name).update(update_data).eq("user_id", str(user_id)).execute()
            
            if not result.data:
                logger.warning(f"User profile not found for update: {user_id}")
                return None
            
            logger.info(f"Updated user profile for user: {user_id}")
            return UserProfileResponse(**result.data[0])
            
        except Exception as e:
            logger.error(f"Error updating user profile for user {user_id}: {e}")
            raise
    
    async def upsert_user_profile(self, profile: UserProfileCreate) -> UserProfileResponse:
        """Upsert (insert or update) user profile by user_id"""
        try:
            # Convert Pydantic model to dict
            profile_data = profile.model_dump()
            
            # Ensure all values are JSON serializable
            profile_data = self._convert_decimals_to_primitives(profile_data)
            
            # Use upsert to insert or update
            result = self.db.table(self.table_name).upsert(
                profile_data,
                on_conflict="user_id"
            ).execute()
            
            if not result.data:
                raise Exception("Failed to upsert user profile")
            
            logger.info(f"Upserted user profile for user: {profile_data['user_id']}")
            return UserProfileResponse(**result.data[0])
            
        except Exception as e:
            logger.error(f"Error upserting user profile: {e}")
            raise
    
    async def delete_user_profile(self, profile_id: UUID) -> bool:
        """Delete user profile by ID"""
        try:
            result = self.db.table(self.table_name).delete().eq("id", str(profile_id)).execute()
            
            if not result.data:
                logger.warning(f"User profile not found for deletion: {profile_id}")
                return False
            
            logger.info(f"Deleted user profile: {profile_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting user profile {profile_id}: {e}")
            raise
    
    async def delete_user_profile_by_user_id(self, user_id: UUID) -> bool:
        """Delete user profile by user ID"""
        try:
            result = self.db.table(self.table_name).delete().eq("user_id", str(user_id)).execute()
            
            if not result.data:
                logger.warning(f"User profile not found for user: {user_id}")
                return False
            
            logger.info(f"Deleted user profile for user: {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting user profile for user {user_id}: {e}")
            raise
    
    async def search_user_profiles(self, search_params: UserProfileSearch) -> List[UserProfileResponse]:
        """Search user profiles with filters"""
        try:
            query = self.db.table(self.table_name).select("*")
            
            # Apply filters
            if search_params.preferred_styles:
                query = query.overlaps("preferred_styles", search_params.preferred_styles)
            
            if search_params.has_color_profile is not None:
                if search_params.has_color_profile:
                    query = query.not_.is_("color_profile_json", "null")
                else:
                    query = query.is_("color_profile_json", "null")
            
            if search_params.has_budget_range is not None:
                if search_params.has_budget_range:
                    query = query.not_.is_("budget_range", "null")
                else:
                    query = query.is_("budget_range", "null")
            
            # Apply pagination
            query = query.range(search_params.offset, search_params.offset + search_params.limit - 1)
            
            result = query.execute()
            profiles = [UserProfileResponse(**item) for item in result.data]
            
            logger.info(f"Found {len(profiles)} user profiles matching search criteria")
            return profiles
            
        except Exception as e:
            logger.error(f"Error searching user profiles: {e}")
            raise
    
    async def get_user_profiles_by_style(self, style_tags: List[str]) -> List[UserProfileResponse]:
        """Get user profiles by preferred styles"""
        try:
            result = self.db.table(self.table_name).select("*").overlaps("preferred_styles", style_tags).execute()
            
            profiles = [UserProfileResponse(**item) for item in result.data]
            logger.info(f"Found {len(profiles)} user profiles with styles: {style_tags}")
            return profiles
            
        except Exception as e:
            logger.error(f"Error getting user profiles by style: {e}")
            raise
    
    async def count_user_profiles(self) -> int:
        """Get total count of user profiles"""
        try:
            result = self.db.table(self.table_name).select("id", count="exact").execute()
            count = result.count if hasattr(result, 'count') else len(result.data)
            logger.info(f"Total user profiles count: {count}")
            return count
            
        except Exception as e:
            logger.error(f"Error counting user profiles: {e}")
            raise


# Global CRUD instance
user_profile_crud = UserProfileCRUD()

