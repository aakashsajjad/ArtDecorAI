"""
Script to help fix the invalid API key error
"""
import os
from pathlib import Path
from dotenv import load_dotenv

print("=" * 60)
print("API Key Configuration Fix")
print("=" * 60)
print()

# Check if .env exists
env_path = Path(__file__).resolve().parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=False)
    print("✅ Found backend/.env file")
else:
    print("⚠️  No backend/.env file found")

print()
print("Current configuration:")
print("-" * 60)

# Check what keys are set
service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
anon_key = os.getenv("SUPABASE_ANON_KEY") or os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")

if service_key:
    print(f"✅ Service Role Key: SET (ends with: ...{service_key[-10:]})")
    print("   This should work and bypass RLS!")
elif anon_key:
    print(f"⚠️  Anon Key: SET (ends with: ...{anon_key[-10:]})")
    print("   This key might be invalid or expired")
else:
    print("❌ No API keys found in .env")
    print("   Using hardcoded fallback key (which is invalid)")

print()
print("=" * 60)
print("HOW TO FIX:")
print("=" * 60)
print()
print("Your API key is invalid or expired. Get a new one:")
print()
print("Step 1: Open Supabase Dashboard")
print("   https://supabase.com/dashboard/project/zcgjlmdvztxakwubrjyg/settings/api")
print()
print("Step 2: Get your keys")
print("   - Find 'anon' key (public key)")
print("   - Find 'service_role' key (secret key - recommended)")
print()
print("Step 3: Update backend/.env file")
print("   Add these lines:")
print("   SUPABASE_URL=https://zcgjlmdvztxakwubrjyg.supabase.co")
print("   SUPABASE_ANON_KEY=paste-your-anon-key-here")
print("   SUPABASE_SERVICE_ROLE_KEY=paste-your-service-role-key-here")
print()
print("Step 4: Save and test")
print("   python test_add_record.py")
print()
print("=" * 60)

