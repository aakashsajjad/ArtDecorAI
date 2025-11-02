-- ========================================
-- COPY THIS ENTIRE FILE AND RUN IN SUPABASE
-- ========================================
-- 
-- How to run:
-- 1. Go to: https://supabase.com/dashboard/project/zcgjlmdvztxakwubrjyg/sql/new
-- 2. Copy all the SQL below
-- 3. Paste it in the SQL Editor
-- 4. Click "Run" (or press Ctrl+Enter)
-- 5. You should see "Success" message
-- 6. Then run: python test_add_record.py
--
-- ========================================

-- Add INSERT policy for artwork table
CREATE POLICY IF NOT EXISTS "Anyone can insert artwork" 
    ON public.artwork 
    FOR INSERT 
    WITH CHECK (true);

-- Add UPDATE policy (optional)
CREATE POLICY IF NOT EXISTS "Anyone can update artwork" 
    ON public.artwork 
    FOR UPDATE 
    USING (true);

-- Add DELETE policy (optional)
CREATE POLICY IF NOT EXISTS "Anyone can delete artwork" 
    ON public.artwork 
    FOR DELETE 
    USING (true);

-- Add INSERT policy for artwork_embedding table
CREATE POLICY IF NOT EXISTS "Anyone can insert artwork_embedding" 
    ON public.artwork_embedding 
    FOR INSERT 
    WITH CHECK (true);

-- Add UPDATE policy for artwork_embedding (optional)
CREATE POLICY IF NOT EXISTS "Anyone can update artwork_embedding" 
    ON public.artwork_embedding 
    FOR UPDATE 
    USING (true);

-- Add DELETE policy for artwork_embedding (optional)
CREATE POLICY IF NOT EXISTS "Anyone can delete artwork_embedding" 
    ON public.artwork_embedding 
    FOR DELETE 
    USING (true);

-- Verify policies were created for artwork table
SELECT 
    'artwork' as "Table",
    policyname as "Policy Name",
    cmd as "Operation"
FROM pg_policies 
WHERE schemaname = 'public' AND tablename = 'artwork'
ORDER BY cmd;

-- Verify policies were created for artwork_embedding table
SELECT 
    'artwork_embedding' as "Table",
    policyname as "Policy Name",
    cmd as "Operation"
FROM pg_policies 
WHERE schemaname = 'public' AND tablename = 'artwork_embedding'
ORDER BY cmd;

-- You should see:
-- artwork table: 4 policies (SELECT, INSERT, UPDATE, DELETE)
-- artwork_embedding table: 4 policies (SELECT, INSERT, UPDATE, DELETE)
