import { message } from 'antd'
import React, { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react'

import type { UserOut } from '@/api/types'
import { getAccessToken, loginRequest, logoutRequest, meRequest, setAccessToken } from '@/api/client'

type AuthState = {
  user: UserOut | null
  loading: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => Promise<void>
  refreshMe: () => Promise<void>
}

const AuthContext = createContext<AuthState | undefined>(undefined)

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<UserOut | null>(null)
  const [loading, setLoading] = useState(true)

  const refreshMe = useCallback(async () => {
    const token = getAccessToken()
    if (!token) {
      setUser(null)
      setLoading(false)
      return
    }
    try {
      const data = await meRequest()
      setUser(data.user)
    } catch {
      setAccessToken(null)
      setUser(null)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    void refreshMe()
  }, [refreshMe])

  const login = useCallback(async (email: string, password: string) => {
    const data = await loginRequest(email, password)
    setUser(data.user)
    message.success('Вход выполнен')
  }, [])

  const logout = useCallback(async () => {
    try {
      await logoutRequest()
    } catch {
      setAccessToken(null)
    }
    setUser(null)
    message.info('Вы вышли')
  }, [])

  const value = useMemo(
    () => ({
      user,
      loading,
      login,
      logout,
      refreshMe,
    }),
    [user, loading, login, logout, refreshMe],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export const useAuth = (): AuthState => {
  const ctx = useContext(AuthContext)
  if (!ctx) {
    throw new Error('useAuth вне AuthProvider')
  }
  return ctx
}
