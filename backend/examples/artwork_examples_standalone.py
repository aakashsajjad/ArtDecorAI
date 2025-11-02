"""
Standalone example usage of artwork CRUD operations (No Database Required)
This version works without requiring a database connection
"""
import asyncio
import logging
from decimal import Decimal
from uuid import uuid4
from datetime import datetime
from typing import List, Optional, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simple Artwork model for standalone demo
class Artwork:
    def __init__(self, title: str, brand: str = None, price: Decimal = None, 
                 style_tags: List[str] = None, dominant_palette: Dict = None, 
                 image_url: str = None):
        self.id = str(uuid4())
        self.title = title
        self.brand = brand
        self.price = price
        self.style_tags = style_tags or []
        self.dominant_palette = dominant_palette or {}
        self.image_url = image_url
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "brand": self.brand,
            "price": float(self.price) if self.price else None,
            "style_tags": self.style_tags,
            "dominant_palette": self.dominant_palette,
            "image_url": self.image_url,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)
        self.updated_at = datetime.now()

# Simple in-memory database for standalone demo
class ArtworkDatabase:
    def __init__(self):
        self.artworks: List[Artwork] = []
    
    async def create_artwork(self, title: str, brand: str = None, price: Decimal = None, 
                           style_tags: List[str] = None, dominant_palette: Dict = None, 
                           image_url: str = None) -> Artwork:
        """Create a new artwork"""
        artwork = Artwork(title, brand, price, style_tags, dominant_palette, image_url)
        self.artworks.append(artwork)
        return artwork
    
    async def get_artwork_by_id(self, artwork_id: str) -> Optional[Artwork]:
        """Get artwork by ID"""
        for artwork in self.artworks:
            if artwork.id == artwork_id:
                return artwork
        return None
    
    async def get_all_artworks(self, limit: int = 10, offset: int = 0) -> List[Artwork]:
        """Get all artworks with pagination"""
        return self.artworks[offset:offset + limit]
    
    async def update_artwork(self, artwork_id: str, **kwargs) -> Optional[Artwork]:
        """Update artwork by ID"""
        artwork = await self.get_artwork_by_id(artwork_id)
        if artwork:
            artwork.update(**kwargs)
            return artwork
        return None
    
    async def delete_artwork(self, artwork_id: str) -> bool:
        """Delete artwork by ID"""
        for i, artwork in enumerate(self.artworks):
            if artwork.id == artwork_id:
                del self.artworks[i]
                return True
        return False
    
    async def search_artworks(self, style_tags: List[str] = None, 
                            min_price: Decimal = None, max_price: Decimal = None,
                            limit: int = 10) -> List[Artwork]:
        """Search artworks by various criteria"""
        results = []
        for artwork in self.artworks:
            # Filter by style tags
            if style_tags and not any(tag in artwork.style_tags for tag in style_tags):
                continue
            
            # Filter by price range
            if min_price and artwork.price and artwork.price < min_price:
                continue
            if max_price and artwork.price and artwork.price > max_price:
                continue
            
            results.append(artwork)
        
        return results[:limit]
    
    async def get_artworks_by_style(self, style_tags: List[str]) -> List[Artwork]:
        """Search artworks by style tags"""
        results = []
        for artwork in self.artworks:
            if any(tag in artwork.style_tags for tag in style_tags):
                results.append(artwork)
        return results
    
    async def get_artworks_by_price_range(self, min_price: Decimal, max_price: Decimal) -> List[Artwork]:
        """Search artworks by price range"""
        results = []
        for artwork in self.artworks:
            if artwork.price and min_price <= artwork.price <= max_price:
                results.append(artwork)
        return results
    
    async def count_artworks(self) -> int:
        """Get total count of artworks"""
        return len(self.artworks)
    
    async def get_recent_artworks(self, limit: int = 5) -> List[Artwork]:
        """Get recently added artworks"""
        return sorted(self.artworks, key=lambda x: x.created_at, reverse=True)[:limit]

# Global database instance
db = ArtworkDatabase()

async def example_create_artwork():
    """Example: Create a new artwork"""
    logger.info("=== Creating Artwork Example ===")
    
    try:
        artwork = await db.create_artwork(
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
        logger.info(f"Created artwork: {artwork.id} - {artwork.title}")
        return artwork
    except Exception as e:
        logger.error(f"Error creating artwork: {e}")
        return None

async def example_get_artwork(artwork_id):
    """Example: Get artwork by ID"""
    logger.info("=== Getting Artwork Example ===")
    
    try:
        artwork = await db.get_artwork_by_id(artwork_id)
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
    
    try:
        updated_artwork = await db.update_artwork(
            artwork_id,
            price=Decimal("349.99"),
            style_tags=["abstract", "modern", "blue", "contemporary"]
        )
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
    
    try:
        artworks = await db.search_artworks(
            style_tags=["abstract", "modern"],
            min_price=Decimal("100.00"),
            max_price=Decimal("500.00"),
            limit=5
        )
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
        artworks = await db.get_artworks_by_style(["abstract", "modern"])
        logger.info(f"Found {len(artworks)} artworks with abstract/modern style")
        return artworks
    except Exception as e:
        logger.error(f"Error getting artworks by style: {e}")
        return []

async def example_get_artworks_by_price_range():
    """Example: Get artworks by price range"""
    logger.info("=== Getting Artworks by Price Range Example ===")
    
    try:
        artworks = await db.get_artworks_by_price_range(
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
        artworks = await db.get_all_artworks(limit=10, offset=0)
        logger.info(f"Retrieved {len(artworks)} artworks")
        return artworks
    except Exception as e:
        logger.error(f"Error getting all artworks: {e}")
        return []

async def example_count_artworks():
    """Example: Count artworks"""
    logger.info("=== Counting Artworks Example ===")
    
    try:
        count = await db.count_artworks()
        logger.info(f"Total artworks in database: {count}")
        return count
    except Exception as e:
        logger.error(f"Error counting artworks: {e}")
        return 0

async def example_delete_artwork(artwork_id):
    """Example: Delete artwork"""
    logger.info("=== Deleting Artwork Example ===")
    
    try:
        success = await db.delete_artwork(artwork_id)
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
    logger.info("🎨 Starting Artwork CRUD Examples (Standalone Mode)...")
    logger.info("=" * 60)
    
    # Create some sample artworks first
    logger.info("📝 Creating sample artworks...")
    
    # Create multiple artworks for better examples
    artwork1 = await db.create_artwork(
        title="Vintage Botanical Print",
        brand="Botanical Arts",
        price=Decimal("149.99"),
        style_tags=["vintage", "botanical", "green"],
        dominant_palette={
            "primary": "#166534",
            "secondary": "#22c55e",
            "accent": "#84cc16"
        },
        image_url="https://example.com/artwork2.jpg"
    )
    
    artwork2 = await db.create_artwork(
        title="Minimalist Black Lines",
        brand="Minimal Designs",
        price=Decimal("199.99"),
        style_tags=["minimalist", "black", "geometric"],
        dominant_palette={
            "primary": "#000000",
            "secondary": "#404040",
            "accent": "#808080"
        },
        image_url="https://example.com/artwork3.jpg"
    )
    
    # Create artwork for main example
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
    
    # Show recent artworks
    logger.info("=== Recent Artworks Example ===")
    recent = await db.get_recent_artworks(limit=3)
    logger.info(f"Found {len(recent)} recent artworks")
    for artwork in recent:
        logger.info(f"- {artwork.title} (created: {artwork.created_at.strftime('%Y-%m-%d %H:%M:%S')})")
    
    # Delete artwork (optional - comment out if you want to keep the data)
    # await example_delete_artwork(artwork_id)
    
    logger.info("🎉 All examples completed successfully!")
    logger.info("📋 Summary of operations demonstrated:")
    logger.info("   ✅ CREATE - Create new artwork records")
    logger.info("   ✅ READ - Get artwork by ID, get all artworks")
    logger.info("   ✅ UPDATE - Update artwork details")
    logger.info("   ✅ DELETE - Delete artwork records (commented out)")
    logger.info("   ✅ SEARCH - Search by style, price range")
    logger.info("   ✅ COUNT - Count total artworks")
    logger.info("   ✅ RECENT - Get recently added artworks")

if __name__ == "__main__":
    asyncio.run(run_all_examples())

