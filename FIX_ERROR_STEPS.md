# Fix the RLS Error - Step by Step

## You have 2 options to fix this:

### Option 1: Add RLS Policy (Recommended - 2 minutes)

1. **Go to Supabase Dashboard**: https://supabase.com/dashboard/project/zcgjlmdvztxakwubrjyg
2. **Click "SQL Editor"** (left sidebar)
3. **Click "New Query"**
4. **Copy and paste this SQL**:

```sql
CREATE POLICY IF NOT EXISTS "Anyone can insert artwork" 
    ON public.artwork 
    FOR INSERT 
    WITH CHECK (true);
```

5. **Click "Run"** (or press Ctrl+Enter)
6. **Test again**: Run `python test_add_record.py`

### Option 2: Use Service Role Key (Faster - 1 minute)

The Service Role Key bypasses all RLS policies.

1. **Go to Supabase Dashboard**: https://supabase.com/dashboard/project/zcgjlmdvztxakwubrjyg
2. **Click "Settings"** (gear icon, left sidebar)
3. **Click "API"**
4. **Find "service_role" key** (it's under "Project API keys")
5. **Copy the key** (it's very long, starts with `eyJ...`)
6. **Create or edit `backend/.env`** file:

```env
SUPABASE_URL=https://zcgjlmdvztxakwubrjyg.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here
```

7. **Save the file**
8. **Test again**: Run `python test_add_record.py`

⚠️ **Warning**: Service Role Key has full access. Keep it secret!

## What I Fixed in the Code

1. ✅ **Updated data format** to match your actual table:
   - `style_tags`: Now sends JSON string (not array)
   - `dominant_palette`: Now sends JSON string (not object)
   - `id`: Auto-generated (int4), not included

2. ✅ **Better error messages** - Now shows helpful hints when errors occur

3. ✅ **Direct insert** - Bypasses the CRUD layer to match your table structure exactly

## Test It Now

After applying Option 1 or 2, run:

```bash
cd backend
python test_add_record.py
```

You should see:
```
✅ Database connection successful!
✅ Sample record added successfully
📝 Artwork ID: <number>
```

