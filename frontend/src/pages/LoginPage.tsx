import { LockOutlined, UserOutlined } from '@ant-design/icons'
import { App as AntApp, Button, Card, Form, Input, Typography } from 'antd'
import React from 'react'
import { Navigate, useNavigate } from 'react-router-dom'

import { BrandLogo } from '@/components/BrandLogo'
import { useAuth } from '@/auth/AuthContext'

export const LoginPage: React.FC = () => {
  const { user, login } = useAuth()
  const nav = useNavigate()
  const { message } = AntApp.useApp()

  if (user) {
    return <Navigate to="/" replace />
  }

  const handleFinish = async (values: { email: string; password: string }) => {
    try {
      await login(values.email, values.password)
      nav('/', { replace: true })
    } catch (e) {
      message.error(e instanceof Error ? e.message : 'Ошибка входа')
    }
  }

  return (
    <div
      style={{
        minHeight: '100dvh',
        display: 'grid',
        placeItems: 'center',
        padding: 24,
        paddingTop: 'max(24px, env(safe-area-inset-top, 0px))',
        paddingBottom: 'max(24px, env(safe-area-inset-bottom, 0px))',
        background: 'radial-gradient(1200px 600px at 20% 0%, rgba(61,126,255,0.18), transparent), #f5f7fa',
      }}
    >
      <Card
        style={{ width: 420, maxWidth: '100%', borderColor: '#e2e8f0', background: '#ffffff' }}
        bordered
      >
        <div style={{ display: 'flex', justifyContent: 'center', marginBottom: 20 }}>
          <BrandLogo height={40} style={{ maxWidth: 'min(100%, 260px)' }} />
        </div>
        <Typography.Title level={3} style={{ marginTop: 0, color: '#0f172a', textAlign: 'center' }}>
          Панель эфиров
        </Typography.Title>
        <Typography.Paragraph type="secondary" style={{ marginBottom: 24 }}>
          Войдите для продолжения.
        </Typography.Paragraph>
        <Form layout="vertical" onFinish={handleFinish} requiredMark="optional">
          <Form.Item
            name="email"
            label="Email"
            rules={[{ required: true, type: 'email', message: 'Укажите email' }]}
          >
            <Input size="large" prefix={<UserOutlined />} placeholder="you@fed.ru" autoComplete="username" />
          </Form.Item>
          <Form.Item name="password" label="Пароль" rules={[{ required: true, message: 'Введите пароль' }]}>
            <Input.Password
              size="large"
              prefix={<LockOutlined />}
              placeholder="••••••••"
              autoComplete="current-password"
            />
          </Form.Item>
          <Button type="primary" htmlType="submit" size="large" block>
            Войти
          </Button>
        </Form>
      </Card>
    </div>
  )
}
