import React from 'react'
import { Navigate, Route, Routes } from 'react-router-dom'

import { ProtectedRoute } from '@/components/ProtectedRoute'
import { LoginPage } from '@/pages/LoginPage'
import { ManagerStreamPage } from '@/pages/ManagerStreamPage'
import { ManagerStreamsPage } from '@/pages/ManagerStreamsPage'
import { OperatorEventPage } from '@/pages/OperatorEventPage'
import { OperatorHomePage } from '@/pages/OperatorHomePage'
import { RoleHome } from '@/pages/RoleHome'
import { SuperadminPage } from '@/pages/SuperadminPage'

export const App: React.FC = () => {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <RoleHome />
          </ProtectedRoute>
        }
      />
      <Route
        path="/operator"
        element={
          <ProtectedRoute roles={['OPERATOR', 'SUPERADMIN']}>
            <OperatorHomePage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/operator/:id"
        element={
          <ProtectedRoute roles={['OPERATOR', 'SUPERADMIN']}>
            <OperatorEventPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/manager"
        element={
          <ProtectedRoute roles={['STREAM_MANAGER', 'SUPERADMIN']}>
            <ManagerStreamsPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/manager/:id"
        element={
          <ProtectedRoute roles={['STREAM_MANAGER', 'SUPERADMIN']}>
            <ManagerStreamPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin"
        element={
          <ProtectedRoute roles={['SUPERADMIN']}>
            <SuperadminPage />
          </ProtectedRoute>
        }
      />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
