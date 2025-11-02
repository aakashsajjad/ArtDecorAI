# How to Fix Row-Level Security Policy Error

## Problem
You're getting this error when trying to add a record:
```
new row violates row-level security policy for table "artwork"
```

This happens because Row-Level Security (RLS) is enabled on the `artwork` table, but there's no policy allowing inserts.

## Solution

You need to add policies to allow INSERT, UPDATE, and DELETE operations on the artwork table.

### Option 1: Using Supabase Dashboard (Recommended)

1. **Go to your Supabase Dashboard**: https://supabase.com/dashboard
2. **Select your project**
3. **Navigate to SQL Editor** (left sidebar)
4. **Open a New Query**
5. **Copy and paste this SQL**:

```sql
-- Create policy for inserting artwork records
CREATE POLICY "Anyone can insert artwork" ON public.artwork
    FOR INSERT WITH CHECK (true);

-- Create policy for updating artwork records
CREATE POLICY "Anyone can update artwork" ON public.artwork
    FOR UPDATE USING (true);

-- Create policy for deleting artwork records
CREATE POLICY "Anyone can delete artwork" ON public.artwork
    FOR DELETE USING (true);
```

6. **Click "Run"** to execute the query
7. **Verify** the policies were created:
```sql
SELECT * FROM pg_policies WHERE schemaname = 'public' AND tablename = 'artwork';
```

### Option 2: Using Migration File

If you want to add this to your migrations:

1. The migration file is already created: `supabase/migrations/20240102000000_add_artwork_insert_policy.sql`
2. To apply it manually, copy the content and run it in Supabase SQL Editor
3. Or if using Supabase CLI: `supabase db push`

### Option 3: Using the Provided SQL File

1. Open `supabase/add_artwork_permissions.sql`
2. Copy the contents
3. Run it in your Supabase SQL Editor

## Verify the Fix

After adding the policies, try running your test script again:

```bash
cd backend
python test_add_record.py
```

Or:

```bash
cd backend
python demo_add_record.py
```

You should now see:
```
✅ Connection successful!
Adding sample record...
✅ Sample record added successfully
📝 Artwork ID: <some-uuid>
```

## Alternative Solution: Use Service Role Key

If you don't want to modify the policies (for security reasons), you can use the **Service Role Key** which bypasses RLS:

1. In Supabase Dashboard, go to **Settings** > **API**
2. Find your **Service Role Key** (keep it secret!)
3. Add it to `backend/.env`:
   ```
   SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here
   ```

**Warning:** The service role key has full access to your database and bypasses all RLS policies. Only use it in secure, server-side environments.

## What Policies Are Now in Place?

After adding these policies, your artwork table will have:

| Operation | Policy Name | Effect |
|-----------|-------------|--------|
| SELECT | "Public artwork is viewable by everyone" | ✅ Anyone can read |
| INSERT | "Anyone can insert artwork" | ✅ Anyone can create |
| UPDATE | "Anyone can update artwork" | ✅ Anyone can update |
| DELETE | "Anyone can delete artwork" | ✅ Anyone can delete |

## Need More Security?

If you want more restrictive policies (e.g., only authenticated users, or specific roles), you can modify the policies to check for authentication:

```sql
-- Example: Only authenticated users can modify
CREATE POLICY "Authenticated users can insert" ON public.artwork
    FOR INSERT TO authenticated WITH CHECK (true);

CREATE POLICY "Authenticated users can update" ON public.artwork
    FOR UPDATE TO authenticated USING (auth.uid() IS NOT NULL);

CREATE POLICY "Authenticated users can delete" ON public.artwork
    FOR DELETE TO authenticated USING (auth.uid() IS NOT NULL);
```

## Summary

The fastest way to fix the error is to run the SQL in `supabase/add_artwork_permissions.sql` in your Supabase SQL Editor. This will allow your backend code to insert records into the artwork table.

