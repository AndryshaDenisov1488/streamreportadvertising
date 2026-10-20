import { Card, Typography } from 'antd'
import React from 'react'

import type { UserRole } from '@/api/types'
import { useAuth } from '@/auth/AuthContext'
import { OtherRolesHint, PrimaryRoleTraining } from '@/content/onboardingRoleGuides'
import { AppLayout } from '@/layouts/AppLayout'

const roleTitle: Record<UserRole, string> = {
  SUPERADMIN: 'Суперадминистратор',
  STREAM_MANAGER: 'Менеджер',
  OPERATOR: 'Оператор',
}

export const HelpPage: React.FC = () => {
  const { user } = useAuth()
  const role = (user?.role ?? 'OPERATOR') as UserRole

  return (
    <AppLayout
      nav={
        <Typography.Text type="secondary" style={{ fontSize: 13 }}>
          Как работать
        </Typography.Text>
      }
    >
      <Typography.Title level={3} style={{ marginTop: 0 }}>
        Как работать
      </Typography.Title>
      <Typography.Paragraph type="secondary">
        Инструкция для роли «{roleTitle[role]}». Пункт «Как работать» в шапке открывает её в любой момент, не только
        при первом входе.
      </Typography.Paragraph>
      <Card style={{ borderColor: '#e2e8f0', background: '#ffffff', borderRadius: 12 }}>
        <PrimaryRoleTraining role={role} />
        <Typography.Title level={5} style={{ marginTop: 24 }}>
          Другие роли коротко
        </Typography.Title>
        <OtherRolesHint currentRole={role} />
      </Card>
    </AppLayout>
  )
}
