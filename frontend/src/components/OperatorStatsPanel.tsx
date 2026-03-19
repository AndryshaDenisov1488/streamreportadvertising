import { Card, DatePicker, Space, Table, Typography } from 'antd'
import type { ColumnsType } from 'antd/es/table'
import { useQuery } from '@tanstack/react-query'
import dayjs from 'dayjs'
import React, { useState } from 'react'
import { Link } from 'react-router-dom'

import { apiFetch } from '@/api/client'

export type OperatorStatsOverview = {
  stat_date: string
  assignments: {
    stream_event_id: string
    title: string
    locked_by_user_id: string
    locked_by_email: string
    locked_by_display_name: string
  }[]
  operators: {
    operator_id: string
    email: string
    display_name: string
    role: string
    broadcasts_count: number
    mentions_count: number
  }[]
  total_broadcasts_day: number
  total_mentions_day: number
}

const roleRu = (r: string) => {
  const m: Record<string, string> = {
    OPERATOR: 'Оператор',
    STREAM_MANAGER: 'Менеджер стримов',
    SUPERADMIN: 'Суперадмин',
  }
  return m[r] ?? r
}

export const OperatorStatsPanel: React.FC<{ compact?: boolean }> = ({ compact }) => {
  const [statDay, setStatDay] = useState(() => dayjs())

  const statsQuery = useQuery({
    queryKey: ['stats-operators', statDay.format('YYYY-MM-DD')],
    queryFn: async () =>
      (await apiFetch(`/stats/operators?stat_date=${statDay.format('YYYY-MM-DD')}`)) as OperatorStatsOverview,
  })

  const data = statsQuery.data

  const opColumns: ColumnsType<OperatorStatsOverview['operators'][0]> = [
    {
      title: 'Оператор',
      key: 'op',
      ellipsis: true,
      render: (_, r) => (
        <div>
          <div>{r.display_name || r.email}</div>
          <Typography.Text type="secondary" style={{ fontSize: 12 }}>
            {r.email}
          </Typography.Text>
        </div>
      ),
    },
    {
      title: 'Роль',
      dataIndex: 'role',
      key: 'role',
      width: 140,
      render: (r: string) => roleRu(r),
    },
    {
      title: 'Эфиров за день',
      dataIndex: 'broadcasts_count',
      key: 'bc',
      width: 130,
      align: 'center',
    },
    {
      title: 'Упоминаний за день',
      dataIndex: 'mentions_count',
      key: 'mc',
      width: 150,
      align: 'center',
    },
  ]

  const assignColumns: ColumnsType<OperatorStatsOverview['assignments'][0]> = [
    {
      title: 'Событие',
      dataIndex: 'title',
      key: 'title',
      ellipsis: true,
      render: (t: string, r) => (
        <Link to={`/manager/${r.stream_event_id}`} style={{ color: '#69b1ff' }}>
          {t}
        </Link>
      ),
    },
    {
      title: 'Кто в работе',
      key: 'who',
      ellipsis: true,
      render: (_, r) => (
        <div>
          <div>{r.locked_by_display_name || r.locked_by_email}</div>
          <Typography.Text type="secondary" style={{ fontSize: 12 }}>
            {r.locked_by_email}
          </Typography.Text>
        </div>
      ),
    },
  ]

  return (
    <Space direction="vertical" size={16} style={{ width: '100%' }}>
      <Space wrap align="center">
        <Typography.Text type="secondary">День статистики (МСК):</Typography.Text>
        <DatePicker
          value={statDay}
          onChange={(d) => d && setStatDay(d)}
          format="DD.MM.YYYY"
          allowClear={false}
        />
      </Space>
      {data ? (
        <Space direction="vertical" size={12} style={{ width: '100%' }}>
          <Typography.Text type="secondary">
            За {dayjs(data.stat_date).format('DD.MM.YYYY')}: эфиров {data.total_broadcasts_day}, упоминаний{' '}
            {data.total_mentions_day}
          </Typography.Text>
          <Card
            size={compact ? 'small' : 'default'}
            title="Кто на каких событиях сейчас"
            style={{ borderColor: '#1f2a3a', background: '#0d1219' }}
          >
            <Table
              rowKey="stream_event_id"
              size="small"
              loading={statsQuery.isLoading}
              dataSource={data.assignments}
              columns={assignColumns}
              pagination={false}
              locale={{ emptyText: 'Никто не взял события в работу' }}
            />
          </Card>
          <Card
            size={compact ? 'small' : 'default'}
            title="Операторы: эфиры и упоминания за день"
            style={{ borderColor: '#1f2a3a', background: '#0d1219' }}
          >
            <Table
              rowKey="operator_id"
              size="small"
              dataSource={data.operators}
              columns={opColumns}
              pagination={false}
              locale={{ emptyText: 'Нет данных за этот день' }}
              scroll={{ x: 480 }}
            />
          </Card>
        </Space>
      ) : (
        <Typography.Text type="secondary">{statsQuery.isLoading ? 'Загрузка…' : 'Нет данных'}</Typography.Text>
      )}
    </Space>
  )
}
