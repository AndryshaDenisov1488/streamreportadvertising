import {
  BarChartOutlined,
  CalendarOutlined,
  ControlOutlined,
  SettingOutlined,
  TeamOutlined,
} from '@ant-design/icons'
import { App as AntApp, Button, Card, Col, Row, Space, Statistic, Typography } from 'antd'
import { useQuery } from '@tanstack/react-query'
import React, { useEffect } from 'react'
import { Link } from 'react-router-dom'

import { getDashboardSummary } from '@/api/client'
import { useAuth } from '@/auth/AuthContext'
import { AppLayout } from '@/layouts/AppLayout'
import { userDisplayName } from '@/utils/userDisplay'

const cardIcon = (key: string) => {
  if (key.includes('mention')) {
    return <BarChartOutlined style={{ fontSize: 22, opacity: 0.85 }} />
  }
  if (key.includes('stream') || key.includes('event')) {
    return <CalendarOutlined style={{ fontSize: 22, opacity: 0.85 }} />
  }
  if (key.includes('user')) {
    return <TeamOutlined style={{ fontSize: 22, opacity: 0.85 }} />
  }
  if (key.includes('audit')) {
    return <ControlOutlined style={{ fontSize: 22, opacity: 0.85 }} />
  }
  if (key.includes('notif')) {
    return <SettingOutlined style={{ fontSize: 22, opacity: 0.85 }} />
  }
  return <BarChartOutlined style={{ fontSize: 22, opacity: 0.85 }} />
}

export const DashboardPage: React.FC = () => {
  const { user } = useAuth()
  const { message } = AntApp.useApp()

  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['dashboard'],
    queryFn: getDashboardSummary,
  })

  useEffect(() => {
    if (isError && error) {
      message.error(error instanceof Error ? error.message : 'Ошибка загрузки')
    }
  }, [isError, error, message])

  const role = user?.role

  return (
    <AppLayout
      nav={
        <Typography.Text type="secondary" style={{ fontSize: 13 }}>
          Обзор
        </Typography.Text>
      }
    >
      <Space direction="vertical" size={20} style={{ width: '100%' }}>
        <div>
          <Typography.Title level={3} style={{ marginTop: 0, marginBottom: 4 }}>
            {data?.title ?? 'Панель'}
          </Typography.Title>
          <Typography.Paragraph type="secondary" style={{ marginBottom: 0 }}>
            {user ? userDisplayName(user) : ''} · краткая сводка по вашей роли и быстрые переходы.
          </Typography.Paragraph>
        </div>

        <Card
          loading={isLoading}
          style={{
            borderColor: '#1f3a5f',
            background: 'linear-gradient(145deg, #0d1520 0%, #0a1018 100%)',
            borderRadius: 12,
          }}
          styles={{ body: { padding: 20 } }}
        >
          <Typography.Text strong style={{ color: 'rgba(255,255,255,0.75)', fontSize: 12, letterSpacing: 0.6 }}>
            ПОКАЗАТЕЛИ
          </Typography.Text>
          <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
            {(data?.cards ?? []).map((c) => (
              <Col xs={24} sm={12} lg={8} key={c.key}>
                <div
                  style={{
                    border: '1px solid #1f2a3a',
                    borderRadius: 10,
                    padding: 16,
                    background: 'rgba(15, 22, 32, 0.85)',
                    minHeight: 112,
                    display: 'flex',
                    gap: 14,
                    alignItems: 'flex-start',
                  }}
                >
                  <div style={{ color: '#5b8cff', marginTop: 2 }}>{cardIcon(c.key)}</div>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <Typography.Text type="secondary" style={{ fontSize: 12, display: 'block' }}>
                      {c.title}
                    </Typography.Text>
                    <Statistic
                      value={c.value}
                      valueStyle={{ color: 'rgba(255,255,255,0.95)', fontSize: 26, lineHeight: 1.2 }}
                    />
                    <Typography.Text type="secondary" style={{ fontSize: 11, display: 'block', marginTop: 6 }}>
                      {c.hint}
                    </Typography.Text>
                  </div>
                </div>
              </Col>
            ))}
          </Row>
        </Card>

        <Card
          title="Рабочие разделы"
          style={{ borderColor: '#1f2a3a', background: '#0d1219', borderRadius: 12 }}
          styles={{ header: { borderBottom: '1px solid #1f2a3a' } }}
        >
          <Space wrap size="middle">
            {role === 'OPERATOR' || role === 'SUPERADMIN' ? (
              <Link to="/operator">
                <Button type="primary" size="large">
                  События оператора
                </Button>
              </Link>
            ) : null}
            {role === 'STREAM_MANAGER' || role === 'SUPERADMIN' ? (
              <Link to="/manager">
                <Button type="primary" size="large" ghost>
                  Менеджер стримов
                </Button>
              </Link>
            ) : null}
            {role === 'SUPERADMIN' ? (
              <Link to="/admin">
                <Button size="large">Администрирование</Button>
              </Link>
            ) : null}
            <Link to="/profile">
              <Button size="large">Профиль и безопасность</Button>
            </Link>
          </Space>
        </Card>
      </Space>
    </AppLayout>
  )
}
