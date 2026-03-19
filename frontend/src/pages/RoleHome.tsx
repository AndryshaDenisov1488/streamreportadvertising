import React from 'react'
import { Navigate } from 'react-router-dom'

import { useAuth } from '@/auth/AuthContext'

export const RoleHome: React.FC = () => {
  const { user } = useAuth()
  if (!user) {
    return <Navigate to="/login" replace />
  }
  if (user.role === 'OPERATOR') {
    return <Navigate to="/operator" replace />
  }
  if (user.role === 'STREAM_MANAGER') {
    return <Navigate to="/manager" replace />
  }
  return <Navigate to="/admin" replace />
}
