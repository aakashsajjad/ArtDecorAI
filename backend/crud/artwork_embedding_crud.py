"""
CRUD operations for artwork_embedding table
"""
from database import db_connection
from typing import List, Optional
from uuid import UUID
import logging
from datetime import datetime

from models.artwork_embedding import (
    ArtworkEmbeddingCreate,
    ArtworkEmbeddingUpdate,
    ArtworkEmbeddingResponse,
    ArtworkEmbeddingSearch
)

logger = logging.getLogger(__name__)


class ArtworkEmbeddingCRUD:
    """CRUD operations for artwork_embedding table"""
    
    def __init__(self):
        self.db = db_connection.client
        self.table_name = "artwork_embedding"
    
    async def create_embedding(self, embedding: ArtworkEmbeddingCreate) -> ArtworkEmbeddingResponse:
        """Create a new artwork embedding"""
        try:
            # Convert Pydantic model to dict
            embedding_data = embedding.model_dump()
            
            # Verify artwork exists
            artwork_check = self.db.table("artwork").select("id").eq("id", str(embedding_data["artwork_id"])).execute()
            if not artwork_check.data:
                raise ValueError(f"Artwork with ID {embedding_data['artwork_id']} not found")
            
            # Insert into database
            result = self.db.table(self.table_name).insert(embedding_data).execute()
            
            if not result.data:
                raise Exception("Failed to create artwork embedding")
            
            logger.info(f"Created artwork embedding: {result.data[0]['id']}")
            return ArtworkEmbeddingResponse(**result.data[0])
            
        except Exception as e:
            logger.error(f"Error creating artwork embedding: {e}")
            raise
    
    async def get_embedding_by_id(self, embedding_id: UUID) -> Optional[ArtworkEmbeddingResponse]:
        """Get artwork embedding by ID"""
        try:
            result = self.db.table(self.table_name).select("*").eq("id", str(embedding_id)).execute()
            
            if not result.data:
                logger.warning(f"Artwork embedding not found: {embedding_id}")
                return None
            
            return ArtworkEmbeddingResponse(**result.data[0])
            
        except Exception as e:
            logger.error(f"Error getting artwork embedding {embedding_id}: {e}")
            raise
    
    async def get_embedding_by_artwork_id(self, artwork_id: UUID) -> Optional[ArtworkEmbeddingResponse]:
        """Get artwork embedding by artwork ID"""
        try:
            result = self.db.table(self.table_name).select("*").eq("artwork_id", str(artwork_id)).execute()
            
            if not result.data:
                logger.warning(f"Artwork embedding not found for artwork: {artwork_id}")
                return None
            
            # Return the first embedding (assuming one embedding per artwork)
            return ArtworkEmbeddingResponse(**result.data[0])
            
        except Exception as e:
            logger.error(f"Error getting artwork embedding for artwork {artwork_id}: {e}")
            raise
    
    async def get_all_embeddings(self, limit: int = 10, offset: int = 0) -> List[ArtworkEmbeddingResponse]:
        """Get all artwork embeddings with pagination"""
        try:
            result = self.db.table(self.table_name).select("*").range(offset, offset + limit - 1).execute()
            
            embeddings = [ArtworkEmbeddingResponse(**item) for item in result.data]
            logger.info(f"Retrieved {len(embeddings)} artwork embeddings")
            return embeddings
            
        except Exception as e:
            logger.error(f"Error getting all artwork embeddings: {e}")
            raise
    
    async def update_embedding(self, embedding_id: UUID, embedding_update: ArtworkEmbeddingUpdate) -> Optional[ArtworkEmbeddingResponse]:
        """Update artwork embedding by ID"""
        try:
            # Convert to dict, excluding None values
            update_data = embedding_update.model_dump(exclude_unset=True)
            
            if not update_data:
                logger.warning(f"No fields to update for artwork embedding {embedding_id}")
                return await self.get_embedding_by_id(embedding_id)
            
            result = self.db.table(self.table_name).update(update_data).eq("id", str(embedding_id)).execute()
            
            if not result.data:
                logger.warning(f"Artwork embedding not found for update: {embedding_id}")
                return None
            
            logger.info(f"Updated artwork embedding: {embedding_id}")
            return ArtworkEmbeddingResponse(**result.data[0])
            
        except Exception as e:
            logger.error(f"Error updating artwork embedding {embedding_id}: {e}")
            raise
    
    async def delete_embedding(self, embedding_id: UUID) -> bool:
        """Delete artwork embedding by ID"""
        try:
            result = self.db.table(self.table_name).delete().eq("id", str(embedding_id)).execute()
            
            if not result.data:
                logger.warning(f"Artwork embedding not found for deletion: {embedding_id}")
                return False
            
            logger.info(f"Deleted artwork embedding: {embedding_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting artwork embedding {embedding_id}: {e}")
            raise
    
    async def delete_embedding_by_artwork_id(self, artwork_id: UUID) -> bool:
        """Delete artwork embedding by artwork ID"""
        try:
            result = self.db.table(self.table_name).delete().eq("artwork_id", str(artwork_id)).execute()
            
            if not result.data:
                logger.warning(f"Artwork embedding not found for artwork: {artwork_id}")
                return False
            
            logger.info(f"Deleted artwork embedding for artwork: {artwork_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting artwork embedding for artwork {artwork_id}: {e}")
            raise
    
    async def search_similar_embeddings(self, search_params: ArtworkEmbeddingSearch) -> List[dict]:
        """
        Search for similar artwork embeddings using vector similarity.
        
        Note: This uses PostgreSQL's vector similarity operators.
        The actual similarity calculation depends on your database configuration.
        """
        try:
            # Use RPC function if available, otherwise use direct query
            # First, try to use the match_artworks function if it exists
            try:
                result = self.db.rpc(
                    "match_artworks",
                    {
                        "query_embedding": search_params.query_vector,
                        "match_threshold": search_params.threshold,
                        "match_count": search_params.limit
                    }
                ).execute()
                
                if result.data:
                    logger.info(f"Found {len(result.data)} similar embeddings via RPC")
                    return result.data
            except Exception as e:
                logger.debug(f"RPC function not available, using direct query: {e}")
            
            # Fallback: Get all embeddings and calculate similarity (not efficient for large datasets)
            # In production, you should use the database's vector similarity search
            logger.warning("Using fallback similarity search - consider implementing proper vector search")
            
            # Get all embeddings (this is not efficient for large datasets)
            all_embeddings = self.db.table(self.table_name).select("*").limit(search_params.limit * 2).execute()
            
            # Calculate cosine similarity (simplified - should be done in database)
            similar_results = []
            for item in all_embeddings.data:
                # Calculate cosine similarity
                similarity = self._cosine_similarity(search_params.query_vector, item["vector"])
                
                if similarity >= search_params.threshold:
                    similar_results.append({
                        "id": item["id"],
                        "artwork_id": item["artwork_id"],
                        "vector": item["vector"],
                        "similarity": similarity,
                        "created_at": item["created_at"]
                    })
            
            # Sort by similarity and limit results
            similar_results.sort(key=lambda x: x["similarity"], reverse=True)
            similar_results = similar_results[:search_params.limit]
            
            logger.info(f"Found {len(similar_results)} similar embeddings")
            return similar_results
            
        except Exception as e:
            logger.error(f"Error searching similar embeddings: {e}")
            raise
    
    @staticmethod
    def _cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        if len(vec1) != len(vec2):
            raise ValueError("Vectors must have the same length")
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = sum(a * a for a in vec1) ** 0.5
        magnitude2 = sum(b * b for b in vec2) ** 0.5
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    async def count_embeddings(self) -> int:
        """Get total count of artwork embeddings"""
        try:
            result = self.db.table(self.table_name).select("id", count="exact").execute()
            count = result.count if hasattr(result, 'count') else len(result.data)
            logger.info(f"Total artwork embeddings count: {count}")
            return count
            
        except Exception as e:
            logger.error(f"Error counting artwork embeddings: {e}")
            raise


# Global CRUD instance
artwork_embedding_crud = ArtworkEmbeddingCRUD()

