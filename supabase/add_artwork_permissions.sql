-- Add INSERT, UPDATE, and DELETE policies for artwork table
-- This allows anyone to perform CRUD operations on the artwork table
-- Run this in your Supabase SQL Editor

-- Create policy for inserting artwork records
CREATE POLICY "Anyone can insert artwork" ON public.artwork
    FOR INSERT WITH CHECK (true);

-- Create policy for updating artwork records
CREATE POLICY "Anyone can update artwork" ON public.artwork
    FOR UPDATE USING (true);

-- Create policy for deleting artwork records
CREATE POLICY "Anyone can delete artwork" ON public.artwork
    FOR DELETE USING (true);

-- Verify policies are created
SELECT * FROM pg_policies WHERE schemaname = 'public' AND tablename = 'artwork';

