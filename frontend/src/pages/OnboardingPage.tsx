import { RocketOutlined, TeamOutlined, UserOutlined } from '@ant-design/icons'
import {
  App as AntApp,
  Button,
  Card,
  Divider,
  Form,
  Input,
  Space,
  Steps,
  Tag,
  Typography,
  Upload,
} from 'antd'
import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { patchProfileRequest, uploadAvatarRequest } from '@/api/client'
import type { UserRole } from '@/api/types'
import { useAuth } from '@/auth/AuthContext'
import { BrandLogo } from '@/components/BrandLogo'
import { OtherRolesHint, PrimaryRoleTraining } from '@/content/onboardingRoleGuides'
import { normalizeRuMobilePhone } from '@/utils/normalizeRuMobilePhone'

const roleTitle: Record<UserRole, string> = {
  SUPERADMIN: 'Суперадминистратор',
  STREAM_MANAGER: 'Менеджер стримов',
  OPERATOR: 'Оператор',
}

export const OnboardingPage: React.FC = () => {
  const { message } = AntApp.useApp()
  const { user, refreshMe } = useAuth()
  const nav = useNavigate()
  const [step, setStep] = useState(0)
  const [nameForm] = Form.useForm()
  const [finishing, setFinishing] = useState(false)

  useEffect(() => {
    if (user?.onboarding_completed) {
      nav('/dashboard', { replace: true })
    }
  }, [user?.onboarding_completed, user, nav])

  if (!user) {
    return null
  }

  const currentRole = user.role as UserRole

  const handleSkipTour = async () => {
    setFinishing(true)
    try {
      await patchProfileRequest({ onboarding_completed: true })
      await refreshMe()
      message.info('Ознакомление пропущено — всё можно настроить позже в «Профиль»')
      nav('/dashboard', { replace: true })
    } catch (e) {
      message.error(e instanceof Error ? e.message : 'Ошибка')
    } finally {
      setFinishing(false)
    }
  }

  const handleFinish = async () => {
    setFinishing(true)
    try {
      await patchProfileRequest({ onboarding_completed: true })
      await refreshMe()
      message.success('Добро пожаловать в панель')
      nav('/dashboard', { replace: true })
    } catch (e) {
      message.error(e instanceof Error ? e.message : 'Ошибка')
    } finally {
      setFinishing(false)
    }
  }

  const steps = [
    { title: 'Старт', icon: <RocketOutlined /> },
    { title: 'Профиль', icon: <UserOutlined /> },
    { title: 'Аватар', icon: <UserOutlined /> },
    { title: 'Роли', icon: <TeamOutlined /> },
  ]

  return (
    <div
      style={{
        minHeight: '100dvh',
        padding: 24,
        paddingTop: 'max(24px, env(safe-area-inset-top, 0px))',
        background:
          'radial-gradient(1200px 600px at 20% 0%, rgba(61,126,255,0.18), transparent), #070b10',
      }}
    >
      <div style={{ maxWidth: step === 3 ? 760 : 640, margin: '0 auto' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
          <BrandLogo height={36} />
          <Button type="link" onClick={() => void handleSkipTour()} disabled={finishing}>
            Пропустить ознакомление
          </Button>
        </div>

        <Steps current={step} items={steps} responsive style={{ marginBottom: 28 }} />

        <Card style={{ borderColor: '#1f2a3a', background: '#0d1219' }}>
          {step === 0 && (
            <Space direction="vertical" size="middle" style={{ width: '100%' }}>
              <Typography.Title level={4} style={{ marginTop: 0, color: 'rgba(255,255,255,0.92)' }}>
                Добро пожаловать в MainStream Ops
              </Typography.Title>
              <Typography.Paragraph type="secondary" style={{ marginBottom: 0 }}>
                Это рабочая панель федерации: расписание эфиров, таймкоды спонсорских упоминаний, роли операторов и
                менеджеров. Сейчас коротко настроим профиль и покажем, что доступно именно вам.
              </Typography.Paragraph>
              <Button type="primary" size="large" block onClick={() => setStep(1)}>
                Начать
              </Button>
            </Space>
          )}

          {step === 1 && (
            <Form
              form={nameForm}
              layout="vertical"
              initialValues={{
                first_name: user.first_name,
                last_name: user.last_name,
                phone: user.phone ?? '',
              }}
              onFinish={async (v) => {
                try {
                  await patchProfileRequest({
                    first_name: v.first_name,
                    last_name: v.last_name,
                    phone: v.phone,
                  })
                  await refreshMe()
                  message.success('Сохранено')
                  setStep(2)
                } catch (e) {
                  message.error(e instanceof Error ? e.message : 'Ошибка')
                }
              }}
            >
              <Typography.Title level={4} style={{ marginTop: 0, color: 'rgba(255,255,255,0.92)' }}>
                Как к вам обращаться
              </Typography.Title>
              <Typography.Paragraph type="secondary">
                Имя, фамилия и мобильный телефон (Россия) — отображаются в панели и отчётах. Потом всё можно изменить в
                «Профиль». Телефон можно ввести как <Typography.Text code>79060943936</Typography.Text>,{' '}
                <Typography.Text code>89060943936</Typography.Text> или с пробелами — сохранится в едином формате.
              </Typography.Paragraph>
              <Form.Item name="last_name" label="Фамилия" rules={[{ required: true, whitespace: true }]}>
                <Input autoComplete="family-name" />
              </Form.Item>
              <Form.Item name="first_name" label="Имя" rules={[{ required: true, whitespace: true }]}>
                <Input autoComplete="given-name" />
              </Form.Item>
              <Form.Item
                name="phone"
                label="Мобильный телефон"
                rules={[
                  { required: true, message: 'Укажите телефон' },
                  {
                    validator: async (_, value: string) => {
                      const t = (value ?? '').trim()
                      if (!t) {
                        return Promise.reject(new Error('Укажите телефон'))
                      }
                      try {
                        normalizeRuMobilePhone(t)
                        return Promise.resolve()
                      } catch {
                        return Promise.reject(
                          new Error('Нужен российский мобильный: с 7, 8 или 9 (10 или 11 цифр)'),
                        )
                      }
                    },
                  },
                ]}
              >
                <Input placeholder="Например 79060943936 или 8 906 094-39-36" autoComplete="tel" inputMode="tel" />
              </Form.Item>
              <Space wrap>
                <Button onClick={() => setStep(0)}>Назад</Button>
                <Button type="primary" htmlType="submit">
                  Далее
                </Button>
              </Space>
            </Form>
          )}

          {step === 2 && (
            <div>
              <Typography.Title level={4} style={{ marginTop: 0, color: 'rgba(255,255,255,0.92)' }}>
                Аватар
              </Typography.Title>
              <Typography.Paragraph type="secondary">
                По желанию загрузите фото профиля (JPEG, PNG или WebP, до 2 МБ). Это можно сделать и позже в «Профиль».
              </Typography.Paragraph>
              <Upload
                accept="image/jpeg,image/png,image/webp"
                showUploadList={false}
                beforeUpload={(file) => {
                  void (async () => {
                    try {
                      await uploadAvatarRequest(file as File)
                      await refreshMe()
                      message.success('Аватар загружен')
                    } catch (e) {
                      message.error(e instanceof Error ? e.message : 'Ошибка загрузки')
                    }
                  })()
                  return false
                }}
              >
                <Button type="default">Выбрать файл</Button>
              </Upload>
              <div style={{ marginTop: 20 }}>
                <Space wrap>
                  <Button onClick={() => setStep(1)}>Назад</Button>
                  <Button type="primary" onClick={() => setStep(3)}>
                    Далее
                  </Button>
                </Space>
              </div>
            </div>
          )}

          {step === 3 && (
            <div>
              <Typography.Title level={4} style={{ marginTop: 0, color: 'rgba(255,255,255,0.92)' }}>
                Как пользоваться панелью
              </Typography.Title>
              <Typography.Paragraph type="secondary" style={{ marginBottom: 16 }}>
                Ваша роль: <Tag color="blue">{roleTitle[currentRole]}</Tag> — ниже пошаговая инструкция под неё (без
                повторов).
              </Typography.Paragraph>
              <PrimaryRoleTraining role={currentRole} />
              <Divider style={{ borderColor: '#1f2a3a', margin: '20px 0' }} />
              <Typography.Text strong style={{ display: 'block', marginBottom: 8, color: 'rgba(255,255,255,0.75)' }}>
                Остальные роли — кратко
              </Typography.Text>
              <OtherRolesHint currentRole={currentRole} />
              <Space wrap style={{ marginTop: 24 }}>
                <Button onClick={() => setStep(2)}>Назад</Button>
                <Button type="primary" size="large" loading={finishing} onClick={() => void handleFinish()}>
                  Перейти в панель
                </Button>
              </Space>
            </div>
          )}
        </Card>
      </div>
    </div>
  )
}
