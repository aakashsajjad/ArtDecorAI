import { useState, useEffect } from 'react'
import { supabase, db } from '../lib/supabase'

export function useSupabase() {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // Artwork operations
  const getArtworks = async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await db.getArtworks()
      return data
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }

  const getArtworkById = async (id) => {
    setLoading(true)
    setError(null)
    try {
      const data = await db.getArtworkById(id)
      return data
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }

  const searchArtworksByStyle = async (styleTags) => {
    setLoading(true)
    setError(null)
    try {
      const data = await db.searchArtworksByStyle(styleTags)
      return data
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }

  // Room upload operations
  const saveRoomUpload = async (roomData) => {
    setLoading(true)
    setError(null)
    try {
      const data = await db.saveRoomUpload(roomData)
      return data
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }

  const getUserRoomUploads = async (userId) => {
    setLoading(true)
    setError(null)
    try {
      const data = await db.getUserRoomUploads(userId)
      return data
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }

  // Session operations
  const saveSession = async (sessionData) => {
    setLoading(true)
    setError(null)
    try {
      const data = await db.saveSession(sessionData)
      return data
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }

  const getUserSessions = async (userId) => {
    setLoading(true)
    setError(null)
    try {
      const data = await db.getUserSessions(userId)
      return data
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }

  // User profile operations
  const getUserProfile = async (userId) => {
    setLoading(true)
    setError(null)
    try {
      const data = await db.getUserProfile(userId)
      return data
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }

  const upsertUserProfile = async (profileData) => {
    setLoading(true)
    setError(null)
    try {
      const data = await db.upsertUserProfile(profileData)
      return data
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }

  // Vector search operations
  const searchSimilarArtworks = async (embedding, limit = 5) => {
    setLoading(true)
    setError(null)
    try {
      const data = await db.searchSimilarArtworks(embedding, limit)
      return data
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }

  return {
    loading,
    error,
    // Artwork operations
    getArtworks,
    getArtworkById,
    searchArtworksByStyle,
    // Room upload operations
    saveRoomUpload,
    getUserRoomUploads,
    // Session operations
    saveSession,
    getUserSessions,
    // User profile operations
    getUserProfile,
    upsertUserProfile,
    // Vector search operations
    searchSimilarArtworks
  }
}
