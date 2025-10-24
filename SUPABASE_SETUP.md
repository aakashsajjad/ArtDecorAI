# Supabase Local Development Setup

This guide will help you set up Supabase locally for the ArtDecorAI project.

## Prerequisites

- Node.js (version 18 or higher recommended)
- Docker Desktop (for local Supabase instance)
- Git

## Quick Start

### 1. Environment Setup

1. Copy the environment template:
   ```bash
   cp frontend/env.example frontend/.env.local
   ```

2. The default environment variables are already configured for local development.

### 2. Start Supabase Locally

Since the Supabase CLI installation had compatibility issues with the current Node.js version, you can use Docker directly or try alternative installation methods:

#### Option A: Using Docker (Recommended)
```bash
# Start Supabase services using Docker
docker run --name supabase-db -e POSTGRES_PASSWORD=postgres -p 54322:5432 -d postgres:15

# Or use the Supabase Docker Compose setup
# Download the official Supabase Docker Compose file and run it
```

#### Option B: Try Supabase CLI with different Node version
```bash
# If you have nvm installed, try with Node 18+
nvm use 18
npm install -g supabase
```

### 3. Initialize Database Schema

The database schema is already configured in the `supabase/migrations/` directory. To apply it:

```bash
# If Supabase CLI is working:
supabase db reset

# Or manually run the SQL files in your database
```

### 4. Seed the Database

```bash
# If Supabase CLI is working:
supabase db seed

# Or manually run the seed.sql file
```

## Database Schema

The ArtDecorAI project uses the following main tables:

### Core Tables

- **`artwork`** - Stores artwork information (title, brand, price, style tags, etc.)
- **`artwork_embedding`** - Vector embeddings for AI similarity search
- **`room_upload`** - User-uploaded room images and analysis data
- **`session`** - User interaction sessions and recommendations
- **`user_profile`** - User preferences and style profiles

### Key Features

- **Row Level Security (RLS)** - Enabled on all tables for data protection
- **Vector Search** - Using pgvector extension for AI-powered recommendations
- **JSONB Support** - For flexible data storage (color palettes, lighting data)
- **Array Support** - For style tags and recommendation IDs

## API Usage

### Supabase Client Setup

The project includes a pre-configured Supabase client in `frontend/src/lib/supabase.js`:

```javascript
import { supabase, db, auth } from '../lib/supabase'

// Authentication
const { user, error } = await auth.signIn(email, password)

// Database operations
const artworks = await db.getArtworks()
const userProfile = await db.getUserProfile(userId)
```

### React Hooks

Custom hooks are available for easy integration:

```javascript
import { useAuth } from '../hooks/useAuth'
import { useSupabase } from '../hooks/useSupabase'

function MyComponent() {
  const { user, signIn, signOut } = useAuth()
  const { getArtworks, loading, error } = useSupabase()
  
  // Use the hooks in your component
}
```

## Development Workflow

### 1. Start Development Server

```bash
cd frontend
npm run dev
```

### 2. Start Supabase (if CLI is working)

```bash
# In project root
supabase start
```

### 3. Access Services

- **Next.js App**: http://localhost:3000
- **Supabase Studio**: http://localhost:54323
- **API**: http://localhost:54321
- **Database**: localhost:54322

## Environment Variables

### Local Development (.env.local)

```env
NEXT_PUBLIC_SUPABASE_URL=http://localhost:54321
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0
```

### Production

Replace with your actual Supabase project credentials:

```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project-ref.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

## Database Functions

### Vector Search Function

For AI-powered artwork recommendations, you'll need to create a vector search function:

```sql
CREATE OR REPLACE FUNCTION match_artworks(
  query_embedding vector(384),
  match_threshold float,
  match_count int
)
RETURNS TABLE (
  id uuid,
  title text,
  brand text,
  price decimal,
  style_tags text[],
  dominant_palette jsonb,
  image_url text,
  similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    a.id,
    a.title,
    a.brand,
    a.price,
    a.style_tags,
    a.dominant_palette,
    a.image_url,
    1 - (ae.vector <=> query_embedding) as similarity
  FROM artwork_embedding ae
  JOIN artwork a ON ae.artwork_id = a.id
  WHERE 1 - (ae.vector <=> query_embedding) > match_threshold
  ORDER BY ae.vector <=> query_embedding
  LIMIT match_count;
END;
$$;
```

## Troubleshooting

### Common Issues

1. **Node.js Version Compatibility**
   - Supabase CLI requires Node.js 18+
   - Use nvm to switch versions: `nvm use 18`

2. **Docker Issues**
   - Ensure Docker Desktop is running
   - Check if ports 54321-54324 are available

3. **Database Connection**
   - Verify environment variables are correct
   - Check if Supabase services are running

### Alternative Setup

If Supabase CLI continues to have issues, you can:

1. Use a cloud Supabase project for development
2. Set up PostgreSQL manually with the provided schema
3. Use Docker Compose with the official Supabase stack

## Next Steps

1. **Test the Setup**: Try running the Next.js app and check if Supabase connection works
2. **Add Sample Data**: Use the seed data or add your own artwork entries
3. **Implement Features**: Start building the AI-powered recommendation features
4. **Deploy**: When ready, deploy to production with a cloud Supabase project

## Resources

- [Supabase Documentation](https://supabase.com/docs)
- [Next.js with Supabase Guide](https://supabase.com/docs/guides/getting-started/quickstarts/nextjs)
- [pgvector Documentation](https://github.com/pgvector/pgvector)
- [Row Level Security Guide](https://supabase.com/docs/guides/auth/row-level-security)
