"""
Simple demonstration of adding a new record using database.py
"""
from database import db_connection

if __name__ == "__main__":
    # Test connection first
    print("Testing database connection...")
    connection_success = db_connection.test_connection()
    
    if connection_success:
        print("✅ Connection successful!")
        print()
        
        # Add a new record
        print("Adding sample record...")
        result = db_connection.add_sample_record()
        
        if result.get("success"):
            print(f"✅ {result.get('message')}")
            print(f"📝 Artwork ID: {result.get('artwork_id')}")
        else:
            print(f"❌ Error: {result.get('error')}")
    else:
        print("❌ Failed to connect to database")

