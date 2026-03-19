import React from 'react'
import { Navigate } from 'react-router-dom'

import { useAuth } from '@/auth/AuthContext'

export const RoleHome: React.FC = () => {
  const { user } = useAuth()
  if (!user) {
    return <Navigate to="/login" replace />
  }
  return <Navigate to="/dashboard" replace />
}
