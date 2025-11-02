"""
CRUD operations for room_upload table
"""
from database import db_connection
from typing import List, Optional, Dict, Any
from uuid import UUID
import logging
from datetime import datetime

from models.room_upload import (
    RoomUploadCreate,
    RoomUploadUpdate,
    RoomUploadResponse,
    RoomUploadSearch
)

logger = logging.getLogger(__name__)


class RoomUploadCRUD:
    """CRUD operations for room_upload table"""
    
    def __init__(self):
        self.db = db_connection.client
        self.table_name = "room_upload"
    
    @staticmethod
    def _convert_decimals_to_primitives(value: Any) -> Any:
        """Recursively convert Decimal values to float so payload is JSON serializable."""
        from decimal import Decimal
        
        if isinstance(value, Decimal):
            return float(value)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return float(value) if isinstance(value, (int, float)) else value
        if isinstance(value, list):
            return [RoomUploadCRUD._convert_decimals_to_primitives(item) for item in value]
        if isinstance(value, dict):
            return {k: RoomUploadCRUD._convert_decimals_to_primitives(v) for k, v in value.items()}
        return value
    
    async def create_room_upload(self, room_upload: RoomUploadCreate) -> RoomUploadResponse:
        """Create a new room upload"""
        try:
            # Convert Pydantic model to dict
            upload_data = room_upload.model_dump()
            
            # Ensure all values are JSON serializable
            upload_data = self._convert_decimals_to_primitives(upload_data)
            
            # Insert into database
            result = self.db.table(self.table_name).insert(upload_data).execute()
            
            if not result.data:
                raise Exception("Failed to create room upload")
            
            logger.info(f"Created room upload: {result.data[0]['id']} for user: {upload_data['user_id']}")
            return RoomUploadResponse(**result.data[0])
            
        except Exception as e:
            logger.error(f"Error creating room upload: {e}")
            raise
    
    async def get_room_upload_by_id(self, upload_id: UUID) -> Optional[RoomUploadResponse]:
        """Get room upload by ID"""
        try:
            result = self.db.table(self.table_name).select("*").eq("id", str(upload_id)).execute()
            
            if not result.data:
                logger.warning(f"Room upload not found: {upload_id}")
                return None
            
            return RoomUploadResponse(**result.data[0])
            
        except Exception as e:
            logger.error(f"Error getting room upload {upload_id}: {e}")
            raise
    
    async def get_room_uploads_by_user_id(self, user_id: UUID, limit: int = 10, offset: int = 0) -> List[RoomUploadResponse]:
        """Get room uploads by user ID with pagination"""
        try:
            result = (
                self.db.table(self.table_name)
                .select("*")
                .eq("user_id", str(user_id))
                .order("created_at", desc=True)
                .range(offset, offset + limit - 1)
                .execute()
            )
            
            uploads = [RoomUploadResponse(**item) for item in result.data]
            logger.info(f"Retrieved {len(uploads)} room uploads for user {user_id}")
            return uploads
            
        except Exception as e:
            logger.error(f"Error getting room uploads for user {user_id}: {e}")
            raise
    
    async def get_all_room_uploads(self, limit: int = 10, offset: int = 0) -> List[RoomUploadResponse]:
        """Get all room uploads with pagination"""
        try:
            result = (
                self.db.table(self.table_name)
                .select("*")
                .order("created_at", desc=True)
                .range(offset, offset + limit - 1)
                .execute()
            )
            
            uploads = [RoomUploadResponse(**item) for item in result.data]
            logger.info(f"Retrieved {len(uploads)} room uploads")
            return uploads
            
        except Exception as e:
            logger.error(f"Error getting all room uploads: {e}")
            raise
    
    async def update_room_upload(self, upload_id: UUID, upload_update: RoomUploadUpdate) -> Optional[RoomUploadResponse]:
        """Update room upload by ID"""
        try:
            # Convert to dict, excluding None values
            update_data = upload_update.model_dump(exclude_unset=True)
            
            if not update_data:
                logger.warning(f"No fields to update for room upload {upload_id}")
                return await self.get_room_upload_by_id(upload_id)
            
            # Ensure all values are JSON serializable
            update_data = self._convert_decimals_to_primitives(update_data)
            
            result = self.db.table(self.table_name).update(update_data).eq("id", str(upload_id)).execute()
            
            if not result.data:
                logger.warning(f"Room upload not found for update: {upload_id}")
                return None
            
            logger.info(f"Updated room upload: {upload_id}")
            return RoomUploadResponse(**result.data[0])
            
        except Exception as e:
            logger.error(f"Error updating room upload {upload_id}: {e}")
            raise
    
    async def delete_room_upload(self, upload_id: UUID) -> bool:
        """Delete room upload by ID"""
        try:
            result = self.db.table(self.table_name).delete().eq("id", str(upload_id)).execute()
            
            if not result.data:
                logger.warning(f"Room upload not found for deletion: {upload_id}")
                return False
            
            logger.info(f"Deleted room upload: {upload_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting room upload {upload_id}: {e}")
            raise
    
    async def delete_room_uploads_by_user_id(self, user_id: UUID) -> int:
        """Delete all room uploads for a user"""
        try:
            result = self.db.table(self.table_name).delete().eq("user_id", str(user_id)).execute()
            
            deleted_count = len(result.data) if result.data else 0
            logger.info(f"Deleted {deleted_count} room uploads for user: {user_id}")
            return deleted_count
            
        except Exception as e:
            logger.error(f"Error deleting room uploads for user {user_id}: {e}")
            raise
    
    async def search_room_uploads(self, search_params: RoomUploadSearch) -> List[RoomUploadResponse]:
        """Search room uploads with filters"""
        try:
            query = self.db.table(self.table_name).select("*")
            
            # Apply filters
            if search_params.user_id:
                query = query.eq("user_id", str(search_params.user_id))
            
            if search_params.room_type:
                query = query.eq("room_type", search_params.room_type)
            
            if search_params.has_palette is not None:
                if search_params.has_palette:
                    query = query.not_.is_("palette_json", "null")
                else:
                    query = query.is_("palette_json", "null")
            
            if search_params.has_lighting is not None:
                if search_params.has_lighting:
                    query = query.not_.is_("lighting_json", "null")
                else:
                    query = query.is_("lighting_json", "null")
            
            # Apply pagination and ordering
            query = query.order("created_at", desc=True).range(
                search_params.offset, 
                search_params.offset + search_params.limit - 1
            )
            
            result = query.execute()
            uploads = [RoomUploadResponse(**item) for item in result.data]
            
            logger.info(f"Found {len(uploads)} room uploads matching search criteria")
            return uploads
            
        except Exception as e:
            logger.error(f"Error searching room uploads: {e}")
            raise
    
    async def get_room_uploads_by_type(self, room_type: str, limit: int = 10, offset: int = 0) -> List[RoomUploadResponse]:
        """Get room uploads by room type"""
        try:
            result = (
                self.db.table(self.table_name)
                .select("*")
                .eq("room_type", room_type)
                .order("created_at", desc=True)
                .range(offset, offset + limit - 1)
                .execute()
            )
            
            uploads = [RoomUploadResponse(**item) for item in result.data]
            logger.info(f"Found {len(uploads)} room uploads of type: {room_type}")
            return uploads
            
        except Exception as e:
            logger.error(f"Error getting room uploads by type: {e}")
            raise
    
    async def count_room_uploads(self, user_id: Optional[UUID] = None) -> int:
        """Get total count of room uploads"""
        try:
            query = self.db.table(self.table_name).select("id", count="exact")
            
            if user_id:
                query = query.eq("user_id", str(user_id))
            
            result = query.execute()
            count = result.count if hasattr(result, 'count') else len(result.data)
            logger.info(f"Total room uploads count: {count}" + (f" for user {user_id}" if user_id else ""))
            return count
            
        except Exception as e:
            logger.error(f"Error counting room uploads: {e}")
            raise


# Global CRUD instance
room_upload_crud = RoomUploadCRUD()

