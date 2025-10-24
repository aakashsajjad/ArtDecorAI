"""
Direct demonstration of artwork CRUD operations
Simple version that shows how CRUD operations work
"""
import asyncio
from decimal import Decimal
from datetime import datetime
from uuid import uuid4
from typing import List, Optional, Dict, Any

# Simple Artwork model
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

# Simple in-memory database
class ArtworkDatabase:
    def __init__(self):
        self.artworks: List[Artwork] = []
        self._id_counter = 1
    
    def create(self, title: str, brand: str = None, price: Decimal = None, 
               style_tags: List[str] = None, dominant_palette: Dict = None, 
               image_url: str = None) -> Artwork:
        """Create a new artwork"""
        artwork = Artwork(title, brand, price, style_tags, dominant_palette, image_url)
        self.artworks.append(artwork)
        return artwork
    
    def get_by_id(self, artwork_id: str) -> Optional[Artwork]:
        """Get artwork by ID"""
        for artwork in self.artworks:
            if artwork.id == artwork_id:
                return artwork
        return None
    
    def get_all(self, limit: int = 10, offset: int = 0) -> List[Artwork]:
        """Get all artworks with pagination"""
        return self.artworks[offset:offset + limit]
    
    def update(self, artwork_id: str, **kwargs) -> Optional[Artwork]:
        """Update artwork by ID"""
        artwork = self.get_by_id(artwork_id)
        if artwork:
            artwork.update(**kwargs)
            return artwork
        return None
    
    def delete(self, artwork_id: str) -> bool:
        """Delete artwork by ID"""
        for i, artwork in enumerate(self.artworks):
            if artwork.id == artwork_id:
                del self.artworks[i]
                return True
        return False
    
    def search_by_style(self, style_tags: List[str]) -> List[Artwork]:
        """Search artworks by style tags"""
        results = []
        for artwork in self.artworks:
            if any(tag in artwork.style_tags for tag in style_tags):
                results.append(artwork)
        return results
    
    def search_by_price_range(self, min_price: Decimal, max_price: Decimal) -> List[Artwork]:
        """Search artworks by price range"""
        results = []
        for artwork in self.artworks:
            if artwork.price and min_price <= artwork.price <= max_price:
                results.append(artwork)
        return results
    
    def search_by_brand(self, brand: str) -> List[Artwork]:
        """Search artworks by brand"""
        results = []
        for artwork in self.artworks:
            if artwork.brand and brand.lower() in artwork.brand.lower():
                results.append(artwork)
        return results
    
    def count(self) -> int:
        """Get total count of artworks"""
        return len(self.artworks)
    
    def get_recent(self, limit: int = 5) -> List[Artwork]:
        """Get recently added artworks"""
        return sorted(self.artworks, key=lambda x: x.created_at, reverse=True)[:limit]

# Global database instance
db = ArtworkDatabase()

async def demonstrate_crud_operations():
    """Demonstrate all CRUD operations"""
    print("🎨 ArtDecorAI - Artwork CRUD Operations Demo")
    print("=" * 60)
    print("📝 This demonstrates all CRUD operations for the artwork table")
    print("=" * 60)
    
    try:
        # 1. CREATE - Create new artworks
        print("\n1️⃣ CREATE - Creating new artworks...")
        
        artwork1 = db.create(
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
        print(f"✅ Created artwork: {artwork1.id}")
        print(f"   Title: {artwork1.title}")
        print(f"   Brand: {artwork1.brand}")
        print(f"   Price: ${artwork1.price}")
        print(f"   Styles: {artwork1.style_tags}")
        
        artwork2 = db.create(
            title="Minimalist Black Lines",
            brand="Minimal Designs",
            price=Decimal("199.99"),
            style_tags=["minimalist", "black", "geometric"],
            dominant_palette={
                "primary": "#000000",
                "secondary": "#404040",
                "accent": "#808080"
            },
            image_url="https://example.com/artwork2.jpg"
        )
        print(f"✅ Created artwork: {artwork2.id}")
        print(f"   Title: {artwork2.title}")
        
        artwork3 = db.create(
            title="Vintage Botanical Print",
            brand="Botanical Arts",
            price=Decimal("149.99"),
            style_tags=["vintage", "botanical", "green"],
            dominant_palette={
                "primary": "#166534",
                "secondary": "#22c55e",
                "accent": "#84cc16"
            },
            image_url="https://example.com/artwork3.jpg"
        )
        print(f"✅ Created artwork: {artwork3.id}")
        print(f"   Title: {artwork3.title}")
        
        # 2. READ - Get artwork by ID
        print(f"\n2️⃣ READ - Getting artwork by ID: {artwork1.id}")
        retrieved_artwork = db.get_by_id(artwork1.id)
        if retrieved_artwork:
            print(f"✅ Retrieved artwork: {retrieved_artwork.title}")
            print(f"   Brand: {retrieved_artwork.brand}")
            print(f"   Price: ${retrieved_artwork.price}")
        else:
            print("❌ Artwork not found")
        
        # 3. READ - Get all artworks
        print("\n3️⃣ READ - Getting all artworks...")
        all_artworks = db.get_all(limit=10, offset=0)
        print(f"✅ Retrieved {len(all_artworks)} artworks:")
        for artwork in all_artworks:
            print(f"   - {artwork.title} by {artwork.brand} - ${artwork.price}")
        
        # 4. UPDATE - Update artwork
        print(f"\n4️⃣ UPDATE - Updating artwork: {artwork1.id}")
        updated_artwork = db.update(
            artwork1.id,
            price=Decimal("349.99"),
            style_tags=["abstract", "modern", "blue", "contemporary"]
        )
        if updated_artwork:
            print(f"✅ Updated artwork: {updated_artwork.title}")
            print(f"   New price: ${updated_artwork.price}")
            print(f"   New styles: {updated_artwork.style_tags}")
        else:
            print("❌ Failed to update artwork")
        
        # 5. SEARCH - Search by style
        print("\n5️⃣ SEARCH - Searching artworks by style (abstract, modern)...")
        style_results = db.search_by_style(["abstract", "modern"])
        print(f"✅ Found {len(style_results)} artworks with abstract/modern style:")
        for artwork in style_results:
            print(f"   - {artwork.title} by {artwork.brand}")
        
        # 6. SEARCH - Search by price range
        print("\n6️⃣ SEARCH - Searching artworks by price range ($150-$400)...")
        price_results = db.search_by_price_range(Decimal("150.00"), Decimal("400.00"))
        print(f"✅ Found {len(price_results)} artworks in price range $150-$400:")
        for artwork in price_results:
            print(f"   - {artwork.title} by {artwork.brand} - ${artwork.price}")
        
        # 7. SEARCH - Search by brand
        print("\n7️⃣ SEARCH - Searching artworks by brand (Contemporary)...")
        brand_results = db.search_by_brand("Contemporary")
        print(f"✅ Found {len(brand_results)} artworks by Contemporary Gallery:")
        for artwork in brand_results:
            print(f"   - {artwork.title} by {artwork.brand}")
        
        # 8. COUNT - Count artworks
        print("\n8️⃣ COUNT - Counting total artworks...")
        total_count = db.count()
        print(f"✅ Total artworks in database: {total_count}")
        
        # 9. RECENT - Get recent artworks
        print("\n9️⃣ RECENT - Getting recent artworks...")
        recent_artworks = db.get_recent(limit=3)
        print(f"✅ Retrieved {len(recent_artworks)} recent artworks:")
        for artwork in recent_artworks:
            print(f"   - {artwork.title} (created: {artwork.created_at.strftime('%Y-%m-%d %H:%M:%S')})")
        
        # 10. DELETE - Delete artwork
        print(f"\n🔟 DELETE - Deleting artwork: {artwork1.id}")
        delete_success = db.delete(artwork1.id)
        if delete_success:
            print(f"✅ Successfully deleted artwork: {artwork1.id}")
        else:
            print(f"❌ Failed to delete artwork: {artwork1.id}")
        
        # 11. Final count
        print("\n📊 Final count after deletion...")
        final_count = db.count()
        print(f"✅ Remaining artworks: {final_count}")
        
        # 12. Show final state
        print("\n📋 Final artworks in database:")
        remaining_artworks = db.get_all()
        for artwork in remaining_artworks:
            print(f"   - {artwork.title} by {artwork.brand} - ${artwork.price}")
        
        print("\n🎉 All CRUD operations completed successfully!")
        print("\n📋 Summary of operations demonstrated:")
        print("   ✅ CREATE - Create new artwork records")
        print("   ✅ READ - Get artwork by ID, get all artworks")
        print("   ✅ UPDATE - Update artwork details")
        print("   ✅ DELETE - Delete artwork records")
        print("   ✅ SEARCH - Search by style, price, brand")
        print("   ✅ COUNT - Count total artworks")
        print("   ✅ RECENT - Get recently added artworks")
        
        print("\n🔧 CRUD Operations Explained:")
        print("   CREATE: Add new artwork records to the database")
        print("   READ: Retrieve artwork information by ID or get all records")
        print("   UPDATE: Modify existing artwork details")
        print("   DELETE: Remove artwork records from the database")
        print("   SEARCH: Find artworks based on specific criteria")
        print("   COUNT: Get the total number of artwork records")
        print("   RECENT: Get the most recently added artworks")
        
    except Exception as e:
        print(f"❌ Error during CRUD operations: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """Main function"""
    await demonstrate_crud_operations()

if __name__ == "__main__":
    asyncio.run(main())
