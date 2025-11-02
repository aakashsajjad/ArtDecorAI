-- Add INSERT policy for artwork table
-- This allows anyone to insert new artwork records

-- Create policy for inserting artwork records
CREATE POLICY "Anyone can insert artwork" ON public.artwork
    FOR INSERT WITH CHECK (true);

-- Create policy for updating artwork records (optional)
CREATE POLICY "Anyone can update artwork" ON public.artwork
    FOR UPDATE USING (true);

-- Create policy for deleting artwork records (optional)
CREATE POLICY "Anyone can delete artwork" ON public.artwork
    FOR DELETE USING (true);

