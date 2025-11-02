"""
Test script to add a new record using the add_sample_record function
"""
import sys
import os
from pathlib import Path

# Add parent directory to path to allow imports
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

from database import db_connection

def main():
    """Test adding a sample record to the database"""
    print("=" * 60)
    print("Testing Database Record Addition")
    print("=" * 60)
    
    # Test connection first
    print("\n1. Testing database connection...")
    if db_connection.test_connection():
        print("✅ Database connection successful!")
    else:
        print("❌ Database connection failed!")
        return
    
    # Add sample record
    print("\n2. Adding sample record to database...")
    result = db_connection.add_sample_record()
    
    if result.get("success"):
        print(f"✅ {result.get('message')}")
        print(f"   Artwork ID: {result.get('artwork_id')}")
    else:
        print(f"❌ Error adding record: {result.get('error')}")
        if result.get("help"):
            print(f"\n💡 Help: {result.get('help')}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
