import { BarChartOutlined, DeleteOutlined, DownloadOutlined, PlusOutlined } from '@ant-design/icons'
import {
  App as AntApp,
  Button,
  Card,
  Form,
  Grid,
  Input,
  Modal,
  Select,
  Space,
  Switch,
  Table,
  Tabs,
  Typography,
} from 'antd'
import type { ColumnsType } from 'antd/es/table'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import React, { useEffect, useState } from 'react'

import type { AuditLogOut, UserCreatedOut, UserOut } from '@/api/types'
import { apiFetch, getAccessToken } from '@/api/client'
import { OperatorStatsPanel } from '@/components/OperatorStatsPanel'
import { AppLayout } from '@/layouts/AppLayout'
import { auditActionLabel, auditEntityLabel, formatAuditPayloadRu } from '@/utils/auditLabels'
import { formatDateTimeRu } from '@/utils/datetime'
import { userDisplayName } from '@/utils/userDisplay'

type AuditPage = {
  items: AuditLogOut[]
  total: number
  page: number
  page_size: number
}

type AnalyticsSummary = {
  by_event: { event_name: string; count: number }[]
}

const API_BASE = import.meta.env.VITE_API_BASE ?? '/api/v1'

export const SuperadminPage: React.FC = () => {
  const { message, modal } = AntApp.useApp()
  const qc = useQueryClient()
  const screens = Grid.useBreakpoint()
  const isNarrow = !screens.md
  const [userOpen, setUserOpen] = useState(false)
  const [editUser, setEditUser] = useState<UserOut | null>(null)
  const [createForm] = Form.useForm()
  const [editForm] = Form.useForm()
  const [auditPage, setAuditPage] = useState(1)

  const usersQuery = useQuery({
    queryKey: ['users'],
    queryFn: async () => (await apiFetch('/users')) as UserOut[],
  })

  const auditQuery = useQuery({
    queryKey: ['audit', auditPage],
    queryFn: async () =>
      (await apiFetch(`/audit-logs?page=${auditPage}&page_size=25`)) as AuditPage,
  })

  const analyticsQuery = useQuery({
    queryKey: ['analytics-summary'],
    queryFn: async () => (await apiFetch('/analytics/summary')) as AnalyticsSummary,
  })

  const handleExportAuditCsv = async () => {
    const token = getAccessToken()
    const res = await fetch(`${API_BASE}/audit-logs/export.csv`, {
      credentials: 'include',
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    })
    if (!res.ok) {
      message.error('Не удалось выгрузить CSV')
      return
    }
    const blob = await res.blob()
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'audit_export.csv'
    a.click()
    URL.revokeObjectURL(url)
    message.success('Файл скачан')
  }

  useEffect(() => {
    if (!editUser) {
      return
    }
    editForm.setFieldsValue({
      email: editUser.email,
      last_name: editUser.last_name,
      first_name: editUser.first_name,
      role: editUser.role,
      is_active: editUser.is_active,
      password: '',
    })
  }, [editUser, editForm])

  const createMut = useMutation({
    mutationFn: async (values: {
      email: string
      last_name: string
      first_name: string
      role: string
      is_active: boolean
    }) => {
      const body = {
        email: values.email,
        last_name: values.last_name,
        first_name: values.first_name,
        role: values.role,
        is_active: values.is_active,
      }
      return (await apiFetch('/users', {
        method: 'POST',
        body: JSON.stringify(body),
      })) as UserCreatedOut
    },
    onSuccess: async (data) => {
      if (data.welcome_email_queued) {
        message.success('Пользователь создан. Приветственное письмо отправляется на email — подождите 1–2 минуты')
      } else if (data.welcome_email_skipped_reason) {
        message.warning(
          `Пользователь создан. ${data.welcome_email_skipped_reason}`,
          10,
        )
      } else {
        message.success('Пользователь создан')
      }
      setUserOpen(false)
      createForm.resetFields()
      await qc.invalidateQueries({ queryKey: ['users'] })
    },
    onError: (e: Error) => message.error(e.message),
  })

  const updateMut = useMutation({
    mutationFn: async (payload: { id: string; values: Record<string, unknown> }) => {
      await apiFetch(`/users/${payload.id}`, {
        method: 'PATCH',
        body: JSON.stringify(payload.values),
      })
    },
    onSuccess: async () => {
      message.success('Сохранено')
      setEditUser(null)
      await qc.invalidateQueries({ queryKey: ['users'] })
    },
    onError: (e: Error) => message.error(e.message),
  })

  const deleteMut = useMutation({
    mutationFn: async (id: string) => {
      await apiFetch(`/users/${id}`, { method: 'DELETE' })
    },
    onSuccess: async () => {
      message.success('Удалено')
      await qc.invalidateQueries({ queryKey: ['users'] })
    },
    onError: (e: Error) => message.error(e.message),
  })

  const userColumns: ColumnsType<UserOut> = [
    {
      title: 'Фамилия и имя',
      key: 'display_name',
      width: 200,
      ellipsis: true,
      render: (_, u) => userDisplayName(u),
    },
    { title: 'Email', dataIndex: 'email', key: 'email', ellipsis: true },
    {
      title: 'Роль',
      dataIndex: 'role',
      key: 'role',
      width: 160,
      render: (r: string) =>
        ({ OPERATOR: 'Оператор', STREAM_MANAGER: 'Менеджер', SUPERADMIN: 'Суперадмин' } as Record<
          string,
          string
        >)[r] ?? r,
    },
    {
      title: 'Активен',
      dataIndex: 'is_active',
      key: 'is_active',
      width: 100,
      render: (v: boolean) => (v ? 'да' : 'нет'),
    },
    {
      title: 'Последний вход',
      dataIndex: 'last_login_at',
      key: 'last_login_at',
      width: 170,
      ellipsis: true,
      render: (v: string | undefined) => (v ? formatDateTimeRu(v) : '—'),
    },
    {
      title: 'IP при входе',
      dataIndex: 'last_login_ip',
      key: 'last_login_ip',
      width: 140,
      ellipsis: true,
      render: (v: string | null | undefined) => v || '—',
    },
    {
      title: '',
      key: 'actions',
      width: 200,
      render: (_, u) => (
        <Space>
          <Button type="link" onClick={() => setEditUser(u)}>
            Изменить
          </Button>
          <Button
            type="link"
            danger
            icon={<DeleteOutlined />}
            onClick={() => {
              modal.confirm({
                title: 'Удалить пользователя?',
                okText: 'Удалить',
                cancelText: 'Отмена',
                okButtonProps: { danger: true },
                onOk: async () => {
                  await deleteMut.mutateAsync(u.id)
                },
              })
            }}
          >
            Удалить
          </Button>
        </Space>
      ),
    },
  ]

  const auditColumns: ColumnsType<AuditLogOut> = [
    {
      title: 'Время',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 160,
      render: (v: string) => formatDateTimeRu(v),
    },
    {
      title: 'Действие',
      dataIndex: 'action_type',
      key: 'action_type',
      width: 200,
      render: (v: string) => auditActionLabel(v),
    },
    {
      title: 'Сущность',
      dataIndex: 'entity_type',
      key: 'entity_type',
      width: 160,
      render: (v: string) => auditEntityLabel(v),
    },
    { title: 'ID', dataIndex: 'entity_id', key: 'entity_id', ellipsis: true },
    {
      title: 'Детали',
      key: 'details',
      width: 320,
      render: (_, r) => {
        const text = formatAuditPayloadRu({
          ...(r.payload_before != null ? { было: r.payload_before as Record<string, unknown> } : {}),
          ...(r.payload_after != null ? { стало: r.payload_after as Record<string, unknown> } : {}),
        })
        return (
          <Typography.Paragraph type="secondary" style={{ fontSize: 12, marginBottom: 0, maxWidth: 400 }}>
            {text || '—'}
          </Typography.Paragraph>
        )
      },
    },
  ]

  return (
    <AppLayout
      nav={
        <Typography.Text type="secondary" style={{ fontSize: 13 }}>
          Суперадмин
        </Typography.Text>
      }
    >
      <Typography.Title level={3} style={{ marginTop: 0 }}>
        Администрирование
      </Typography.Title>

      <Tabs
        items={[
          {
            key: 'users',
            label: 'Пользователи',
            children: (
              <Card
                style={{ borderColor: '#e2e8f0', background: '#ffffff' }}
                extra={
                  <Button
                    type="primary"
                    icon={<PlusOutlined />}
                    onClick={() => setUserOpen(true)}
                    size="large"
                    block={isNarrow}
                  >
                    Новый пользователь
                  </Button>
                }
              >
                <Table
                  rowKey="id"
                  loading={usersQuery.isLoading}
                  dataSource={usersQuery.data ?? []}
                  columns={userColumns}
                  scroll={{ x: 1100 }}
                  size={isNarrow ? 'small' : 'middle'}
                />
              </Card>
            ),
          },
          {
            key: 'stats',
            label: 'Статистика',
            children: (
              <Card style={{ borderColor: '#e2e8f0', background: '#ffffff' }}>
                <Typography.Paragraph type="secondary">
                  Назначения операторов на мероприятия, число эфиров и упоминаний за выбранный календарный день (МСК).
                  Карточки мероприятий открываются как у менеджера.
                </Typography.Paragraph>
                <OperatorStatsPanel />
              </Card>
            ),
          },
          {
            key: 'analytics',
            label: (
              <span>
                <BarChartOutlined /> Продукт
              </span>
            ),
            children: (
              <Card style={{ borderColor: '#e2e8f0', background: '#ffffff' }}>
                <Typography.Paragraph type="secondary">
                  Данные аналитики за 7 дней (page_view и др.), накопленные через{' '}
                  <Typography.Text code>/analytics/events</Typography.Text>.
                </Typography.Paragraph>
                <Table
                  rowKey="event_name"
                  loading={analyticsQuery.isLoading}
                  dataSource={analyticsQuery.data?.by_event ?? []}
                  pagination={false}
                  size="small"
                  columns={[
                    { title: 'Ключ', dataIndex: 'event_name', key: 'e' },
                    { title: 'Раз', dataIndex: 'count', key: 'c', width: 100 },
                  ]}
                />
              </Card>
            ),
          },
          {
            key: 'audit',
            label: 'Аудит',
            children: (
              <Card
                style={{ borderColor: '#e2e8f0', background: '#ffffff' }}
                extra={
                  <Button icon={<DownloadOutlined />} onClick={() => void handleExportAuditCsv()}>
                    Выгрузить CSV
                  </Button>
                }
              >
                <Table
                  rowKey="id"
                  loading={auditQuery.isLoading}
                  dataSource={auditQuery.data?.items ?? []}
                  columns={auditColumns}
                  scroll={{ x: 900 }}
                  size={isNarrow ? 'small' : 'middle'}
                  pagination={{
                    current: auditPage,
                    pageSize: 25,
                    total: auditQuery.data?.total ?? 0,
                    onChange: (p) => setAuditPage(p),
                    size: isNarrow ? 'small' : 'default',
                    showSizeChanger: false,
                  }}
                />
              </Card>
            ),
          },
        ]}
      />

      <Modal
        title="Новый пользователь"
        open={userOpen}
        okText="Создать"
        cancelText="Отмена"
        confirmLoading={createMut.isPending}
        onCancel={() => setUserOpen(false)}
        onOk={async () => {
          const v = await createForm.validateFields()
          await createMut.mutateAsync({
            email: v.email,
            last_name: v.last_name,
            first_name: v.first_name,
            role: v.role,
            is_active: v.is_active ?? true,
          })
        }}
      >
        <Form form={createForm} layout="vertical" initialValues={{ is_active: true, role: 'OPERATOR' }}>
          <Form.Item name="email" label="Email" rules={[{ required: true, type: 'email' }]}>
            <Input />
          </Form.Item>
          <Form.Item name="last_name" label="Фамилия" rules={[{ required: true, whitespace: true }]}>
            <Input autoComplete="family-name" />
          </Form.Item>
          <Form.Item name="first_name" label="Имя" rules={[{ required: true, whitespace: true }]}>
            <Input autoComplete="given-name" />
          </Form.Item>
          <Typography.Paragraph type="secondary" style={{ marginBottom: 0 }}>
            Пароль генерируется автоматически и отправляется на email (если на сервере настроен SMTP).
          </Typography.Paragraph>
          <Form.Item name="role" label="Роль" rules={[{ required: true }]}>
            <Select
              options={[
                { label: 'SUPERADMIN', value: 'SUPERADMIN' },
                { label: 'STREAM_MANAGER', value: 'STREAM_MANAGER' },
                { label: 'OPERATOR', value: 'OPERATOR' },
              ]}
            />
          </Form.Item>
          <Form.Item name="is_active" label="Активен" valuePropName="checked">
            <Switch />
          </Form.Item>
        </Form>
      </Modal>

      <Modal
        title="Изменить пользователя"
        open={Boolean(editUser)}
        okText="Сохранить"
        cancelText="Отмена"
        confirmLoading={updateMut.isPending}
        onCancel={() => setEditUser(null)}
        onOk={async () => {
          if (!editUser) {
            return
          }
          const v = await editForm.validateFields()
          const payload: Record<string, unknown> = {
            email: v.email,
            last_name: v.last_name,
            first_name: v.first_name,
            role: v.role,
            is_active: v.is_active,
          }
          if (v.password) {
            payload.password = v.password
          }
          await updateMut.mutateAsync({ id: editUser.id, values: payload })
        }}
      >
        <Form form={editForm} layout="vertical">
          <Form.Item name="email" label="Email" rules={[{ required: true, type: 'email' }]}>
            <Input />
          </Form.Item>
          <Form.Item name="last_name" label="Фамилия" rules={[{ required: true, whitespace: true }]}>
            <Input autoComplete="family-name" />
          </Form.Item>
          <Form.Item name="first_name" label="Имя" rules={[{ required: true, whitespace: true }]}>
            <Input autoComplete="given-name" />
          </Form.Item>
          <Form.Item
            name="password"
            label="Новый пароль (необязательно)"
            rules={[
              {
                validator: async (_, v: string) => {
                  if (!v || v.length >= 8) {
                    return
                  }
                  throw new Error('Минимум 8 символов')
                },
              },
            ]}
          >
            <Input.Password />
          </Form.Item>
          <Form.Item name="role" label="Роль" rules={[{ required: true }]}>
            <Select
              options={[
                { label: 'SUPERADMIN', value: 'SUPERADMIN' },
                { label: 'STREAM_MANAGER', value: 'STREAM_MANAGER' },
                { label: 'OPERATOR', value: 'OPERATOR' },
              ]}
            />
          </Form.Item>
          <Form.Item name="is_active" label="Активен" valuePropName="checked">
            <Switch />
          </Form.Item>
        </Form>
      </Modal>
    </AppLayout>
  )
}
