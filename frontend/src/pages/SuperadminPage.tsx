import { DeleteOutlined, PlusOutlined } from '@ant-design/icons'
import {
  App as AntApp,
  Button,
  Card,
  Form,
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

import type { AuditLogOut, UserOut } from '@/api/types'
import { apiFetch } from '@/api/client'
import { AppLayout } from '@/layouts/AppLayout'

type AuditPage = {
  items: AuditLogOut[]
  total: number
  page: number
  page_size: number
}

export const SuperadminPage: React.FC = () => {
  const { message, modal } = AntApp.useApp()
  const qc = useQueryClient()
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

  useEffect(() => {
    if (!editUser) {
      return
    }
    editForm.setFieldsValue({
      email: editUser.email,
      role: editUser.role,
      is_active: editUser.is_active,
      password: '',
    })
  }, [editUser, editForm])

  const createMut = useMutation({
    mutationFn: async (values: { email: string; password: string; role: string; is_active: boolean }) => {
      await apiFetch('/users', {
        method: 'POST',
        body: JSON.stringify(values),
      })
    },
    onSuccess: async () => {
      message.success('Пользователь создан')
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
    { title: 'Email', dataIndex: 'email', key: 'email' },
    { title: 'Роль', dataIndex: 'role', key: 'role', width: 160 },
    {
      title: 'Активен',
      dataIndex: 'is_active',
      key: 'is_active',
      width: 100,
      render: (v: boolean) => (v ? 'да' : 'нет'),
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
    { title: 'Время', dataIndex: 'created_at', key: 'created_at', width: 200 },
    { title: 'Действие', dataIndex: 'action_type', key: 'action_type', width: 160 },
    { title: 'Сущность', dataIndex: 'entity_type', key: 'entity_type', width: 140 },
    { title: 'ID', dataIndex: 'entity_id', key: 'entity_id', ellipsis: true },
    {
      title: 'Детали',
      key: 'details',
      render: (_, r) => (
        <Typography.Text type="secondary" style={{ fontSize: 12 }}>
          {JSON.stringify({ before: r.payload_before, after: r.payload_after }).slice(0, 180)}
          …
        </Typography.Text>
      ),
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
                style={{ borderColor: '#1f2a3a', background: '#0d1219' }}
                extra={
                  <Button type="primary" icon={<PlusOutlined />} onClick={() => setUserOpen(true)}>
                    Новый пользователь
                  </Button>
                }
              >
                <Table rowKey="id" loading={usersQuery.isLoading} dataSource={usersQuery.data ?? []} columns={userColumns} />
              </Card>
            ),
          },
          {
            key: 'audit',
            label: 'Аудит',
            children: (
              <Card style={{ borderColor: '#1f2a3a', background: '#0d1219' }}>
                <Table
                  rowKey="id"
                  loading={auditQuery.isLoading}
                  dataSource={auditQuery.data?.items ?? []}
                  columns={auditColumns}
                  pagination={{
                    current: auditPage,
                    pageSize: 25,
                    total: auditQuery.data?.total ?? 0,
                    onChange: (p) => setAuditPage(p),
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
            password: v.password,
            role: v.role,
            is_active: v.is_active ?? true,
          })
        }}
      >
        <Form form={createForm} layout="vertical" initialValues={{ is_active: true, role: 'OPERATOR' }}>
          <Form.Item name="email" label="Email" rules={[{ required: true, type: 'email' }]}>
            <Input />
          </Form.Item>
          <Form.Item name="password" label="Пароль" rules={[{ required: true, min: 8 }]}>
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
