import { LockOutlined, SafetyOutlined } from '@ant-design/icons'
import { App as AntApp, Button, Card, Form, Input, Spin, Typography } from 'antd'
import React, { useEffect, useState } from 'react'
import { Link, Navigate, useNavigate, useSearchParams } from 'react-router-dom'

import { useAuth } from '@/auth/AuthContext'
import { resetPasswordRequest, validatePasswordResetTokenRequest } from '@/api/client'
import { BrandLogo } from '@/components/BrandLogo'

export const ResetPasswordPage: React.FC = () => {
  const { user } = useAuth()
  const { message } = AntApp.useApp()
  const nav = useNavigate()
  const [searchParams] = useSearchParams()
  const token = (searchParams.get('token') ?? '').trim()
  const [form] = Form.useForm()
  const [checking, setChecking] = useState(true)
  const [tokenOk, setTokenOk] = useState(false)
  const [submitting, setSubmitting] = useState(false)

  if (user) {
    return <Navigate to="/" replace />
  }

  useEffect(() => {
    if (!token) {
      setTokenOk(false)
      setChecking(false)
      return
    }
    let cancelled = false
    const run = async () => {
      setChecking(true)
      try {
        const { ok } = await validatePasswordResetTokenRequest(token)
        if (!cancelled) {
          setTokenOk(ok)
        }
      } catch {
        if (!cancelled) {
          setTokenOk(false)
        }
      } finally {
        if (!cancelled) {
          setChecking(false)
        }
      }
    }
    void run()
    return () => {
      cancelled = true
    }
  }, [token])

  const handleFinish = async (v: { new_password: string; new_password2: string }) => {
    setSubmitting(true)
    try {
      await resetPasswordRequest({
        token,
        new_password: v.new_password,
        new_password_confirm: v.new_password2,
      })
      message.success('Пароль обновлён. Войдите с новым паролем.')
      nav('/login', { replace: true })
    } catch (e) {
      message.error(e instanceof Error ? e.message : 'Не удалось сменить пароль')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div
      style={{
        minHeight: '100dvh',
        padding: 24,
        paddingTop: 'max(24px, env(safe-area-inset-top, 0px))',
        background:
          'radial-gradient(1200px 600px at 20% 0%, rgba(61,126,255,0.18), transparent), #f5f7fa',
      }}
    >
      <div style={{ maxWidth: 480, margin: '0 auto' }}>
        <div style={{ display: 'flex', justifyContent: 'center', marginBottom: 20 }}>
          <BrandLogo height={36} />
        </div>
        <Card style={{ borderColor: '#e2e8f0', background: '#ffffff' }}>
          <Typography.Title
            level={4}
            style={{ marginTop: 0, color: '#0f172a', display: 'flex', alignItems: 'center', gap: 8 }}
          >
            <SafetyOutlined /> Новый пароль
          </Typography.Title>
          {checking ? (
            <div style={{ display: 'grid', placeItems: 'center', padding: 32 }}>
              <Spin size="large" />
            </div>
          ) : !token || !tokenOk ? (
            <>
              <Typography.Paragraph type="secondary">
                Ссылка недействительна или срок её действия истёк. Запросите новую на странице «Забыли пароль?».
              </Typography.Paragraph>
              <Link to="/forgot-password">
                <Button type="primary" block size="large">
                  Запросить ссылку снова
                </Button>
              </Link>
              <div style={{ marginTop: 12, textAlign: 'center' }}>
                <Link to="/login">Вход</Link>
              </div>
            </>
          ) : (
            <>
              <Typography.Paragraph type="secondary" style={{ marginBottom: 20 }}>
                Придумайте новый пароль и введите его дважды.
              </Typography.Paragraph>
              <Form form={form} layout="vertical" onFinish={handleFinish}>
                <Form.Item name="new_password" label="Новый пароль" rules={[{ required: true, min: 8 }]}>
                  <Input.Password
                    prefix={<LockOutlined />}
                    autoComplete="new-password"
                    size="large"
                  />
                </Form.Item>
                <Form.Item
                  name="new_password2"
                  label="Повторите пароль"
                  dependencies={['new_password']}
                  rules={[
                    { required: true },
                    ({ getFieldValue }) => ({
                      validator(_, value) {
                        if (!value || getFieldValue('new_password') === value) {
                          return Promise.resolve()
                        }
                        return Promise.reject(new Error('Пароли не совпадают'))
                      },
                    }),
                  ]}
                >
                  <Input.Password
                    prefix={<LockOutlined />}
                    autoComplete="new-password"
                    size="large"
                  />
                </Form.Item>
                <Button type="primary" htmlType="submit" size="large" block loading={submitting}>
                  Сохранить пароль
                </Button>
                <div style={{ marginTop: 12, textAlign: 'center' }}>
                  <Link to="/login">Назад ко входу</Link>
                </div>
              </Form>
            </>
          )}
        </Card>
      </div>
    </div>
  )
}
