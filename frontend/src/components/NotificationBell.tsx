import { BellOutlined } from '@ant-design/icons'
import { Badge, Button, Dropdown, List, Space, Typography } from 'antd'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import React from 'react'

import { apiFetch } from '@/api/client'
import { formatDateTimeRu } from '@/utils/datetime'

type NotificationItem = {
  id: string
  title: string
  body: string
  kind: string | null
  is_read: boolean
  created_at: string
}

type NotificationResponse = {
  items: NotificationItem[]
  unread_count: number
}

export const NotificationBell: React.FC = () => {
  const qc = useQueryClient()
  const q = useQuery({
    queryKey: ['notifications'],
    queryFn: async () => (await apiFetch('/notifications')) as NotificationResponse,
    refetchInterval: 60_000,
  })

  const markRead = useMutation({
    mutationFn: async (id: string) => {
      await apiFetch(`/notifications/${id}/read`, { method: 'POST', body: '{}' })
    },
    onSuccess: async () => {
      await qc.invalidateQueries({ queryKey: ['notifications'] })
    },
  })

  const markAll = useMutation({
    mutationFn: async () => {
      await apiFetch('/notifications/read-all', { method: 'POST', body: '{}' })
    },
    onSuccess: async () => {
      await qc.invalidateQueries({ queryKey: ['notifications'] })
    },
  })

  const unread = q.data?.unread_count ?? 0
  const items = q.data?.items ?? []

  const dropdownContent = (
    <div style={{ width: 320, maxHeight: 360, overflow: 'auto', background: '#0d1219', padding: 8 }}>
      <Space style={{ width: '100%', justifyContent: 'space-between', marginBottom: 8 }}>
        <Typography.Text strong style={{ color: 'rgba(255,255,255,0.88)' }}>
          Уведомления
        </Typography.Text>
        {unread > 0 ? (
          <Typography.Link onClick={() => void markAll.mutate()} style={{ fontSize: 12 }}>
            Прочитать все
          </Typography.Link>
        ) : null}
      </Space>
      <List
        size="small"
        dataSource={items}
        locale={{ emptyText: 'Пока пусто' }}
        renderItem={(n) => (
          <List.Item
            style={{
              opacity: n.is_read ? 0.65 : 1,
              cursor: n.is_read ? 'default' : 'pointer',
            }}
            onClick={() => {
              if (!n.is_read) {
                void markRead.mutate(n.id)
              }
            }}
          >
            <div style={{ width: '100%' }}>
              <Typography.Text strong style={{ fontSize: 13, color: 'rgba(255,255,255,0.92)' }}>
                {n.title}
              </Typography.Text>
              <div>
                <Typography.Text type="secondary" style={{ fontSize: 12 }}>
                  {n.body}
                </Typography.Text>
              </div>
              <Typography.Text type="secondary" style={{ fontSize: 11 }}>
                {formatDateTimeRu(n.created_at)}
              </Typography.Text>
            </div>
          </List.Item>
        )}
      />
    </div>
  )

  return (
    <Dropdown dropdownRender={() => dropdownContent} trigger={['click']} placement="bottomRight">
      <Badge count={unread} size="small" offset={[-2, 2]}>
        <Button type="text" icon={<BellOutlined />} aria-label="Уведомления" style={{ color: 'rgba(255,255,255,0.75)' }} />
      </Badge>
    </Dropdown>
  )
}
