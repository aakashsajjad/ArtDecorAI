"""
Script to run FastAPI server
"""
import uvicorn

if __name__ == "__main__":
    print("=" * 60)
    print("Starting FastAPI Server")
    print("=" * 60)
    print()
    print("📡 Server is listening on: 0.0.0.0:8000 (all network interfaces)")
    print()
    print("🌐 Access the server at:")
    print("   • http://localhost:8000")
    print("   • http://127.0.0.1:8000")
    print()
    print("📚 API Documentation:")
    print("   • Swagger UI: http://localhost:8000/docs")
    print("   • ReDoc: http://localhost:8000/redoc")
    print()
    print("🔍 Test Endpoints:")
    print("   • Health: http://localhost:8000/health")
    print("   • Sample Artwork: http://localhost:8000/api/artworks/sample")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # 0.0.0.0 = listen on all interfaces (allows remote access)
        port=8000,
        reload=True,
        log_level="info"
    )
