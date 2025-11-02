"""
Database connection and configuration for ArtDecorAI
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from backend/.env if present
try:
    backend_env_path = Path(__file__).resolve().parent / ".env"
    load_dotenv(dotenv_path=backend_env_path, override=False)
    logger.info(f"Loaded environment variables from {backend_env_path}")
except Exception as e:
    logger.warning(f"Could not load .env file: {e}")

class DatabaseConnection:
    """Database connection manager for Supabase"""
    
    def __init__(self):
        # Prefer explicit backend envs; fall back to frontend ones if present
        raw_url = (
            os.getenv("SUPABASE_URL")
            or os.getenv("NEXT_PUBLIC_SUPABASE_URL")
            or "https://zcgjlmdvztxakwubrjyg.supabase.co"
        )
        raw_key = (
            os.getenv("SUPABASE_SERVICE_ROLE_KEY")  # allow service role for local/dev
            or os.getenv("SUPABASE_ANON_KEY")
            or os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")
            or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpjZ2psbWR2enR4YWt3dWJyanlnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE3NTY4MDMsImV4cCI6MjA3NzMzMjgwM30.A97auA0Ts-xSN_DVi0C7HIB0V5H9ZAjUc5zfEAvj5AE"
        )

        # Normalize values (strip quotes/spaces)
        self.supabase_url = (raw_url or "").strip().strip('"').strip("'")
        self.supabase_key = (raw_key or "").strip().strip('"').strip("'")
        if self.supabase_url.endswith("/"):
            self.supabase_url = self.supabase_url[:-1]
        self._client: Optional[Client] = None
        
        # Log which key type is being used (without exposing the full key)
        key_type = "SERVICE_ROLE" if os.getenv("SUPABASE_SERVICE_ROLE_KEY") else "ANON"
        logger.info(f"Using Supabase {key_type} key (key ends with: ...{self.supabase_key[-10:]})")
    
    @property
    def client(self) -> Client:
        """Get Supabase client instance"""
        if self._client is None:
            try:
                self._client = create_client(self.supabase_url, self.supabase_key)
                logger.info("Supabase client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Supabase client: {e}")
                raise
        return self._client
    
    def test_connection(self) -> bool:
        """Test database connection"""
        try:
            # Simple query to test connection
            result = self.client.table("artwork").select("id").limit(1).execute()
            logger.info("Database connection test successful")
            return True
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False
    
    def add_sample_record(self) -> dict:
        """Add a sample artwork record to the database"""
        try:
            import json
            
            # Create sample artwork data matching the actual table structure:
            # - id: int4 (auto-generated, don't include)
            # - style_tags: json (needs to be JSON string, not array)
            # - dominant_palette: varchar (needs to be string, not object)
            sample_data = {
                "title": "Sample Modern Art Piece",
                "brand": "ArtDecorAI",
                "price": 299.99,
                "style_tags": json.dumps(["modern", "abstract", "minimalist"]),  # Convert to JSON string
                "dominant_palette": json.dumps({  # Convert to JSON string for varchar
                    "primary": "#3498db",
                    "secondary": "#e74c3c",
                    "accent": "#f39c12"
                }),
                "image_url": "https://example.com/sample-art.jpg"
            }
            
            # Insert directly using Supabase client (bypasses CRUD layer to match table structure)
            result = self.client.table("artwork").insert(sample_data).execute()
            
            if not result.data:
                raise Exception("Failed to create artwork - no data returned")
            
            artwork_id = result.data[0].get('id')
            logger.info(f"Successfully added sample record with ID: {artwork_id}")
            return {"success": True, "artwork_id": str(artwork_id), "message": "Sample record added successfully"}
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error adding sample record: {error_msg}")
            
            # Provide helpful error messages
            if "row-level security" in error_msg.lower() or "42501" in error_msg:
                return {
                    "success": False, 
                    "error": error_msg,
                    "help": "You need to add an INSERT policy. See APPLY_POLICY_NOW.sql or use SUPABASE_SERVICE_ROLE_KEY in .env"
                }
            elif "401" in error_msg or "unauthorized" in error_msg.lower():
                return {
                    "success": False,
                    "error": error_msg,
                    "help": "Authentication failed. Check your SUPABASE_ANON_KEY or SUPABASE_SERVICE_ROLE_KEY in backend/.env"
                }
            
            return {"success": False, "error": error_msg}
    
    def add_embedding_record(self, artwork_id: str, vector: list) -> dict:
        """Add a vector embedding record to the artwork_embedding table
        
        Args:
            artwork_id: The UUID of the artwork this embedding belongs to
            vector: List of 384 float values representing the embedding vector
            
        Returns:
            dict with success status, embedding_id, and message
        """
        try:
            # Validate vector dimensions
            if len(vector) != 384:
                raise ValueError(f"Vector must have exactly 384 dimensions, got {len(vector)}")
            
            # Validate artwork_id exists
            artwork_check = self.client.table("artwork").select("id").eq("id", str(artwork_id)).execute()
            if not artwork_check.data:
                raise ValueError(f"Artwork with ID {artwork_id} not found")
            
            # Prepare embedding data
            # Note: Supabase handles VECTOR type as array in JSON format
            embedding_data = {
                "artwork_id": str(artwork_id),
                "vector": vector  # Supabase will convert this to VECTOR type
            }
            
            # Insert into artwork_embedding table
            result = self.client.table("artwork_embedding").insert(embedding_data).execute()
            
            if not result.data:
                raise Exception("Failed to create embedding - no data returned")
            
            embedding_id = result.data[0].get('id')
            logger.info(f"Successfully added embedding record with ID: {embedding_id} for artwork: {artwork_id}")
            return {
                "success": True, 
                "embedding_id": str(embedding_id),
                "artwork_id": str(artwork_id),
                "message": "Embedding record added successfully"
            }
            
        except ValueError as e:
            error_msg = str(e)
            logger.error(f"Validation error adding embedding: {error_msg}")
            return {"success": False, "error": error_msg}
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error adding embedding record: {error_msg}")
            
            # Provide helpful error messages
            if "row-level security" in error_msg.lower() or "42501" in error_msg:
                return {
                    "success": False, 
                    "error": error_msg,
                    "help": "You need to add an INSERT policy for artwork_embedding table. See COPY_THIS_SQL.sql or use SUPABASE_SERVICE_ROLE_KEY in .env"
                }
            elif "401" in error_msg or "unauthorized" in error_msg.lower():
                return {
                    "success": False,
                    "error": error_msg,
                    "help": "Authentication failed. Check your SUPABASE_ANON_KEY or SUPABASE_SERVICE_ROLE_KEY in backend/.env"
                }
            
            return {"success": False, "error": error_msg}
    
    def add_sample_embedding(self, artwork_id: Optional[str] = None) -> dict:
        """Add a sample embedding record to the artwork_embedding table
        
        Args:
            artwork_id: Optional artwork ID. If not provided, creates a sample artwork first.
            
        Returns:
            dict with success status and details
        """
        try:
            # If no artwork_id provided, create a sample artwork first
            if not artwork_id:
                artwork_result = self.add_sample_record()
                if not artwork_result.get("success"):
                    return {
                        "success": False,
                        "error": "Failed to create artwork for embedding",
                        "details": artwork_result
                    }
                artwork_id = artwork_result.get("artwork_id")
            
            # Generate a sample 384-dimensional vector (placeholder)
            # In production, this would come from an embedding model like DINOv2
            import random
            sample_vector = [random.uniform(-1.0, 1.0) for _ in range(384)]
            
            # Add the embedding
            return self.add_embedding_record(artwork_id, sample_vector)
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error adding sample embedding: {error_msg}")
            return {"success": False, "error": error_msg}

# Global database instance
db_connection = DatabaseConnection()
