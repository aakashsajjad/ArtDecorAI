"""
CRUD operations for session table
"""
from database import db_connection
from typing import List, Optional
from uuid import UUID
import logging
from datetime import datetime

from models.session import (
    SessionCreate,
    SessionUpdate,
    SessionResponse,
    SessionSearch
)

logger = logging.getLogger(__name__)


class SessionCRUD:
    """CRUD operations for session table"""
    
    def __init__(self):
        self.db = db_connection.client
        self.table_name = "session"
    
    @staticmethod
    def _convert_uuid_list(uuid_list: Optional[List[UUID]]) -> Optional[List[str]]:
        """Convert list of UUIDs to list of strings for database storage"""
        if uuid_list is None:
            return None
        return [str(uuid) for uuid in uuid_list]
    
    async def create_session(self, session: SessionCreate) -> SessionResponse:
        """Create a new session"""
        try:
            # Convert Pydantic model to dict
            session_data = session.model_dump()
            
            # Convert UUID lists to string lists for database
            if session_data.get("topk_ids") is not None:
                session_data["topk_ids"] = self._convert_uuid_list(session_data["topk_ids"])
            
            # Convert UUID to string if present
            if session_data.get("chosen_id") is not None:
                session_data["chosen_id"] = str(session_data["chosen_id"])
            
            if session_data.get("user_id") is not None:
                session_data["user_id"] = str(session_data["user_id"])
            
            # Insert into database
            result = self.db.table(self.table_name).insert(session_data).execute()
            
            if not result.data:
                raise Exception("Failed to create session")
            
            logger.info(f"Created session: {result.data[0]['id']} for user: {session_data['user_id']}")
            return SessionResponse(**result.data[0])
            
        except Exception as e:
            logger.error(f"Error creating session: {e}")
            raise
    
    async def get_session_by_id(self, session_id: UUID) -> Optional[SessionResponse]:
        """Get session by ID"""
        try:
            result = self.db.table(self.table_name).select("*").eq("id", str(session_id)).execute()
            
            if not result.data:
                logger.warning(f"Session not found: {session_id}")
                return None
            
            return SessionResponse(**result.data[0])
            
        except Exception as e:
            logger.error(f"Error getting session {session_id}: {e}")
            raise
    
    async def get_sessions_by_user_id(self, user_id: UUID, limit: int = 10, offset: int = 0) -> List[SessionResponse]:
        """Get sessions by user ID with pagination"""
        try:
            result = (
                self.db.table(self.table_name)
                .select("*")
                .eq("user_id", str(user_id))
                .order("created_at", desc=True)
                .range(offset, offset + limit - 1)
                .execute()
            )
            
            sessions = [SessionResponse(**item) for item in result.data]
            logger.info(f"Retrieved {len(sessions)} sessions for user {user_id}")
            return sessions
            
        except Exception as e:
            logger.error(f"Error getting sessions for user {user_id}: {e}")
            raise
    
    async def get_all_sessions(self, limit: int = 10, offset: int = 0) -> List[SessionResponse]:
        """Get all sessions with pagination"""
        try:
            result = (
                self.db.table(self.table_name)
                .select("*")
                .order("created_at", desc=True)
                .range(offset, offset + limit - 1)
                .execute()
            )
            
            sessions = [SessionResponse(**item) for item in result.data]
            logger.info(f"Retrieved {len(sessions)} sessions")
            return sessions
            
        except Exception as e:
            logger.error(f"Error getting all sessions: {e}")
            raise
    
    async def update_session(self, session_id: UUID, session_update: SessionUpdate) -> Optional[SessionResponse]:
        """Update session by ID"""
        try:
            # Convert to dict, excluding None values
            update_data = session_update.model_dump(exclude_unset=True)
            
            if not update_data:
                logger.warning(f"No fields to update for session {session_id}")
                return await self.get_session_by_id(session_id)
            
            # Convert UUID lists to string lists for database
            if "topk_ids" in update_data and update_data["topk_ids"] is not None:
                update_data["topk_ids"] = self._convert_uuid_list(update_data["topk_ids"])
            
            # Convert UUID to string if present
            if "chosen_id" in update_data and update_data["chosen_id"] is not None:
                update_data["chosen_id"] = str(update_data["chosen_id"])
            
            result = self.db.table(self.table_name).update(update_data).eq("id", str(session_id)).execute()
            
            if not result.data:
                logger.warning(f"Session not found for update: {session_id}")
                return None
            
            logger.info(f"Updated session: {session_id}")
            return SessionResponse(**result.data[0])
            
        except Exception as e:
            logger.error(f"Error updating session {session_id}: {e}")
            raise
    
    async def delete_session(self, session_id: UUID) -> bool:
        """Delete session by ID"""
        try:
            result = self.db.table(self.table_name).delete().eq("id", str(session_id)).execute()
            
            if not result.data:
                logger.warning(f"Session not found for deletion: {session_id}")
                return False
            
            logger.info(f"Deleted session: {session_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting session {session_id}: {e}")
            raise
    
    async def delete_sessions_by_user_id(self, user_id: UUID) -> int:
        """Delete all sessions for a user"""
        try:
            result = self.db.table(self.table_name).delete().eq("user_id", str(user_id)).execute()
            
            deleted_count = len(result.data) if result.data else 0
            logger.info(f"Deleted {deleted_count} sessions for user: {user_id}")
            return deleted_count
            
        except Exception as e:
            logger.error(f"Error deleting sessions for user {user_id}: {e}")
            raise
    
    async def search_sessions(self, search_params: SessionSearch) -> List[SessionResponse]:
        """Search sessions with filters"""
        try:
            query = self.db.table(self.table_name).select("*")
            
            # Apply filters
            if search_params.user_id:
                query = query.eq("user_id", str(search_params.user_id))
            
            if search_params.has_chosen_id is not None:
                if search_params.has_chosen_id:
                    query = query.not_.is_("chosen_id", "null")
                else:
                    query = query.is_("chosen_id", "null")
            
            if search_params.has_topk_ids is not None:
                if search_params.has_topk_ids:
                    query = query.not_.is_("topk_ids", "null")
                else:
                    query = query.is_("topk_ids", "null")
            
            if search_params.has_rationale is not None:
                if search_params.has_rationale:
                    query = query.not_.is_("rationale", "null")
                else:
                    query = query.is_("rationale", "null")
            
            # Apply pagination and ordering
            query = query.order("created_at", desc=True).range(
                search_params.offset, 
                search_params.offset + search_params.limit - 1
            )
            
            result = query.execute()
            sessions = [SessionResponse(**item) for item in result.data]
            
            logger.info(f"Found {len(sessions)} sessions matching search criteria")
            return sessions
            
        except Exception as e:
            logger.error(f"Error searching sessions: {e}")
            raise
    
    async def get_sessions_with_chosen_artwork(self, user_id: Optional[UUID] = None, limit: int = 10, offset: int = 0) -> List[SessionResponse]:
        """Get sessions where user has chosen an artwork"""
        try:
            query = self.db.table(self.table_name).select("*").not_.is_("chosen_id", "null")
            
            if user_id:
                query = query.eq("user_id", str(user_id))
            
            result = (
                query
                .order("created_at", desc=True)
                .range(offset, offset + limit - 1)
                .execute()
            )
            
            sessions = [SessionResponse(**item) for item in result.data]
            logger.info(f"Found {len(sessions)} sessions with chosen artwork" + (f" for user {user_id}" if user_id else ""))
            return sessions
            
        except Exception as e:
            logger.error(f"Error getting sessions with chosen artwork: {e}")
            raise
    
    async def count_sessions(self, user_id: Optional[UUID] = None) -> int:
        """Get total count of sessions"""
        try:
            query = self.db.table(self.table_name).select("id", count="exact")
            
            if user_id:
                query = query.eq("user_id", str(user_id))
            
            result = query.execute()
            count = result.count if hasattr(result, 'count') else len(result.data)
            logger.info(f"Total sessions count: {count}" + (f" for user {user_id}" if user_id else ""))
            return count
            
        except Exception as e:
            logger.error(f"Error counting sessions: {e}")
            raise


# Global CRUD instance
session_crud = SessionCRUD()

