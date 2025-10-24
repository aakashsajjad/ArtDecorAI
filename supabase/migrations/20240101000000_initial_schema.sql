-- Initial schema migration for ArtDecorAI
-- This migration sets up the core database schema

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

-- Create artwork table
CREATE TABLE IF NOT EXISTS public.artwork (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    title TEXT NOT NULL,
    brand TEXT,
    price DECIMAL(10,2),
    style_tags TEXT[],
    dominant_palette JSONB,
    image_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create artwork_embedding table for vector storage
CREATE TABLE IF NOT EXISTS public.artwork_embedding (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    vector VECTOR(384), -- Vector embedding for similarity search
    artwork_id UUID REFERENCES public.artwork(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create room_upload table
CREATE TABLE IF NOT EXISTS public.room_upload (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID,
    room_type TEXT,
    s3_url TEXT,
    palette_json JSONB,
    lighting_json JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create session table
CREATE TABLE IF NOT EXISTS public.session (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID,
    query_text TEXT,
    topk_ids UUID[],
    chosen_id UUID,
    rationale TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create user_profile table
CREATE TABLE IF NOT EXISTS public.user_profile (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID UNIQUE,
    preferred_styles TEXT[],
    color_profile_json JSONB,
    budget_range JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_artwork_style_tags ON public.artwork USING GIN(style_tags);
CREATE INDEX IF NOT EXISTS idx_artwork_embedding_vector ON public.artwork_embedding USING ivfflat (vector vector_cosine_ops);
CREATE INDEX IF NOT EXISTS idx_room_upload_user_id ON public.room_upload(user_id);
CREATE INDEX IF NOT EXISTS idx_session_user_id ON public.session(user_id);

-- Enable Row Level Security (RLS)
ALTER TABLE public.artwork ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.artwork_embedding ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.room_upload ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.session ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_profile ENABLE ROW LEVEL SECURITY;

-- Create policies for public access to artwork (read-only)
CREATE POLICY "Public artwork is viewable by everyone" ON public.artwork
    FOR SELECT USING (true);

CREATE POLICY "Public artwork_embedding is viewable by everyone" ON public.artwork_embedding
    FOR SELECT USING (true);

-- Create policies for user-specific data
CREATE POLICY "Users can view their own room uploads" ON public.room_upload
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own room uploads" ON public.room_upload
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view their own sessions" ON public.session
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own sessions" ON public.session
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view their own profile" ON public.user_profile
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can update their own profile" ON public.user_profile
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own profile" ON public.user_profile
    FOR INSERT WITH CHECK (auth.uid() = user_id);
