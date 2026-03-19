import { RocketOutlined, SafetyOutlined, TeamOutlined, UserOutlined } from '@ant-design/icons'
import {
  App as AntApp,
  Button,
  Card,
  Collapse,
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

import {
  changePasswordRequest,
  patchProfileRequest,
  uploadAvatarRequest,
} from '@/api/client'
import type { UserRole } from '@/api/types'
import { useAuth } from '@/auth/AuthContext'
import { BrandLogo } from '@/components/BrandLogo'

const roleCopy: Record<
  UserRole,
  { title: string; lines: string[] }
> = {
  SUPERADMIN: {
    title: 'Суперадминистратор',
    lines: [
      'Полный доступ: пользователи, аудит, продуктовая аналитика, все события и эфиры.',
      'Раздел «Администрирование» — создание учёток, приглашения, просмотр журнала действий.',
    ],
  },
  STREAM_MANAGER: {
    title: 'Менеджер стримов',
    lines: [
      'Создание и настройка событий (турниры, дни, ссылки на стримы, назначение операторов по дням).',
      'Запуск и остановка эфира, чек-лист, просмотр упоминаний спонсоров.',
    ],
  },
  OPERATOR: {
    title: 'Оператор',
    lines: [
      'Работа в назначенных днях турнира: открыть эфир, отмечать таймкоды упоминаний, вести чек-лист.',
      'В календаре видны только события, где вас назначили.',
    ],
  },
}

export const OnboardingPage: React.FC = () => {
  const { message } = AntApp.useApp()
  const { user, refreshMe } = useAuth()
  const nav = useNavigate()
  const [step, setStep] = useState(0)
  const [nameForm] = Form.useForm()
  const [pwdForm] = Form.useForm()
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
  const rc = roleCopy[currentRole]

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
    { title: 'Имя', icon: <UserOutlined /> },
    { title: 'Пароль', icon: <SafetyOutlined /> },
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
      <div style={{ maxWidth: 640, margin: '0 auto' }}>
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
              initialValues={{ first_name: user.first_name, last_name: user.last_name }}
              onFinish={async (v) => {
                try {
                  await patchProfileRequest({
                    first_name: v.first_name,
                    last_name: v.last_name,
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
                Имя и фамилия отображаются в панели и в отчётах. Потом их можно изменить в «Профиль».
              </Typography.Paragraph>
              <Form.Item name="last_name" label="Фамилия" rules={[{ required: true, whitespace: true }]}>
                <Input autoComplete="family-name" />
              </Form.Item>
              <Form.Item name="first_name" label="Имя" rules={[{ required: true, whitespace: true }]}>
                <Input autoComplete="given-name" />
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
                Пароль
              </Typography.Title>
              <Typography.Paragraph type="secondary">
                Если вам выдали временный пароль по почте — смените его здесь. Можно пропустить шаг и сменить позже в
                «Профиль».
              </Typography.Paragraph>
              <Form
                form={pwdForm}
                layout="vertical"
                onFinish={async (v) => {
                  try {
                    await changePasswordRequest(v.current_password, v.new_password)
                    await refreshMe()
                    message.success('Пароль обновлён')
                    setStep(3)
                  } catch (e) {
                    message.error(e instanceof Error ? e.message : 'Ошибка')
                  }
                }}
              >
                <Form.Item name="current_password" label="Текущий пароль" rules={[{ required: true }]}>
                  <Input.Password autoComplete="current-password" />
                </Form.Item>
                <Form.Item name="new_password" label="Новый пароль" rules={[{ required: true, min: 8 }]}>
                  <Input.Password autoComplete="new-password" />
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
                  <Input.Password autoComplete="new-password" />
                </Form.Item>
                <Space wrap>
                  <Button onClick={() => setStep(1)}>Назад</Button>
                  <Button onClick={() => setStep(3)}>Пропустить</Button>
                  <Button type="primary" htmlType="submit">
                    Сохранить и далее
                  </Button>
                </Space>
              </Form>
            </div>
          )}

          {step === 3 && (
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
                  <Button onClick={() => setStep(2)}>Назад</Button>
                  <Button type="primary" onClick={() => setStep(4)}>
                    Далее
                  </Button>
                </Space>
              </div>
            </div>
          )}

          {step === 4 && (
            <div>
              <Typography.Title level={4} style={{ marginTop: 0, color: 'rgba(255,255,255,0.92)' }}>
                Роли в системе
              </Typography.Title>
              <Typography.Paragraph type="secondary">
                Ваша текущая роль: <Tag color="blue">{rc.title}</Tag>
              </Typography.Paragraph>
              <Collapse
                bordered={false}
                style={{ background: 'transparent' }}
                items={[
                  {
                    key: 'mine',
                    label: (
                      <span>
                        <strong>Ваша роль</strong> — {rc.title}
                      </span>
                    ),
                    children: (
                      <ul style={{ margin: 0, paddingLeft: 20, color: 'rgba(255,255,255,0.75)' }}>
                        {rc.lines.map((line, i) => (
                          <li key={i} style={{ marginBottom: 8 }}>
                            {line}
                          </li>
                        ))}
                      </ul>
                    ),
                  },
                  {
                    key: 'op',
                    label: 'Оператор',
                    children: (
                      <Typography.Paragraph type="secondary" style={{ marginBottom: 0 }}>
                        {roleCopy.OPERATOR.lines.join(' ')}
                      </Typography.Paragraph>
                    ),
                  },
                  {
                    key: 'mgr',
                    label: 'Менеджер стримов',
                    children: (
                      <Typography.Paragraph type="secondary" style={{ marginBottom: 0 }}>
                        {roleCopy.STREAM_MANAGER.lines.join(' ')}
                      </Typography.Paragraph>
                    ),
                  },
                  {
                    key: 'adm',
                    label: 'Суперадминистратор',
                    children: (
                      <Typography.Paragraph type="secondary" style={{ marginBottom: 0 }}>
                        {roleCopy.SUPERADMIN.lines.join(' ')}
                      </Typography.Paragraph>
                    ),
                  },
                ]}
              />
              <Space wrap style={{ marginTop: 24 }}>
                <Button onClick={() => setStep(3)}>Назад</Button>
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
