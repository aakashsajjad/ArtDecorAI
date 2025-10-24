-- Vector similarity search function for artwork recommendations
CREATE OR REPLACE FUNCTION match_artworks(
  query_embedding vector(384),
  match_threshold float DEFAULT 0.5,
  match_count int DEFAULT 5
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
