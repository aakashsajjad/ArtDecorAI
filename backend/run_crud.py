"""
Simple script to run artwork CRUD operations
"""
import asyncio
import sys
import os
from decimal import Decimal

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import db_connection
from crud.artwork_crud import artwork_crud
from models.artwork import ArtworkCreate, ArtworkUpdate, ArtworkSearch

async def test_database_connection():
    """Test if database connection works"""
    print("🔍 Testing database connection...")
    try:
        if db_connection.test_connection():
            print("✅ Database connection successful!")
            return True
        else:
            print("❌ Database connection failed!")
            return False
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

async def run_crud_examples():
    """Run CRUD operation examples"""
    print("\n🚀 Starting Artwork CRUD Operations...")
    
    try:
        # 1. Create a new artwork
        print("\n1️⃣ Creating new artwork...")
        artwork_data = ArtworkCreate(
            title="Test Abstract Art",
            brand="Test Gallery",
            price=Decimal("199.99"),
            style_tags=["abstract", "modern", "test"],
            dominant_palette={
                "primary": "#ff6b6b",
                "secondary": "#4ecdc4",
                "accent": "#45b7d1"
            },
            image_url="https://example.com/test-artwork.jpg"
        )
        
        created_artwork = await artwork_crud.create_artwork(artwork_data)
        print(f"✅ Created artwork: {created_artwork.id} - {created_artwork.title}")
        artwork_id = created_artwork.id
        
        # 2. Get artwork by ID
        print("\n2️⃣ Getting artwork by ID...")
        retrieved_artwork = await artwork_crud.get_artwork_by_id(artwork_id)
        if retrieved_artwork:
            print(f"✅ Retrieved artwork: {retrieved_artwork.title} by {retrieved_artwork.brand}")
        else:
            print("❌ Artwork not found")
        
        # 3. Update artwork
        print("\n3️⃣ Updating artwork...")
        update_data = ArtworkUpdate(
            price=Decimal("249.99"),
            style_tags=["abstract", "modern", "test", "updated"]
        )
        
        updated_artwork = await artwork_crud.update_artwork(artwork_id, update_data)
        if updated_artwork:
            print(f"✅ Updated artwork: {updated_artwork.title} - New price: ${updated_artwork.price}")
        else:
            print("❌ Failed to update artwork")
        
        # 4. Search artworks
        print("\n4️⃣ Searching artworks...")
        search_params = ArtworkSearch(
            style_tags=["abstract", "modern"],
            min_price=Decimal("100.00"),
            max_price=Decimal("300.00"),
            limit=5
        )
        
        search_results = await artwork_crud.search_artworks(search_params)
        print(f"✅ Found {len(search_results)} artworks matching search criteria")
        for artwork in search_results:
            print(f"   - {artwork.title} by {artwork.brand} - ${artwork.price}")
        
        # 5. Get artworks by style
        print("\n5️⃣ Getting artworks by style...")
        style_results = await artwork_crud.get_artworks_by_style(["abstract", "modern"])
        print(f"✅ Found {len(style_results)} artworks with abstract/modern style")
        
        # 6. Get artworks by price range
        print("\n6️⃣ Getting artworks by price range...")
        price_results = await artwork_crud.get_artworks_by_price_range(
            Decimal("150.00"), 
            Decimal("300.00")
        )
        print(f"✅ Found {len(price_results)} artworks in price range $150-$300")
        
        # 7. Get all artworks
        print("\n7️⃣ Getting all artworks...")
        all_artworks = await artwork_crud.get_all_artworks(limit=10, offset=0)
        print(f"✅ Retrieved {len(all_artworks)} artworks")
        
        # 8. Count artworks
        print("\n8️⃣ Counting artworks...")
        total_count = await artwork_crud.count_artworks()
        print(f"✅ Total artworks in database: {total_count}")
        
        # 9. Get recent artworks
        print("\n9️⃣ Getting recent artworks...")
        recent_artworks = await artwork_crud.get_recent_artworks(limit=3)
        print(f"✅ Retrieved {len(recent_artworks)} recent artworks")
        for artwork in recent_artworks:
            print(f"   - {artwork.title} (created: {artwork.created_at})")
        
        # 10. Delete artwork (optional)
        print("\n🔟 Deleting test artwork...")
        delete_success = await artwork_crud.delete_artwork(artwork_id)
        if delete_success:
            print(f"✅ Successfully deleted artwork: {artwork_id}")
        else:
            print(f"❌ Failed to delete artwork: {artwork_id}")
        
        print("\n🎉 All CRUD operations completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during CRUD operations: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """Main function to run the CRUD operations"""
    print("🎨 ArtDecorAI - Artwork CRUD Operations")
    print("=" * 50)
    
    # Test database connection first
    if not await test_database_connection():
        print("\n❌ Cannot proceed without database connection.")
        print("Please ensure:")
        print("1. Supabase is running locally (supabase start)")
        print("2. Environment variables are set correctly")
        print("3. Database schema is created")
        return
    
    # Run CRUD examples
    await run_crud_examples()

if __name__ == "__main__":
    asyncio.run(main())
