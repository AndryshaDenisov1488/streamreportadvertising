import { Spin } from 'antd'
import React from 'react'
import { Navigate, useLocation } from 'react-router-dom'

import type { UserRole } from '@/api/types'
import { useAuth } from '@/auth/AuthContext'

type Props = {
  children: React.ReactNode
  roles?: UserRole[]
}

export const ProtectedRoute: React.FC<Props> = ({ children, roles }) => {
  const { user, loading } = useAuth()
  const location = useLocation()

  if (loading) {
    return (
      <div style={{ display: 'grid', placeItems: 'center', minHeight: '60vh' }}>
        <Spin size="large" />
      </div>
    )
  }

  if (!user) {
    return <Navigate to="/login" replace />
  }

  if (location.pathname === '/first-login' && !user.suggest_password_change) {
    return <Navigate to={user.onboarding_completed ? '/dashboard' : '/onboarding'} replace />
  }

  if (!user.onboarding_completed) {
    if (user.suggest_password_change && location.pathname !== '/first-login') {
      return <Navigate to="/first-login" replace />
    }
    if (!user.suggest_password_change && location.pathname !== '/onboarding') {
      return <Navigate to="/onboarding" replace />
    }
  }

  if (roles && !roles.includes(user.role)) {
    return <Navigate to="/" replace />
  }

  return <>{children}</>
}
