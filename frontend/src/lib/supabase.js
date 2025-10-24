import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error('Missing Supabase environment variables. Please check your .env.local file.')
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// Database helper functions
export const db = {
  // Artwork operations
  async getArtworks() {
    const { data, error } = await supabase
      .from('artwork')
      .select('*')
      .order('created_at', { ascending: false })
    
    if (error) throw error
    return data
  },

  async getArtworkById(id) {
    const { data, error } = await supabase
      .from('artwork')
      .select('*')
      .eq('id', id)
      .single()
    
    if (error) throw error
    return data
  },

  async searchArtworksByStyle(styleTags) {
    const { data, error } = await supabase
      .from('artwork')
      .select('*')
      .overlaps('style_tags', styleTags)
    
    if (error) throw error
    return data
  },

  // Room upload operations
  async saveRoomUpload(roomData) {
    const { data, error } = await supabase
      .from('room_upload')
      .insert(roomData)
      .select()
    
    if (error) throw error
    return data
  },

  async getUserRoomUploads(userId) {
    const { data, error } = await supabase
      .from('room_upload')
      .select('*')
      .eq('user_id', userId)
      .order('created_at', { ascending: false })
    
    if (error) throw error
    return data
  },

  // Session operations
  async saveSession(sessionData) {
    const { data, error } = await supabase
      .from('session')
      .insert(sessionData)
      .select()
    
    if (error) throw error
    return data
  },

  async getUserSessions(userId) {
    const { data, error } = await supabase
      .from('session')
      .select('*')
      .eq('user_id', userId)
      .order('created_at', { ascending: false })
    
    if (error) throw error
    return data
  },

  // User profile operations
  async getUserProfile(userId) {
    const { data, error } = await supabase
      .from('user_profile')
      .select('*')
      .eq('user_id', userId)
      .single()
    
    if (error && error.code !== 'PGRST116') throw error
    return data
  },

  async upsertUserProfile(profileData) {
    const { data, error } = await supabase
      .from('user_profile')
      .upsert(profileData, { onConflict: 'user_id' })
      .select()
    
    if (error) throw error
    return data
  },

  // Vector search operations (for AI recommendations)
  async searchSimilarArtworks(embedding, limit = 5) {
    const { data, error } = await supabase.rpc('match_artworks', {
      query_embedding: embedding,
      match_threshold: 0.5,
      match_count: limit
    })
    
    if (error) throw error
    return data
  }
}

// Auth helper functions
export const auth = {
  async signUp(email, password) {
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
    })
    return { data, error }
  },

  async signIn(email, password) {
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    })
    return { data, error }
  },

  async signOut() {
    const { error } = await supabase.auth.signOut()
    return { error }
  },

  async getCurrentUser() {
    const { data: { user }, error } = await supabase.auth.getUser()
    return { user, error }
  },

  async onAuthStateChange(callback) {
    return supabase.auth.onAuthStateChange(callback)
  }
}
