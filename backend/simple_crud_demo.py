"""
Simple demonstration of artwork CRUD operations
This version works without requiring a local Supabase instance
"""
import asyncio
import sys
import os
from decimal import Decimal
from datetime import datetime
from uuid import uuid4

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Mock database for demonstration
class MockDatabase:
    """Mock database for demonstration purposes"""
    def __init__(self):
        self.artworks = []
        self._id_counter = 1
    
    def insert(self, data):
        """Mock insert operation"""
        artwork_id = str(uuid4())
        artwork = {
            "id": artwork_id,
            "title": data.get("title"),
            "brand": data.get("brand"),
            "price": float(data.get("price", 0)) if data.get("price") else None,
            "style_tags": data.get("style_tags", []),
            "dominant_palette": data.get("dominant_palette"),
            "image_url": data.get("image_url"),
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        self.artworks.append(artwork)
        return {"data": [artwork]}
    
    def select(self, columns="*"):
        """Mock select operation"""
        return MockQuery(self.artworks)
    
    def eq(self, column, value):
        """Mock equality filter"""
        return self
    
    def gte(self, column, value):
        """Mock greater than or equal filter"""
        return self
    
    def lte(self, column, value):
        """Mock less than or equal filter"""
        return self
    
    def overlaps(self, column, values):
        """Mock array overlap filter"""
        return self
    
    def range(self, start, end):
        """Mock range filter"""
        return self
    
    def limit(self, count):
        """Mock limit filter"""
        return self
    
    def order(self, column, desc=False):
        """Mock order filter"""
        return self
    
    def update(self, data):
        """Mock update operation"""
        return self
    
    def delete(self):
        """Mock delete operation"""
        return self
    
    def execute(self):
        """Mock execute operation"""
        return {"data": self.artworks}

class MockQuery:
    """Mock query builder"""
    def __init__(self, artworks):
        self.artworks = artworks
        self.filters = []
    
    def eq(self, column, value):
        """Mock equality filter"""
        self.filters.append(("eq", column, value))
        return self
    
    def gte(self, column, value):
        """Mock greater than or equal filter"""
        self.filters.append(("gte", column, value))
        return self
    
    def lte(self, column, value):
        """Mock less than or equal filter"""
        self.filters.append(("lte", column, value))
        return self
    
    def overlaps(self, column, values):
        """Mock array overlap filter"""
        self.filters.append(("overlaps", column, values))
        return self
    
    def range(self, start, end):
        """Mock range filter"""
        self.filters.append(("range", start, end))
        return self
    
    def limit(self, count):
        """Mock limit filter"""
        self.filters.append(("limit", count))
        return self
    
    def order(self, column, desc=False):
        """Mock order filter"""
        self.filters.append(("order", column, desc))
        return self
    
    def update(self, data):
        """Mock update operation"""
        return MockUpdate(self.artworks, data)
    
    def delete(self):
        """Mock delete operation"""
        return MockDelete(self.artworks)
    
    def execute(self):
        """Mock execute operation"""
        filtered_artworks = self.artworks.copy()
        
        # Apply filters
        for filter_type, column, value in self.filters:
            if filter_type == "eq":
                filtered_artworks = [a for a in filtered_artworks if a.get(column) == value]
            elif filter_type == "gte":
                filtered_artworks = [a for a in filtered_artworks if a.get(column) and a.get(column) >= value]
            elif filter_type == "lte":
                filtered_artworks = [a for a in filtered_artworks if a.get(column) and a.get(column) <= value]
            elif filter_type == "overlaps":
                filtered_artworks = [a for a in filtered_artworks if a.get(column) and any(tag in a.get(column, []) for tag in value)]
            elif filter_type == "range":
                start, end = value
                filtered_artworks = filtered_artworks[start:end+1]
            elif filter_type == "limit":
                filtered_artworks = filtered_artworks[:value]
            elif filter_type == "order":
                column, desc = value
                filtered_artworks.sort(key=lambda x: x.get(column, ""), reverse=desc)
        
        return {"data": filtered_artworks}

class MockUpdate:
    """Mock update operation"""
    def __init__(self, artworks, data):
        self.artworks = artworks
        self.data = data
    
    def eq(self, column, value):
        """Mock equality filter for update"""
        # Find and update the artwork
        for artwork in self.artworks:
            if artwork.get(column) == value:
                artwork.update(self.data)
                artwork["updated_at"] = datetime.utcnow().isoformat()
                return {"data": [artwork]}
        return {"data": []}

class MockDelete:
    """Mock delete operation"""
    def __init__(self, artworks):
        self.artworks = artworks
    
    def eq(self, column, value):
        """Mock equality filter for delete"""
        # Find and remove the artwork
        for i, artwork in enumerate(self.artworks):
            if artwork.get(column) == value:
                deleted_artwork = self.artworks.pop(i)
                return {"data": [deleted_artwork]}
        return {"data": []}

# Mock the database connection
class MockDatabaseConnection:
    def __init__(self):
        self._client = None
    
    @property
    def client(self):
        if self._client is None:
            self._client = MockSupabaseClient()
        return self._client
    
    def test_connection(self):
        return True

class MockSupabaseClient:
    def __init__(self):
        self.table = lambda name: MockTable()

class MockTable:
    def __init__(self):
        self.db = MockDatabase()
    
    def insert(self, data):
        return self.db.insert(data)
    
    def select(self, columns="*"):
        return self.db.select(columns)
    
    def update(self, data):
        return self.db.update(data)
    
    def delete(self):
        return self.db.delete()
    
    def eq(self, column, value):
        return self
    
    def gte(self, column, value):
        return self
    
    def lte(self, column, value):
        return self
    
    def overlaps(self, column, values):
        return self
    
    def range(self, start, end):
        return self
    
    def limit(self, count):
        return self
    
    def order(self, column, desc=False):
        return self

# Replace the real database connection with mock
import database
database.db_connection = MockDatabaseConnection()

# Now import the CRUD operations
from crud.artwork_crud import artwork_crud
from models.artwork import ArtworkCreate, ArtworkUpdate, ArtworkSearch

async def demonstrate_crud_operations():
    """Demonstrate all CRUD operations"""
    print("🎨 ArtDecorAI - Artwork CRUD Operations Demo")
    print("=" * 60)
    print("📝 Note: This is a demonstration using mock data")
    print("=" * 60)
    
    try:
        # 1. Create a new artwork
        print("\n1️⃣ Creating new artwork...")
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
        
        created_artwork = await artwork_crud.create_artwork(artwork_data)
        print(f"✅ Created artwork: {created_artwork.id}")
        print(f"   Title: {created_artwork.title}")
        print(f"   Brand: {created_artwork.brand}")
        print(f"   Price: ${created_artwork.price}")
        print(f"   Styles: {created_artwork.style_tags}")
        artwork_id = created_artwork.id
        
        # 2. Create another artwork
        print("\n2️⃣ Creating second artwork...")
        artwork_data2 = ArtworkCreate(
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
        
        created_artwork2 = await artwork_crud.create_artwork(artwork_data2)
        print(f"✅ Created artwork: {created_artwork2.id}")
        print(f"   Title: {created_artwork2.title}")
        
        # 3. Get artwork by ID
        print(f"\n3️⃣ Getting artwork by ID: {artwork_id}")
        retrieved_artwork = await artwork_crud.get_artwork_by_id(artwork_id)
        if retrieved_artwork:
            print(f"✅ Retrieved artwork: {retrieved_artwork.title}")
        else:
            print("❌ Artwork not found")
        
        # 4. Update artwork
        print(f"\n4️⃣ Updating artwork: {artwork_id}")
        update_data = ArtworkUpdate(
            price=Decimal("349.99"),
            style_tags=["abstract", "modern", "blue", "contemporary"]
        )
        
        updated_artwork = await artwork_crud.update_artwork(artwork_id, update_data)
        if updated_artwork:
            print(f"✅ Updated artwork: {updated_artwork.title}")
            print(f"   New price: ${updated_artwork.price}")
            print(f"   New styles: {updated_artwork.style_tags}")
        else:
            print("❌ Failed to update artwork")
        
        # 5. Get all artworks
        print("\n5️⃣ Getting all artworks...")
        all_artworks = await artwork_crud.get_all_artworks(limit=10, offset=0)
        print(f"✅ Retrieved {len(all_artworks)} artworks:")
        for artwork in all_artworks:
            print(f"   - {artwork.title} by {artwork.brand} - ${artwork.price}")
        
        # 6. Search artworks by style
        print("\n6️⃣ Searching artworks by style (abstract, modern)...")
        search_results = await artwork_crud.get_artworks_by_style(["abstract", "modern"])
        print(f"✅ Found {len(search_results)} artworks with abstract/modern style:")
        for artwork in search_results:
            print(f"   - {artwork.title} by {artwork.brand}")
        
        # 7. Search artworks by price range
        print("\n7️⃣ Searching artworks by price range ($150-$400)...")
        price_results = await artwork_crud.get_artworks_by_price_range(
            Decimal("150.00"), 
            Decimal("400.00")
        )
        print(f"✅ Found {len(price_results)} artworks in price range $150-$400:")
        for artwork in price_results:
            print(f"   - {artwork.title} by {artwork.brand} - ${artwork.price}")
        
        # 8. Advanced search
        print("\n8️⃣ Advanced search with multiple filters...")
        search_params = ArtworkSearch(
            style_tags=["abstract", "modern"],
            min_price=Decimal("200.00"),
            max_price=Decimal("500.00"),
            limit=5
        )
        
        advanced_results = await artwork_crud.search_artworks(search_params)
        print(f"✅ Found {len(advanced_results)} artworks matching advanced criteria:")
        for artwork in advanced_results:
            print(f"   - {artwork.title} by {artwork.brand} - ${artwork.price}")
        
        # 9. Count artworks
        print("\n9️⃣ Counting total artworks...")
        total_count = await artwork_crud.count_artworks()
        print(f"✅ Total artworks in database: {total_count}")
        
        # 10. Get recent artworks
        print("\n🔟 Getting recent artworks...")
        recent_artworks = await artwork_crud.get_recent_artworks(limit=3)
        print(f"✅ Retrieved {len(recent_artworks)} recent artworks:")
        for artwork in recent_artworks:
            print(f"   - {artwork.title} (created: {artwork.created_at})")
        
        # 11. Delete artwork (optional)
        print(f"\n🗑️ Deleting artwork: {artwork_id}")
        delete_success = await artwork_crud.delete_artwork(artwork_id)
        if delete_success:
            print(f"✅ Successfully deleted artwork: {artwork_id}")
        else:
            print(f"❌ Failed to delete artwork: {artwork_id}")
        
        # 12. Final count
        print("\n📊 Final artwork count...")
        final_count = await artwork_crud.count_artworks()
        print(f"✅ Remaining artworks: {final_count}")
        
        print("\n🎉 All CRUD operations completed successfully!")
        print("\n📋 Summary of operations demonstrated:")
        print("   ✅ CREATE - Create new artwork")
        print("   ✅ READ - Get artwork by ID, get all artworks")
        print("   ✅ UPDATE - Update artwork details")
        print("   ✅ DELETE - Delete artwork")
        print("   ✅ SEARCH - Search by style, price, filters")
        print("   ✅ COUNT - Count total artworks")
        print("   ✅ RECENT - Get recently added artworks")
        
    except Exception as e:
        print(f"❌ Error during CRUD operations: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """Main function"""
    await demonstrate_crud_operations()

if __name__ == "__main__":
    asyncio.run(main())
