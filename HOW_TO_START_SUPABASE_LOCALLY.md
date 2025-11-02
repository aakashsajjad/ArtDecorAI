# How to Start Supabase Locally

## Quick Summary
To run Supabase locally, you need the **Supabase CLI** which requires **Node.js 18+**. Once installed, simply run `supabase start`.

## Method 1: Using Supabase CLI (Recommended)

### Step 1: Check Node.js Version
```bash
node --version
```
**Required:** Node.js 18 or higher

### Step 2: Install/Upgrade Node.js (if needed)
If your Node.js is below 18:

**Option A: Download from website**
- Visit: https://nodejs.org/
- Download and install Node.js 18 LTS or newer

**Option B: Using nvm (Node Version Manager)** - if you have it installed
```bash
nvm install 18
nvm use 18
```

### Step 3: Install Supabase CLI
```bash
npm install -g supabase
```

Verify installation:
```bash
supabase --version
```

### Step 4: Navigate to Project Directory
```bash
cd "C:\asif nawaz\Project03\ArtDecorAI-main\ArtDecorAI-main"
```

### Step 5: Start Supabase
```bash
supabase start
```

This will:
- Download required Docker images
- Start all Supabase services (PostgreSQL, API Gateway, Auth, Studio)
- Apply your migrations
- Show you connection details

**Expected output:**
```
Started supabase local development setup.

         API URL: http://localhost:54321
     GraphQL URL: http://localhost:54321/graphql/v1
          DB URL: postgresql://postgres:postgres@localhost:54322/postgres
      Studio URL: http://localhost:54323
    Inbucket URL: http://localhost:54324
      JWT secret: super-secret-jwt-token-with-at-least-32-characters-long
        anon key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
service_role key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Step 6: Verify It's Running
```bash
supabase status
```

### Step 7: Access Services
- **Supabase Studio**: http://localhost:54323
- **API**: http://localhost:54321
- **Database**: localhost:54322

### Step 8: Run Your Example
```bash
cd backend
python examples\artwork_examples.py
```

### Stop Supabase When Done
```bash
supabase stop
```

## Method 2: Using npx (Without Global Install)

If you can't install globally, use npx (requires Node 18+):

```bash
# Make sure you're in the project root
cd "C:\asif nawaz\Project03\ArtDecorAI-main\ArtDecorAI-main"

# Start Supabase using npx
npx supabase start
```

## Method 3: Docker Compose (Advanced - Not Recommended)

The official Supabase stack is complex and requires multiple services. The Supabase CLI handles this automatically. Manual Docker setup is not recommended unless you have specific requirements.

## Troubleshooting

### Issue: "Node.js version too old"
**Solution:** Upgrade to Node.js 18+ (see Step 2)

### Issue: "Docker is not running"
**Solution:** 
1. Start Docker Desktop
2. Wait for it to fully start (Docker icon in system tray)
3. Try `supabase start` again

### Issue: "Port already in use"
**Solution:**
```bash
# Stop existing Supabase instance
supabase stop

# Or manually stop the containers
docker ps
docker stop <container-id>
```

### Issue: "Permission denied" (Windows)
**Solution:** Run your terminal as Administrator

### Issue: Supabase CLI installation fails
**Solution:**
1. Ensure Node.js 18+ is installed
2. Try: `npm cache clean --force`
3. Try: `npm install -g supabase@latest`

## Verify Your Setup

After starting Supabase, test the connection:

```bash
# From backend directory
cd backend

# Test connection
python -c "from database import db_connection; print('Connected!' if db_connection.test_connection() else 'Failed')"
```

## What Gets Started?

When you run `supabase start`, it starts:
- **PostgreSQL** (port 54322) - Database
- **Kong API Gateway** (port 54321) - REST API endpoint
- **GoTrue** - Authentication service
- **PostgREST** - Auto-generated REST API
- **Supabase Studio** (port 54323) - Web interface
- **Inbucket** (port 54324) - Email testing

## Next Steps After Starting

1. ✅ Supabase is running locally
2. ✅ Your `backend/.env` already has the correct local URLs
3. ✅ Run your examples:
   ```bash
   cd backend
   python examples\artwork_examples.py
   ```

## Need Help?

If you encounter issues:
1. Check Docker is running: `docker ps`
2. Check Supabase status: `supabase status`
3. View logs: `supabase logs`
4. Restart: `supabase stop && supabase start`


