"""
Quick test script for the new FastAPI endpoint
"""
import requests
import time

def test_fastapi_endpoint():
    """Test the new /api/artworks/sample endpoint"""
    base_url = "http://localhost:8000"
    
    print("=" * 60)
    print("Testing FastAPI Endpoints")
    print("=" * 60)
    print()
    
    # Wait a moment for server to be ready
    print("1. Checking if server is running...")
    try:
        response = requests.get(f"{base_url}/health", timeout=2)
        if response.status_code == 200:
            print("   ✅ Server is running!")
            print(f"   Status: {response.json()}")
        else:
            print(f"   ⚠️  Server responded with status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   ❌ Server is NOT running!")
        print()
        print("   Please start the server first:")
        print("   - Run: run_fastapi.bat")
        print("   - Or: python run_fastapi.py")
        print("   - Or: python main.py")
        return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    print()
    print("2. Testing new /api/artworks/sample endpoint...")
    try:
        response = requests.post(f"{base_url}/api/artworks/sample")
        if response.status_code == 201:
            print("   ✅ Success!")
            print(f"   Response: {response.json()}")
        else:
            print(f"   ⚠️  Status: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    print("3. Testing GET /api/artworks/ endpoint...")
    try:
        response = requests.get(f"{base_url}/api/artworks/")
        if response.status_code == 200:
            artworks = response.json()
            print(f"   ✅ Success! Found {len(artworks)} artwork(s)")
            if artworks:
                print(f"   First artwork: {artworks[0].get('title', 'N/A')}")
        else:
            print(f"   ⚠️  Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    print("=" * 60)
    print("To test manually:")
    print("- Open browser: http://localhost:8000/docs")
    print("- Or use curl: curl -X POST http://localhost:8000/api/artworks/sample")
    print("=" * 60)

if __name__ == "__main__":
    test_fastapi_endpoint()

