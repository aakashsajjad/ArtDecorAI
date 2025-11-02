# Quick Fix for Row-Level Security Error

## The Problem
You're getting this error:
```
Error adding record: {'message': 'new row violates row-level security policy for table "artwork"', 'code': '42501'}
```

## The Solution (2 Minutes)

You need to add database policies to allow inserting records. Follow these steps:

### Step 1: Open Your Supabase Dashboard
1. Go to: https://supabase.com/dashboard/project/zcgjlmdvztxakwubrjyg
2. Login if needed

### Step 2: Open SQL Editor
1. Click on **SQL Editor** in the left sidebar
2. Click **New Query**

### Step 3: Run This SQL
Copy and paste this code, then click **Run**:

```sql
-- Add policies to allow CRUD operations on artwork table
CREATE POLICY IF NOT EXISTS "Anyone can insert artwork" 
    ON public.artwork FOR INSERT WITH CHECK (true);

CREATE POLICY IF NOT EXISTS "Anyone can update artwork" 
    ON public.artwork FOR UPDATE USING (true);

CREATE POLICY IF NOT EXISTS "Anyone can delete artwork" 
    ON public.artwork FOR DELETE USING (true);
```

### Step 4: Verify It Worked
Run this query to see your policies:

```sql
SELECT policyname, cmd, qual 
FROM pg_policies 
WHERE schemaname = 'public' AND tablename = 'artwork';
```

You should see 4 policies:
- "Public artwork is viewable by everyone" (SELECT)
- "Anyone can insert artwork" (INSERT)
- "Anyone can update artwork" (UPDATE)
- "Anyone can delete artwork" (DELETE)

### Step 5: Test Your Code
Go back to your terminal and run:

```bash
cd backend
python test_add_record.py
```

You should now see:
```
✅ Database connection successful!
✅ Sample record added successfully
📝 Artwork ID: <some-uuid>
```

## Alternative: Use Service Role Key

If you can't modify the database policies, you can use the Service Role Key which bypasses RLS:

1. In Supabase Dashboard, go to **Settings** → **API**
2. Find **Service Role Key** (🔴 secret!)
3. Add to `backend/.env`:
   ```
   SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here
   ```

**⚠️ Warning:** Service Role Key bypasses ALL security policies. Only use on backend servers.

## Done! 🎉

Your code should now work. The issue was that your artwork table had RLS enabled but no policies allowing inserts.

