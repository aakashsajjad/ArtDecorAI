"""
Setup script for ArtDecorAI backend
"""
import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    if not os.path.exists(".env"):
        print("\n📝 Creating .env file...")
        try:
            with open("env.example", "r") as src:
                content = src.read()
            with open(".env", "w") as dst:
                dst.write(content)
            print("✅ .env file created from template")
            print("⚠️  Please edit .env file with your actual Supabase credentials")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        print("✅ .env file already exists")
        return True

def check_supabase_connection():
    """Check if Supabase is accessible"""
    print("\n🔍 Checking Supabase connection...")
    try:
        from database import db_connection
        if db_connection.test_connection():
            print("✅ Supabase connection successful")
            return True
        else:
            print("❌ Supabase connection failed")
            print("Please ensure:")
            print("1. Supabase is running locally (supabase start)")
            print("2. Database schema is created")
            print("3. Environment variables are correct")
            return False
    except Exception as e:
        print(f"❌ Supabase connection error: {e}")
        return False

def main():
    """Main setup function"""
    print("🎨 ArtDecorAI Backend Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Create .env file
    if not create_env_file():
        return False
    
    # Check Supabase connection
    if not check_supabase_connection():
        print("\n⚠️  Setup completed but Supabase connection failed.")
        print("You may need to:")
        print("1. Start Supabase locally: supabase start")
        print("2. Run database migrations")
        print("3. Check your .env file")
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Run CRUD operations: python run_crud.py")
    print("2. Start API server: python main.py")
    print("3. View API docs: http://localhost:8000/docs")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
