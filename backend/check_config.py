"""
Diagnostic script to check Supabase configuration
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
backend_env_path = Path(__file__).resolve().parent / ".env"
if backend_env_path.exists():
    load_dotenv(dotenv_path=backend_env_path, override=False)
    print("✅ Found backend/.env file")
else:
    print("⚠️  No backend/.env file found")

print("\n" + "=" * 60)
print("Current Configuration:")
print("=" * 60)

supabase_url = (
    os.getenv("SUPABASE_URL")
    or os.getenv("NEXT_PUBLIC_SUPABASE_URL")
    or "https://zcgjlmdvztxakwubrjyg.supabase.co"
)
print(f"Supabase URL: {supabase_url}")

# Check which keys are available
has_service_key = bool(os.getenv("SUPABASE_SERVICE_ROLE_KEY"))
has_anon_key = bool(os.getenv("SUPABASE_ANON_KEY") or os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY"))

print(f"\nAPI Keys:")
print(f"  Service Role Key: {'✅ SET' if has_service_key else '❌ NOT SET (will bypass RLS if set)'}")
print(f"  Anon Key: {'✅ SET' if has_anon_key else '❌ NOT SET (using fallback)'}")

if has_service_key:
    print("\n✅ GOOD: Service Role Key is set - this will bypass RLS policies!")
    print("   You should be able to insert records now.")
else:
    print("\n⚠️  Service Role Key is NOT set.")
    print("   You need to EITHER:")
    print("   1. Add Service Role Key to backend/.env (recommended)")
    print("   2. Add INSERT policy in Supabase Dashboard")

print("\n" + "=" * 60)
print("NEXT STEPS:")
print("=" * 60)

if not has_service_key:
    print("\nOption 1: Add Service Role Key (Easiest)")
    print("1. Go to: https://supabase.com/dashboard/project/zcgjlmdvztxakwubrjyg/settings/api")
    print("2. Find 'service_role' key (under 'Project API keys')")
    print("3. Copy it")
    print("4. Create backend/.env file with:")
    print("   SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here")
    print("5. Run test again: python test_add_record.py")
    
    print("\nOption 2: Add RLS Policy")
    print("1. Go to: https://supabase.com/dashboard/project/zcgjlmdvztxakwubrjyg/sql/new")
    print("2. Copy this SQL:")
    print("   CREATE POLICY IF NOT EXISTS \"Anyone can insert artwork\"")
    print("       ON public.artwork FOR INSERT WITH CHECK (true);")
    print("3. Click 'Run'")
    print("4. Run test again: python test_add_record.py")
else:
    print("\n✅ Configuration looks good!")
    print("   Run: python test_add_record.py")

