import { Card, DatePicker, Space, Table, Typography } from 'antd'
import type { ColumnsType } from 'antd/es/table'
import { useQuery } from '@tanstack/react-query'
import dayjs from 'dayjs'
import React, { useState } from 'react'
import { Link } from 'react-router-dom'

import { apiFetch } from '@/api/client'

export type OperatorStatsOverview = {
  stat_date: string
  week_start: string
  week_end: string
  month_start: string
  month_end: string
  assignments: {
    stream_event_id: string
    title: string
    summary: string
  }[]
  operators: {
    operator_id: string
    email: string
    display_name: string
    role: string
    broadcasts_week: number
    mentions_week: number
    mentions_norm_week: number
    mentions_met_week: boolean
    broadcasts_month: number
    mentions_month: number
    mentions_norm_month: number
    mentions_met_month: boolean
  }[]
  total_broadcasts_week: number
  total_mentions_week: number
  total_broadcasts_month: number
  total_mentions_month: number
}

const roleRu = (r: string) => {
  const m: Record<string, string> = {
    OPERATOR: 'Оператор',
    STREAM_MANAGER: 'Менеджер стримов',
    SUPERADMIN: 'Суперадмин',
  }
  return m[r] ?? r
}

const mentionCell = (v: number, met: boolean) => (
  <span
    style={{
      color: met ? '#52c41a' : '#ff7875',
      fontWeight: 600,
    }}
  >
    {v}
  </span>
)

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
      title: 'Эфиров за неделю',
      dataIndex: 'broadcasts_week',
      key: 'bw',
      width: 130,
      align: 'center',
    },
    {
      title: 'Упоминаний (нед.)',
      key: 'mw',
      width: 150,
      align: 'center',
      render: (_, r) => mentionCell(r.mentions_week, r.mentions_met_week),
    },
    {
      title: 'Эфиров за месяц',
      dataIndex: 'broadcasts_month',
      key: 'bm',
      width: 130,
      align: 'center',
    },
    {
      title: 'Упоминаний (мес.)',
      key: 'mm',
      width: 150,
      align: 'center',
      render: (_, r) => mentionCell(r.mentions_month, r.mentions_met_month),
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
      title: 'Операторы по дням',
      dataIndex: 'summary',
      key: 'summary',
      ellipsis: true,
    },
  ]

  return (
    <Space direction="vertical" size={16} style={{ width: '100%' }}>
      <Space wrap align="center">
        <Typography.Text type="secondary">Опорная дата (МСК, для границ недели и месяца):</Typography.Text>
        <DatePicker value={statDay} onChange={(d) => d && setStatDay(d)} format="DD.MM.YYYY" allowClear={false} />
      </Space>
      {data ? (
        <Space direction="vertical" size={12} style={{ width: '100%' }}>
          <Typography.Text type="secondary">
            Неделя {dayjs(data.week_start).format('DD.MM')} — {dayjs(data.week_end).format('DD.MM.YYYY')}: эфиров{' '}
            {data.total_broadcasts_week}, упоминаний {data.total_mentions_week}. Месяц{' '}
            {dayjs(data.month_start).format('MM.YYYY')}: эфиров {data.total_broadcasts_month}, упоминаний{' '}
            {data.total_mentions_month}. Норма упоминаний: 4 на каждый эфир — зелёный цвет, если выполнено.
          </Typography.Text>
          <Card
            size={compact ? 'small' : 'default'}
            title="Кто на каких событиях (по дням)"
            style={{ borderColor: '#1f2a3a', background: '#0d1219' }}
          >
            <Table
              rowKey="stream_event_id"
              size="small"
              loading={statsQuery.isLoading}
              dataSource={data.assignments}
              columns={assignColumns}
              pagination={false}
              locale={{ emptyText: 'Нет назначений по дням' }}
            />
          </Card>
          <Card
            size={compact ? 'small' : 'default'}
            title="Операторы: эфиры и упоминания (неделя и месяц)"
            style={{ borderColor: '#1f2a3a', background: '#0d1219' }}
          >
            <Table
              rowKey="operator_id"
              size="small"
              dataSource={data.operators}
              columns={opColumns}
              pagination={false}
              locale={{ emptyText: 'Нет операторов' }}
              scroll={{ x: 900 }}
            />
          </Card>
        </Space>
      ) : (
        <Typography.Text type="secondary">{statsQuery.isLoading ? 'Загрузка…' : 'Нет данных'}</Typography.Text>
      )}
    </Space>
  )
}
