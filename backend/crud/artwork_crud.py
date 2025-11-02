"""
CRUD operations for artwork table
"""
from database import db_connection
from typing import List, Optional, Dict, Any
from uuid import UUID
from decimal import Decimal
import logging
from datetime import datetime

from database import db_connection
from models.artwork import ArtworkCreate, ArtworkUpdate, ArtworkResponse, ArtworkSearch, ArtworkFilter

logger = logging.getLogger(__name__)

class ArtworkCRUD:
    """CRUD operations for artwork table"""
    
    def __init__(self):
        self.db = db_connection.client
        self.table_name = "artwork"
    
    @staticmethod
    def _convert_decimals_to_primitives(value: Any) -> Any:
        """Recursively convert Decimal values to float so payload is JSON serializable."""
        if isinstance(value, Decimal):
            return float(value)
        if isinstance(value, list):
            return [ArtworkCRUD._convert_decimals_to_primitives(item) for item in value]
        if isinstance(value, dict):
            return {k: ArtworkCRUD._convert_decimals_to_primitives(v) for k, v in value.items()}
        return value
    
    async def create_artwork(self, artwork: ArtworkCreate) -> ArtworkResponse:
        """Create a new artwork"""
        try:
            # Convert Pydantic model to dict
            artwork_data = artwork.model_dump()
            # Ensure all Decimal values are JSON serializable
            artwork_data = self._convert_decimals_to_primitives(artwork_data)
            
            # Insert into database
            result = self.db.table(self.table_name).insert(artwork_data).execute()
            
            if not result.data:
                raise Exception("Failed to create artwork")
            
            logger.info(f"Created artwork: {result.data[0]['id']}")
            return ArtworkResponse(**result.data[0])
            
        except Exception as e:
            logger.error(f"Error creating artwork: {e}")
            raise
    
    async def get_artwork_by_id(self, artwork_id: UUID) -> Optional[ArtworkResponse]:
        """Get artwork by ID"""
        try:
            result = self.db.table(self.table_name).select("*").eq("id", str(artwork_id)).execute()
            
            if not result.data:
                logger.warning(f"Artwork not found: {artwork_id}")
                return None
            
            return ArtworkResponse(**result.data[0])
            
        except Exception as e:
            logger.error(f"Error getting artwork {artwork_id}: {e}")
            raise
    
    async def get_all_artworks(self, limit: int = 10, offset: int = 0) -> List[ArtworkResponse]:
        """Get all artworks with pagination"""
        try:
            result = self.db.table(self.table_name).select("*").range(offset, offset + limit - 1).execute()
            
            artworks = [ArtworkResponse(**item) for item in result.data]
            logger.info(f"Retrieved {len(artworks)} artworks")
            return artworks
            
        except Exception as e:
            logger.error(f"Error getting all artworks: {e}")
            raise
    
    async def update_artwork(self, artwork_id: UUID, artwork_update: ArtworkUpdate) -> Optional[ArtworkResponse]:
        """Update artwork by ID"""
        try:
            # Convert to dict, excluding None values
            update_data = artwork_update.model_dump(exclude_unset=True)
            
            if not update_data:
                logger.warning(f"No fields to update for artwork {artwork_id}")
                return await self.get_artwork_by_id(artwork_id)
            
            # Add updated_at timestamp
            update_data["updated_at"] = datetime.utcnow().isoformat()
            
            result = self.db.table(self.table_name).update(update_data).eq("id", str(artwork_id)).execute()
            
            if not result.data:
                logger.warning(f"Artwork not found for update: {artwork_id}")
                return None
            
            logger.info(f"Updated artwork: {artwork_id}")
            return ArtworkResponse(**result.data[0])
            
        except Exception as e:
            logger.error(f"Error updating artwork {artwork_id}: {e}")
            raise
    
    async def delete_artwork(self, artwork_id: UUID) -> bool:
        """Delete artwork by ID"""
        try:
            result = self.db.table(self.table_name).delete().eq("id", str(artwork_id)).execute()
            
            if not result.data:
                logger.warning(f"Artwork not found for deletion: {artwork_id}")
                return False
            
            logger.info(f"Deleted artwork: {artwork_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting artwork {artwork_id}: {e}")
            raise
    
    async def search_artworks(self, search_params: ArtworkSearch) -> List[ArtworkResponse]:
        """Search artworks with filters"""
        try:
            query = self.db.table(self.table_name).select("*")
            
            # Apply filters
            if search_params.style_tags:
                query = query.overlaps("style_tags", search_params.style_tags)
            
            if search_params.brand:
                query = query.eq("brand", search_params.brand)
            
            if search_params.min_price is not None:
                query = query.gte("price", float(search_params.min_price))
            
            if search_params.max_price is not None:
                query = query.lte("price", float(search_params.max_price))
            
            # Apply pagination
            query = query.range(search_params.offset, search_params.offset + search_params.limit - 1)
            
            result = query.execute()
            artworks = [ArtworkResponse(**item) for item in result.data]
            
            logger.info(f"Found {len(artworks)} artworks matching search criteria")
            return artworks
            
        except Exception as e:
            logger.error(f"Error searching artworks: {e}")
            raise
    
    async def get_artworks_by_style(self, style_tags: List[str]) -> List[ArtworkResponse]:
        """Get artworks by style tags"""
        try:
            result = self.db.table(self.table_name).select("*").overlaps("style_tags", style_tags).execute()
            
            artworks = [ArtworkResponse(**item) for item in result.data]
            logger.info(f"Found {len(artworks)} artworks with styles: {style_tags}")
            return artworks
            
        except Exception as e:
            logger.error(f"Error getting artworks by style: {e}")
            raise
    
    async def get_artworks_by_price_range(self, min_price: Decimal, max_price: Decimal) -> List[ArtworkResponse]:
        """Get artworks within price range"""
        try:
            result = self.db.table(self.table_name).select("*").gte("price", float(min_price)).lte("price", float(max_price)).execute()
            
            artworks = [ArtworkResponse(**item) for item in result.data]
            logger.info(f"Found {len(artworks)} artworks in price range ${min_price}-${max_price}")
            return artworks
            
        except Exception as e:
            logger.error(f"Error getting artworks by price range: {e}")
            raise
    
    async def get_artworks_by_brand(self, brand: str) -> List[ArtworkResponse]:
        """Get artworks by brand"""
        try:
            result = self.db.table(self.table_name).select("*").eq("brand", brand).execute()
            
            artworks = [ArtworkResponse(**item) for item in result.data]
            logger.info(f"Found {len(artworks)} artworks by brand: {brand}")
            return artworks
            
        except Exception as e:
            logger.error(f"Error getting artworks by brand: {e}")
            raise
    
    async def count_artworks(self) -> int:
        """Get total count of artworks"""
        try:
            result = self.db.table(self.table_name).select("id", count="exact").execute()
            count = result.count if hasattr(result, 'count') else len(result.data)
            logger.info(f"Total artworks count: {count}")
            return count
            
        except Exception as e:
            logger.error(f"Error counting artworks: {e}")
            raise
    
    async def get_recent_artworks(self, limit: int = 5) -> List[ArtworkResponse]:
        """Get recently added artworks"""
        try:
            result = self.db.table(self.table_name).select("*").order("created_at", desc=True).limit(limit).execute()
            
            artworks = [ArtworkResponse(**item) for item in result.data]
            logger.info(f"Retrieved {len(artworks)} recent artworks")
            return artworks
            
        except Exception as e:
            logger.error(f"Error getting recent artworks: {e}")
            raise

# Global CRUD instance
artwork_crud = ArtworkCRUD()
