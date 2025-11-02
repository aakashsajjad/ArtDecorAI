-- COPY THIS ENTIRE FILE AND RUN IT IN SUPABASE SQL EDITOR
-- This will fix the RLS error immediately

-- Check existing policies first
SELECT policyname, cmd 
FROM pg_policies 
WHERE schemaname = 'public' AND tablename = 'artwork';

-- Drop existing policies if they exist (optional, to start fresh)
-- DROP POLICY IF EXISTS "Anyone can insert artwork" ON public.artwork;
-- DROP POLICY IF EXISTS "Anyone can update artwork" ON public.artwork;
-- DROP POLICY IF EXISTS "Anyone can delete artwork" ON public.artwork;

-- Create the INSERT policy (this fixes your error!)
CREATE POLICY IF NOT EXISTS "Anyone can insert artwork" 
    ON public.artwork 
    FOR INSERT 
    WITH CHECK (true);

-- Create UPDATE policy (optional, for completeness)
CREATE POLICY IF NOT EXISTS "Anyone can update artwork" 
    ON public.artwork 
    FOR UPDATE 
    USING (true);

-- Create DELETE policy (optional, for completeness)
CREATE POLICY IF NOT EXISTS "Anyone can delete artwork" 
    ON public.artwork 
    FOR DELETE 
    USING (true);

-- Verify the policies were created
SELECT policyname, cmd, qual 
FROM pg_policies 
WHERE schemaname = 'public' AND tablename = 'artwork'
ORDER BY cmd;

