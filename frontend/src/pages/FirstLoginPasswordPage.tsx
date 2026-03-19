import { SafetyOutlined } from '@ant-design/icons'
import { App as AntApp, Button, Card, Form, Input, Space, Typography } from 'antd'
import React from 'react'
import { useNavigate } from 'react-router-dom'

import { changePasswordRequest, patchProfileRequest } from '@/api/client'
import { useAuth } from '@/auth/AuthContext'
import { BrandLogo } from '@/components/BrandLogo'

export const FirstLoginPasswordPage: React.FC = () => {
  const { message } = AntApp.useApp()
  const { user, refreshMe } = useAuth()
  const nav = useNavigate()
  const [form] = Form.useForm()
  const [skipping, setSkipping] = React.useState(false)
  const [submitting, setSubmitting] = React.useState(false)

  if (!user) {
    return null
  }

  const handleSkip = async () => {
    setSkipping(true)
    try {
      await patchProfileRequest({ suggest_password_change: false })
      await refreshMe()
      message.info('Можно сменить пароль позже в разделе «Профиль»')
      nav('/onboarding', { replace: true })
    } catch (e) {
      message.error(e instanceof Error ? e.message : 'Ошибка')
    } finally {
      setSkipping(false)
    }
  }

  const handleFinish = async (v: { current_password: string; new_password: string; new_password2: string }) => {
    setSubmitting(true)
    try {
      await changePasswordRequest(v.current_password, v.new_password)
      await refreshMe()
      message.success('Пароль обновлён — далее короткое знакомство с панелью')
      nav('/onboarding', { replace: true })
    } catch (e) {
      message.error(e instanceof Error ? e.message : 'Ошибка')
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
            <SafetyOutlined /> Первый вход: пароль
          </Typography.Title>
          <Typography.Paragraph type="secondary" style={{ marginBottom: 20 }}>
            В письме вам пришёл <strong>временный пароль</strong>. Рекомендуем задать свой — так безопаснее. Затем
            начнётся короткое знакомство с панелью.
          </Typography.Paragraph>

          <Form form={form} layout="vertical" onFinish={handleFinish}>
            <Form.Item name="current_password" label="Текущий пароль (из письма)" rules={[{ required: true }]}>
              <Input.Password autoComplete="current-password" size="large" />
            </Form.Item>
            <Form.Item name="new_password" label="Новый пароль" rules={[{ required: true, min: 8 }]}>
              <Input.Password autoComplete="new-password" size="large" />
            </Form.Item>
            <Form.Item
              name="new_password2"
              label="Повтор нового пароля"
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
              <Input.Password autoComplete="new-password" size="large" />
            </Form.Item>
            <Space wrap style={{ marginTop: 8 }}>
              <Button onClick={() => void handleSkip()} disabled={submitting} loading={skipping}>
                Сменить позже
              </Button>
              <Button type="primary" htmlType="submit" size="large" loading={submitting}>
                Сохранить и продолжить
              </Button>
            </Space>
          </Form>
        </Card>
      </div>
    </div>
  )
}
