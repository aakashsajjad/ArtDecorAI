import { useState, useEffect } from 'react'
import { supabase, auth } from '../lib/supabase'

export function useAuth() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Get initial session
    const getInitialSession = async () => {
      const { user, error } = await auth.getCurrentUser()
      if (error) {
        console.error('Error getting current user:', error)
      } else {
        setUser(user)
      }
      setLoading(false)
    }

    getInitialSession()

    // Listen for auth changes
    const { data: { subscription } } = auth.onAuthStateChange((event, session) => {
      setUser(session?.user ?? null)
      setLoading(false)
    })

    return () => subscription?.unsubscribe()
  }, [])

  const signUp = async (email, password) => {
    setLoading(true)
    const { data, error } = await auth.signUp(email, password)
    setLoading(false)
    return { data, error }
  }

  const signIn = async (email, password) => {
    setLoading(true)
    const { data, error } = await auth.signIn(email, password)
    setLoading(false)
    return { data, error }
  }

  const signOut = async () => {
    setLoading(true)
    const { error } = await auth.signOut()
    setLoading(false)
    return { error }
  }

  return {
    user,
    loading,
    signUp,
    signIn,
    signOut
  }
}
