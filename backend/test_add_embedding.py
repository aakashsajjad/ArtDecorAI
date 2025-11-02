"""
Test script to add embedding records to artwork_embedding table
"""
import sys
from pathlib import Path

# Add parent directory to path to allow imports
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

from database import db_connection

def main():
    """Test adding embedding records to the database"""
    print("=" * 60)
    print("Testing Embedding Record Addition")
    print("=" * 60)
    
    # Test connection first
    print("\n1. Testing database connection...")
    if db_connection.test_connection():
        print("✅ Database connection successful!")
    else:
        print("❌ Database connection failed!")
        return
    
    # Test adding a sample embedding (will create artwork first if needed)
    print("\n2. Adding sample embedding record...")
    print("   (This will create a sample artwork if none exists)")
    result = db_connection.add_sample_embedding()
    
    if result.get("success"):
        print(f"✅ {result.get('message')}")
        print(f"   Embedding ID: {result.get('embedding_id')}")
        print(f"   Artwork ID: {result.get('artwork_id')}")
    else:
        print(f"❌ Error adding embedding: {result.get('error')}")
        if result.get("help"):
            print(f"\n💡 Help: {result.get('help')}")
        if result.get("details"):
            print(f"\n   Details: {result.get('details')}")
    
    # Example: Add embedding to specific artwork
    print("\n3. Example: Adding embedding to existing artwork...")
    print("   (First, let's get an artwork ID)")
    
    # Get first artwork ID
    try:
        artworks = db_connection.client.table("artwork").select("id").limit(1).execute()
        if artworks.data:
            existing_artwork_id = artworks.data[0].get('id')
            print(f"   Found artwork ID: {existing_artwork_id}")
            
            # Add embedding to this artwork
            import random
            custom_vector = [random.uniform(-1.0, 1.0) for _ in range(384)]
            result2 = db_connection.add_embedding_record(str(existing_artwork_id), custom_vector)
            
            if result2.get("success"):
                print(f"✅ Added embedding to artwork {existing_artwork_id}")
                print(f"   Embedding ID: {result2.get('embedding_id')}")
            else:
                print(f"❌ Error: {result2.get('error')}")
        else:
            print("   No artworks found. Create an artwork first.")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("Usage Examples:")
    print("=" * 60)
    print("""
# Add sample embedding (creates artwork automatically)
result = db_connection.add_sample_embedding()

# Add embedding to specific artwork
vector = [0.1, 0.2, ...]  # 384 dimensions
result = db_connection.add_embedding_record(artwork_id="your-uuid", vector=vector)
    """)

if __name__ == "__main__":
    main()

