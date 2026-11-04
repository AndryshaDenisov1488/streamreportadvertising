import { LockOutlined, SafetyOutlined } from '@ant-design/icons'
import { App as AntApp, Button, Card, Form, Input, Spin, Typography } from 'antd'
import React, { useEffect, useState } from 'react'
import { Link, useNavigate, useSearchParams } from 'react-router-dom'

import { acceptInviteRequest, previewInviteRequest } from '@/api/client'
import type { UserRole } from '@/api/types'
import { useAuth } from '@/auth/AuthContext'
import { BrandLogo } from '@/components/BrandLogo'

const roleTitle: Record<UserRole, string> = {
  SUPERADMIN: 'Суперадминистратор',
  STREAM_MANAGER: 'Менеджер',
  OPERATOR: 'Оператор',
}

export const AcceptInvitePage: React.FC = () => {
  const { message } = AntApp.useApp()
  const { adoptSession } = useAuth()
  const nav = useNavigate()
  const [searchParams] = useSearchParams()
  const token = (searchParams.get('token') ?? '').trim()
  const [form] = Form.useForm()
  const [checking, setChecking] = useState(true)
  const [preview, setPreview] = useState<{ fullName: string; role: UserRole } | null>(null)
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    if (!token) {
      setPreview(null)
      setChecking(false)
      return
    }
    let cancelled = false
    const run = async () => {
      setChecking(true)
      try {
        const data = await previewInviteRequest(token)
        if (cancelled) {
          return
        }
        if (data.ok && data.full_name && data.role) {
          setPreview({ fullName: data.full_name, role: data.role })
        } else {
          setPreview(null)
        }
      } catch {
        if (!cancelled) {
          setPreview(null)
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

  const handleFinish = async (values: { password: string; password2: string }) => {
    setSubmitting(true)
    try {
      const data = await acceptInviteRequest({
        token,
        password: values.password,
        password_confirm: values.password2,
      })
      adoptSession(data.user)
      nav('/', { replace: true })
    } catch (e) {
      message.error(e instanceof Error ? e.message : 'Не удалось сохранить пароль')
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
            <SafetyOutlined /> Задайте пароль
          </Typography.Title>
          {checking ? (
            <div style={{ display: 'grid', placeItems: 'center', padding: 32 }}>
              <Spin size="large" />
            </div>
          ) : !preview ? (
            <>
              <Typography.Paragraph type="secondary">
                Ссылка недействительна, уже использована или срок её действия истёк. Попросите администратора
                отправить приглашение ещё раз.
              </Typography.Paragraph>
              <Link to="/login">
                <Button type="primary" block size="large">
                  Ко входу
                </Button>
              </Link>
            </>
          ) : (
            <>
              <Typography.Paragraph style={{ marginBottom: 4 }}>
                {preview.fullName}
              </Typography.Paragraph>
              <Typography.Paragraph type="secondary" style={{ marginBottom: 20 }}>
                Роль: {roleTitle[preview.role]}. Придумайте пароль и введите его дважды. После сохранения учётка
                откроется.
              </Typography.Paragraph>
              <Form form={form} layout="vertical" onFinish={handleFinish}>
                <Form.Item name="password" label="Пароль" rules={[{ required: true, min: 8, message: 'Минимум 8 символов' }]}>
                  <Input.Password prefix={<LockOutlined />} autoComplete="new-password" size="large" />
                </Form.Item>
                <Form.Item
                  name="password2"
                  label="Повторите пароль"
                  dependencies={['password']}
                  rules={[
                    { required: true, message: 'Повторите пароль' },
                    ({ getFieldValue }) => ({
                      validator(_, value) {
                        if (!value || getFieldValue('password') === value) {
                          return Promise.resolve()
                        }
                        return Promise.reject(new Error('Пароли не совпадают'))
                      },
                    }),
                  ]}
                >
                  <Input.Password prefix={<LockOutlined />} autoComplete="new-password" size="large" />
                </Form.Item>
                <Button type="primary" htmlType="submit" size="large" block loading={submitting}>
                  Сохранить и открыть учётку
                </Button>
              </Form>
            </>
          )}
        </Card>
      </div>
    </div>
  )
}
