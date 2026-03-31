import { MailOutlined } from '@ant-design/icons'
import { App as AntApp, Button, Card, Form, Input, Typography } from 'antd'
import React, { useState } from 'react'
import { Link, Navigate, useNavigate } from 'react-router-dom'

import { useAuth } from '@/auth/AuthContext'
import { forgotPasswordRequest } from '@/api/client'
import { BrandLogo } from '@/components/BrandLogo'

export const ForgotPasswordPage: React.FC = () => {
  const { user } = useAuth()
  const nav = useNavigate()
  const { message } = AntApp.useApp()
  const [done, setDone] = useState(false)
  const [loading, setLoading] = useState(false)

  if (user) {
    return <Navigate to="/" replace />
  }

  const handleFinish = async (values: { email: string }) => {
    setLoading(true)
    try {
      const res = await forgotPasswordRequest(values.email.trim())
      message.success(res.message)
      setDone(true)
    } catch (e) {
      message.error(e instanceof Error ? e.message : 'Не удалось отправить запрос')
    } finally {
      setLoading(false)
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
          Забыли пароль?
        </Typography.Title>
        <Typography.Paragraph type="secondary" style={{ marginBottom: 24 }}>
          Укажите email учётной записи. Если он есть в системе, мы отправим ссылку для сброса пароля.
        </Typography.Paragraph>
        {done ? (
          <>
            <Typography.Paragraph>
              Проверьте почту (в том числе папку «Спам»). Ссылка для сброса активна 10 минут — откройте её сразу.
            </Typography.Paragraph>
            <Button type="primary" block size="large" onClick={() => nav('/login', { replace: true })}>
              Вернуться ко входу
            </Button>
          </>
        ) : (
          <Form layout="vertical" onFinish={handleFinish} requiredMark="optional">
            <Form.Item
              name="email"
              label="Email"
              rules={[{ required: true, type: 'email', message: 'Укажите email' }]}
            >
              <Input size="large" prefix={<MailOutlined />} placeholder="you@example.com" autoComplete="email" />
            </Form.Item>
            <Button type="primary" htmlType="submit" size="large" block loading={loading}>
              Отправить ссылку
            </Button>
            <div style={{ marginTop: 16, textAlign: 'center' }}>
              <Link to="/login">Назад ко входу</Link>
            </div>
          </Form>
        )}
      </Card>
    </div>
  )
}
