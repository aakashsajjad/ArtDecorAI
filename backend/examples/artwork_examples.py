"""
Example usage of artwork CRUD operations
"""
import os
import sys

# Ensure the backend root is on sys.path when running this file directly
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_ROOT = os.path.dirname(CURRENT_DIR)
if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)
import asyncio
import logging
from decimal import Decimal
from uuid import uuid4

from models.artwork import ArtworkCreate, ArtworkUpdate, ArtworkSearch
from crud.artwork_crud import artwork_crud
from database import db_connection

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_database_connection():
    """Check if database connection is available"""
    try:
        # Test the connection - this method returns True/False and logs errors
        if db_connection.test_connection():
            return True
        else:
            logger.error("\n" + "="*60)
            logger.error("❌ Supabase is not running or not configured properly!")
            logger.error("="*60)
            logger.error("\nTo fix this:")
            logger.error("1. Start Supabase locally: supabase start")
            logger.error("2. Or configure your .env file with production Supabase credentials")
            logger.error("   Example .env entries:")
            logger.error("   SUPABASE_URL=https://your-project-ref.supabase.co")
            logger.error("   SUPABASE_ANON_KEY=your-anon-key")
            logger.error("3. Or use the direct_crud_demo.py which doesn't require a database")
            logger.error("\n" + "="*60)
            return False
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        logger.error("\n" + "="*60)
        logger.error("❌ Supabase is not running or not configured properly!")
        logger.error("="*60)
        logger.error("\nTo fix this:")
        logger.error("1. Start Supabase locally: supabase start")
        logger.error("2. Or configure your .env file with production Supabase credentials")
        logger.error("   Example .env entries:")
        logger.error("   SUPABASE_URL=https://your-project-ref.supabase.co")
        logger.error("   SUPABASE_ANON_KEY=your-anon-key")
        logger.error("3. Or use the direct_crud_demo.py which doesn't require a database")
        logger.error("\n" + "="*60)
        return False

async def example_create_artwork():
    """Example: Create a new artwork"""
    logger.info("=== Creating Artwork Example ===")
    
    artwork_data = ArtworkCreate(
        title="Modern Abstract Waves",
        brand="Contemporary Gallery",
        price=Decimal("299.99"),
        style_tags=["abstract", "modern", "blue"],
        dominant_palette={
            "primary": "#1e3a8a",
            "secondary": "#3b82f6", 
            "accent": "#93c5fd"
        },
        image_url="https://example.com/artwork1.jpg"
    )
    
    try:
        artwork = await artwork_crud.create_artwork(artwork_data)
        logger.info(f"Created artwork: {artwork.id} - {artwork.title}")
        return artwork
    except Exception as e:
        logger.error(f"Error creating artwork: {e}")
        return None

async def example_get_artwork(artwork_id):
    """Example: Get artwork by ID"""
    logger.info("=== Getting Artwork Example ===")
    
    try:
        artwork = await artwork_crud.get_artwork_by_id(artwork_id)
        if artwork:
            logger.info(f"Found artwork: {artwork.title} by {artwork.brand}")
        else:
            logger.info("Artwork not found")
        return artwork
    except Exception as e:
        logger.error(f"Error getting artwork: {e}")
        return None

async def example_update_artwork(artwork_id):
    """Example: Update artwork"""
    logger.info("=== Updating Artwork Example ===")
    
    update_data = ArtworkUpdate(
        price=Decimal("349.99"),
        style_tags=["abstract", "modern", "blue", "contemporary"]
    )
    
    try:
        updated_artwork = await artwork_crud.update_artwork(artwork_id, update_data)
        if updated_artwork:
            logger.info(f"Updated artwork: {updated_artwork.title} - New price: ${updated_artwork.price}")
        else:
            logger.info("Artwork not found for update")
        return updated_artwork
    except Exception as e:
        logger.error(f"Error updating artwork: {e}")
        return None

async def example_search_artworks():
    """Example: Search artworks"""
    logger.info("=== Searching Artworks Example ===")
    
    search_params = ArtworkSearch(
        style_tags=["abstract", "modern"],
        min_price=Decimal("100.00"),
        max_price=Decimal("500.00"),
        limit=5
    )
    
    try:
        artworks = await artwork_crud.search_artworks(search_params)
        logger.info(f"Found {len(artworks)} artworks matching criteria")
        for artwork in artworks:
            logger.info(f"- {artwork.title} by {artwork.brand} - ${artwork.price}")
        return artworks
    except Exception as e:
        logger.error(f"Error searching artworks: {e}")
        return []

async def example_get_artworks_by_style():
    """Example: Get artworks by style"""
    logger.info("=== Getting Artworks by Style Example ===")
    
    try:
        artworks = await artwork_crud.get_artworks_by_style(["abstract", "modern"])
        logger.info(f"Found {len(artworks)} artworks with abstract/modern style")
        return artworks
    except Exception as e:
        logger.error(f"Error getting artworks by style: {e}")
        return []

async def example_get_artworks_by_price_range():
    """Example: Get artworks by price range"""
    logger.info("=== Getting Artworks by Price Range Example ===")
    
    try:
        artworks = await artwork_crud.get_artworks_by_price_range(
            Decimal("200.00"), 
            Decimal("400.00")
        )
        logger.info(f"Found {len(artworks)} artworks in price range $200-$400")
        return artworks
    except Exception as e:
        logger.error(f"Error getting artworks by price range: {e}")
        return []

async def example_get_all_artworks():
    """Example: Get all artworks with pagination"""
    logger.info("=== Getting All Artworks Example ===")
    
    try:
        artworks = await artwork_crud.get_all_artworks(limit=10, offset=0)
        logger.info(f"Retrieved {len(artworks)} artworks")
        return artworks
    except Exception as e:
        logger.error(f"Error getting all artworks: {e}")
        return []

async def example_count_artworks():
    """Example: Count artworks"""
    logger.info("=== Counting Artworks Example ===")
    
    try:
        count = await artwork_crud.count_artworks()
        logger.info(f"Total artworks in database: {count}")
        return count
    except Exception as e:
        logger.error(f"Error counting artworks: {e}")
        return 0

async def example_delete_artwork(artwork_id):
    """Example: Delete artwork"""
    logger.info("=== Deleting Artwork Example ===")
    
    try:
        success = await artwork_crud.delete_artwork(artwork_id)
        if success:
            logger.info(f"Successfully deleted artwork: {artwork_id}")
        else:
            logger.info(f"Artwork not found for deletion: {artwork_id}")
        return success
    except Exception as e:
        logger.error(f"Error deleting artwork: {e}")
        return False

async def run_all_examples():
    """Run all examples"""
    logger.info("Starting Artwork CRUD Examples...")
    
    # Check database connection first
    if not check_database_connection():
        logger.error("Cannot proceed without database connection. Exiting.")
        return
    
    # Create artwork
    artwork = await example_create_artwork()
    if not artwork:
        logger.error("Failed to create artwork, stopping examples")
        return
    
    artwork_id = artwork.id
    
    # Get artwork
    await example_get_artwork(artwork_id)
    
    # Update artwork
    await example_update_artwork(artwork_id)
    
    # Search artworks
    await example_search_artworks()
    
    # Get by style
    await example_get_artworks_by_style()
    
    # Get by price range
    await example_get_artworks_by_price_range()
    
    # Get all artworks
    await example_get_all_artworks()
    
    # Count artworks
    await example_count_artworks()
    
    # Delete artwork (optional - comment out if you want to keep the data)
    # await example_delete_artwork(artwork_id)
    
    logger.info("All examples completed!")

if __name__ == "__main__":
    asyncio.run(run_all_examples())
