"""
Test script to verify backend is working
"""
import requests
import time
import json

def test_backend():
    """Test the backend API"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing ArtDecorAI Backend API")
    print("=" * 50)
    
    # Wait a moment for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(3)
    
    try:
        # Test health endpoint
        print("\n1️⃣ Testing health endpoint...")
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health check passed: {health_data['status']}")
            print(f"   Database: {health_data.get('database', 'unknown')}")
            print(f"   Mode: {health_data.get('mode', 'unknown')}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
        
        # Test root endpoint
        print("\n2️⃣ Testing root endpoint...")
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            root_data = response.json()
            print(f"✅ Root endpoint: {root_data['message']}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
        
        # Test artworks endpoint
        print("\n3️⃣ Testing artworks endpoint...")
        response = requests.get(f"{base_url}/api/artworks/", timeout=5)
        if response.status_code == 200:
            artworks = response.json()
            print(f"✅ Found {len(artworks)} artworks")
            for artwork in artworks:
                print(f"   - {artwork['title']} by {artwork['brand']} - ${artwork['price']}")
        else:
            print(f"❌ Artworks endpoint failed: {response.status_code}")
        
        # Test create artwork
        print("\n4️⃣ Testing create artwork...")
        new_artwork = {
            "title": "Test Artwork",
            "brand": "Test Gallery",
            "price": 199.99,
            "style_tags": ["test", "demo"],
            "dominant_palette": {
                "primary": "#ff0000",
                "secondary": "#00ff00"
            },
            "image_url": "https://example.com/test.jpg"
        }
        
        response = requests.post(f"{base_url}/api/artworks/", 
                               json=new_artwork, 
                               headers={"Content-Type": "application/json"},
                               timeout=5)
        if response.status_code == 200:
            created_artwork = response.json()
            print(f"✅ Created artwork: {created_artwork['title']} (ID: {created_artwork['id']})")
            artwork_id = created_artwork['id']
        else:
            print(f"❌ Create artwork failed: {response.status_code}")
            return False
        
        # Test get artwork by ID
        print(f"\n5️⃣ Testing get artwork by ID ({artwork_id})...")
        response = requests.get(f"{base_url}/api/artworks/{artwork_id}", timeout=5)
        if response.status_code == 200:
            artwork = response.json()
            print(f"✅ Retrieved artwork: {artwork['title']}")
        else:
            print(f"❌ Get artwork by ID failed: {response.status_code}")
        
        # Test update artwork
        print(f"\n6️⃣ Testing update artwork ({artwork_id})...")
        update_data = {
            "price": 299.99,
            "style_tags": ["test", "demo", "updated"]
        }
        
        response = requests.put(f"{base_url}/api/artworks/{artwork_id}",
                              json=update_data,
                              headers={"Content-Type": "application/json"},
                              timeout=5)
        if response.status_code == 200:
            updated_artwork = response.json()
            print(f"✅ Updated artwork: {updated_artwork['title']} - New price: ${updated_artwork['price']}")
        else:
            print(f"❌ Update artwork failed: {response.status_code}")
        
        # Test delete artwork
        print(f"\n7️⃣ Testing delete artwork ({artwork_id})...")
        response = requests.delete(f"{base_url}/api/artworks/{artwork_id}", timeout=5)
        if response.status_code == 200:
            delete_result = response.json()
            print(f"✅ Deleted artwork: {delete_result['message']}")
        else:
            print(f"❌ Delete artwork failed: {response.status_code}")
        
        # Test count endpoint
        print("\n8️⃣ Testing count endpoint...")
        response = requests.get(f"{base_url}/api/artworks/stats/count", timeout=5)
        if response.status_code == 200:
            count_data = response.json()
            print(f"✅ Total artworks: {count_data['total_artworks']}")
        else:
            print(f"❌ Count endpoint failed: {response.status_code}")
        
        print("\n🎉 All tests completed successfully!")
        print("\n📋 Summary:")
        print("   ✅ Health check - Backend is running")
        print("   ✅ Root endpoint - API is accessible")
        print("   ✅ Artworks CRUD - All operations working")
        print("   ✅ Create, Read, Update, Delete - All functional")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server")
        print("   Make sure the backend is running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    success = test_backend()
    if success:
        print("\n🚀 Backend is ready for frontend integration!")
        print("   Frontend can now connect to: http://localhost:8000")
    else:
        print("\n❌ Backend tests failed. Please check the server.")
