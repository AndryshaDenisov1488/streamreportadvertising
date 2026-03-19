import { HistoryOutlined, SafetyOutlined, UserOutlined } from '@ant-design/icons'
import {
  App as AntApp,
  Avatar,
  Button,
  Card,
  Form,
  Input,
  Space,
  Table,
  Tabs,
  Tag,
  Typography,
  Upload,
} from 'antd'
import type { ColumnsType } from 'antd/es/table'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import React, { useEffect } from 'react'
import { Link } from 'react-router-dom'

import type { AuditLogOut, SessionOut } from '@/api/types'
import {
  changePasswordRequest,
  getMyActivityPage,
  listSessionsRequest,
  patchProfileRequest,
  revokeSessionRequest,
  uploadAvatarRequest,
} from '@/api/client'
import { useAuth } from '@/auth/AuthContext'
import { AppLayout } from '@/layouts/AppLayout'
import { formatDateTimeRu } from '@/utils/datetime'
import { normalizeRuMobilePhone } from '@/utils/normalizeRuMobilePhone'
import { userDisplayName } from '@/utils/userDisplay'

export const ProfilePage: React.FC = () => {
  const { message } = AntApp.useApp()
  const { user, refreshMe } = useAuth()
  const qc = useQueryClient()
  const [profileForm] = Form.useForm()
  const [passwordForm] = Form.useForm()
  const [activityPage, setActivityPage] = React.useState(1)

  useEffect(() => {
    if (user) {
      profileForm.setFieldsValue({
        first_name: user.first_name,
        last_name: user.last_name,
        phone: user.phone ?? '',
        telegram: user.telegram ?? '',
      })
    }
  }, [user, profileForm])

  const profileMut = useMutation({
    mutationFn: patchProfileRequest,
    onSuccess: async () => {
      message.success('Профиль сохранён')
      await refreshMe()
      await qc.invalidateQueries({ queryKey: ['auth', 'me'] })
    },
    onError: (e: Error) => message.error(e.message),
  })

  const avatarMut = useMutation({
    mutationFn: uploadAvatarRequest,
    onSuccess: async () => {
      message.success('Аватар обновлён')
      await refreshMe()
    },
    onError: (e: Error) => message.error(e.message),
  })

  const passwordMut = useMutation({
    mutationFn: (v: { current_password: string; new_password: string }) =>
      changePasswordRequest(v.current_password, v.new_password),
    onSuccess: async () => {
      message.success('Пароль изменён. Другие сессии завершены.')
      passwordForm.resetFields()
      void qc.invalidateQueries({ queryKey: ['sessions'] })
      await refreshMe()
    },
    onError: (e: Error) => message.error(e.message),
  })

  const { data: sessions, refetch: refetchSessions } = useQuery({
    queryKey: ['sessions'],
    queryFn: listSessionsRequest,
  })

  const revokeMut = useMutation({
    mutationFn: revokeSessionRequest,
    onSuccess: async () => {
      message.success('Сессия завершена')
      await refetchSessions()
    },
    onError: (e: Error) => message.error(e.message),
  })

  const { data: activityData, isLoading: activityLoading } = useQuery({
    queryKey: ['my-activity', activityPage],
    queryFn: () => getMyActivityPage(activityPage, 15),
  })

  const avatarSrc =
    user?.avatar_url && user.avatar_url.length > 0
      ? user.avatar_url.startsWith('http')
        ? user.avatar_url
        : user.avatar_url
      : undefined

  const sessionColumns: ColumnsType<SessionOut> = [
    {
      title: 'Создана',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (v: string) => formatDateTimeRu(v),
    },
    {
      title: 'До',
      dataIndex: 'expires_at',
      key: 'expires_at',
      width: 160,
      render: (v: string) => formatDateTimeRu(v),
    },
    {
      title: 'Клиент',
      dataIndex: 'user_agent',
      key: 'user_agent',
      ellipsis: true,
      render: (v: string | null) => v || '—',
    },
    {
      title: '',
      key: 'cur',
      width: 100,
      render: (_, r) => (r.is_current ? <Tag color="blue">Текущая</Tag> : null),
    },
    {
      title: '',
      key: 'act',
      width: 120,
      render: (_, r) =>
        r.is_current ? null : (
          <Button
            size="small"
            danger
            loading={revokeMut.isPending}
            onClick={() => void revokeMut.mutateAsync(r.id)}
          >
            Завершить
          </Button>
        ),
    },
  ]

  const activityColumns: ColumnsType<AuditLogOut> = [
    {
      title: 'Время',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 160,
      render: (v: string) => formatDateTimeRu(v),
    },
    { title: 'Действие', dataIndex: 'action_type', key: 'action_type', width: 140 },
    { title: 'Сущность', dataIndex: 'entity_type', key: 'entity_type', width: 140 },
    {
      title: 'Детали',
      key: 'after',
      ellipsis: true,
      render: (_, r) => (
        <Typography.Text type="secondary" style={{ fontSize: 12 }}>
          {r.payload_after ? JSON.stringify(r.payload_after).slice(0, 120) : '—'}
        </Typography.Text>
      ),
    },
  ]

  return (
    <AppLayout
      nav={
        <Space>
          <Link to="/dashboard" style={{ color: 'rgba(255,255,255,0.65)', fontSize: 13 }}>
            ← На дашборд
          </Link>
          <Typography.Text type="secondary" style={{ fontSize: 13 }}>
            Профиль
          </Typography.Text>
        </Space>
      }
    >
      <Typography.Title level={3} style={{ marginTop: 0 }}>
        {user ? userDisplayName(user) : 'Профиль'}
      </Typography.Title>

      <Tabs
        defaultActiveKey="info"
        items={[
          {
            key: 'info',
            label: (
              <span>
                <UserOutlined /> Контакты и аватар
              </span>
            ),
            children: (
              <Card style={{ borderColor: '#1f2a3a', background: '#0d1219', maxWidth: 560 }}>
                <Space align="start" size={24} wrap>
                  <Avatar size={96} src={avatarSrc} style={{ background: '#1f2a3a' }}>
                    {user ? (user.last_name || user.email).slice(0, 1).toUpperCase() : '?'}
                  </Avatar>
                  <div>
                    <Upload
                      accept="image/jpeg,image/png,image/webp"
                      showUploadList={false}
                      beforeUpload={(file) => {
                        void avatarMut.mutateAsync(file as File)
                        return false
                      }}
                    >
                      <Button loading={avatarMut.isPending}>Загрузить аватар</Button>
                    </Upload>
                    <Typography.Paragraph type="secondary" style={{ marginTop: 8, marginBottom: 0, fontSize: 12 }}>
                      JPEG, PNG или WebP, до 2 МБ.
                    </Typography.Paragraph>
                  </div>
                </Space>
                <Form
                  form={profileForm}
                  layout="vertical"
                  style={{ marginTop: 24 }}
                  onFinish={(v) => void profileMut.mutateAsync(v)}
                >
                  <Form.Item name="last_name" label="Фамилия" rules={[{ required: true, message: 'Обязательно' }]}>
                    <Input />
                  </Form.Item>
                  <Form.Item name="first_name" label="Имя" rules={[{ required: true, message: 'Обязательно' }]}>
                    <Input />
                  </Form.Item>
                  <Form.Item
                    name="phone"
                    label="Мобильный телефон (Россия)"
                    extra="Можно 7906… или 8906… — сохранится как +7 (906) …"
                    rules={[
                      {
                        validator: async (_, value: string) => {
                          const t = (value ?? '').trim()
                          if (!t) {
                            return Promise.resolve()
                          }
                          try {
                            normalizeRuMobilePhone(t)
                            return Promise.resolve()
                          } catch {
                            return Promise.reject(new Error('Некорректный российский мобильный номер'))
                          }
                        },
                      },
                    ]}
                  >
                    <Input placeholder="79060943936" autoComplete="tel" inputMode="tel" />
                  </Form.Item>
                  <Form.Item name="telegram" label="Telegram">
                    <Input placeholder="@username" />
                  </Form.Item>
                  <Button type="primary" htmlType="submit" loading={profileMut.isPending}>
                    Сохранить
                  </Button>
                </Form>
              </Card>
            ),
          },
          {
            key: 'security',
            label: (
              <span>
                <SafetyOutlined /> Пароль и сессии
              </span>
            ),
            children: (
              <Space direction="vertical" size={24} style={{ width: '100%' }}>
                <Card title="Смена пароля" style={{ borderColor: '#1f2a3a', background: '#0d1219', maxWidth: 480 }}>
                  <Form
                    form={passwordForm}
                    layout="vertical"
                    onFinish={(v: { current_password: string; new_password: string; new_password2: string }) => {
                      if (v.new_password !== v.new_password2) {
                        message.error('Новые пароли не совпадают')
                        return
                      }
                      void passwordMut.mutateAsync({
                        current_password: v.current_password,
                        new_password: v.new_password,
                      })
                    }}
                  >
                    <Form.Item
                      name="current_password"
                      label="Текущий пароль"
                      rules={[{ required: true, message: 'Обязательно' }]}
                    >
                      <Input.Password autoComplete="current-password" />
                    </Form.Item>
                    <Form.Item
                      name="new_password"
                      label="Новый пароль"
                      rules={[{ required: true }, { min: 8, message: 'Не короче 8 символов' }]}
                    >
                      <Input.Password autoComplete="new-password" />
                    </Form.Item>
                    <Form.Item
                      name="new_password2"
                      label="Повтор нового пароля"
                      rules={[{ required: true, message: 'Обязательно' }]}
                    >
                      <Input.Password autoComplete="new-password" />
                    </Form.Item>
                    <Button type="primary" htmlType="submit" loading={passwordMut.isPending}>
                      Сменить пароль
                    </Button>
                  </Form>
                </Card>
                <Card title="Активные сессии (по refresh-токену)" style={{ borderColor: '#1f2a3a', background: '#0d1219' }}>
                  <Table
                    rowKey="id"
                    size="small"
                    columns={sessionColumns}
                    dataSource={sessions ?? []}
                    pagination={false}
                    scroll={{ x: 720 }}
                  />
                </Card>
              </Space>
            ),
          },
          {
            key: 'activity',
            label: (
              <span>
                <HistoryOutlined /> История активности
              </span>
            ),
            children: (
              <Card style={{ borderColor: '#1f2a3a', background: '#0d1219' }}>
                <Table
                  rowKey="id"
                  loading={activityLoading}
                  columns={activityColumns}
                  dataSource={activityData?.items ?? []}
                  pagination={{
                    current: activityPage,
                    pageSize: activityData?.page_size ?? 15,
                    total: activityData?.total ?? 0,
                    onChange: (p) => setActivityPage(p),
                    showSizeChanger: false,
                  }}
                  scroll={{ x: 900 }}
                />
              </Card>
            ),
          },
        ]}
      />
    </AppLayout>
  )
}
