import { LockOutlined, UserOutlined } from '@ant-design/icons'
import { App as AntApp, Button, Card, Form, Input, Typography } from 'antd'
import React from 'react'
import { Navigate, useNavigate } from 'react-router-dom'

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
        minHeight: '100%',
        display: 'grid',
        placeItems: 'center',
        padding: 24,
        background: 'radial-gradient(1200px 600px at 20% 0%, rgba(61,126,255,0.18), transparent), #070b10',
      }}
    >
      <Card
        style={{ width: 420, maxWidth: '100%', borderColor: '#1f2a3a', background: '#0d1219' }}
        bordered
      >
        <Typography.Title level={3} style={{ marginTop: 0, color: 'rgba(255,255,255,0.92)' }}>
          Панель эфиров
        </Typography.Title>
        <Typography.Paragraph type="secondary" style={{ marginBottom: 24 }}>
          Войдите для продолжения. Все времена — Москва.
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
