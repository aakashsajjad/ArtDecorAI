# Setup Guide: Running artwork_examples.py

## Current Status
✅ PostgreSQL container is running on port 54322
✅ Database schema partially applied (artwork table created)
❌ Supabase API gateway needed on port 54321

## Problem
The Supabase Python client requires the full Supabase stack including:
- PostgreSQL database (port 54322) ✅ Running
- Supabase API Gateway/Kong (port 54321) ❌ Not running
- Supabase Auth service
- Supabase Studio (port 54323)

## Solutions

### Option 1: Use Cloud Supabase (Recommended - Easiest)

1. **Sign up for free Supabase account**: https://supabase.com
2. **Create a new project**
3. **Get your credentials**:
   - Go to Project Settings > API
   - Copy your `Project URL` and `anon/public key`
4. **Update backend/.env**:
   ```
   SUPABASE_URL=https://your-project-ref.supabase.co
   SUPABASE_ANON_KEY=your-anon-key-here
   ```
5. **Apply database schema**:
   - Copy contents of `supabase/migrations/20240101000000_initial_schema.sql`
   - Go to Supabase Dashboard > SQL Editor
   - Run the SQL (skip vector extension parts if not needed)
6. **Run the example**:
   ```bash
   cd backend
   python examples/artwork_examples.py
   ```

### Option 2: Full Local Supabase Stack (Complex)

Requires Supabase CLI which needs Node.js 18+. Since your Node.js is 12.x:

1. **Upgrade Node.js to 18+** (or use nvm to switch versions)
2. **Install Supabase CLI**:
   ```bash
   npm install -g supabase
   ```
3. **Start Supabase**:
   ```bash
   supabase start
   ```
4. **Run the example**:
   ```bash
   cd backend
   python examples/artwork_examples.py
   ```

### Option 3: Direct PostgreSQL Connection (Requires code changes)

This would require modifying the database connection code to use PostgreSQL directly instead of Supabase client. Not recommended as it breaks the abstraction.

## Current PostgreSQL Container

If you want to use the PostgreSQL container we started:
- **Container**: `supabase-db-artdecorai`
- **Port**: 54322
- **User**: postgres
- **Password**: postgres
- **Database**: postgres

To connect directly with psql:
```bash
docker exec -it supabase-db-artdecorai psql -U postgres -d postgres
```

## Recommendation

**Use Option 1 (Cloud Supabase)** - It's free, takes 5 minutes to set up, and you get the full Supabase stack without local setup complexity.


