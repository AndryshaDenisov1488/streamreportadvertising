import { ArrowLeftOutlined, SaveOutlined } from '@ant-design/icons'
import {
  App as AntApp,
  Badge,
  Button,
  Card,
  Col,
  DatePicker,
  Form,
  Grid,
  Input,
  List,
  Row,
  Select,
  Space,
  Typography,
} from 'antd'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import dayjs from 'dayjs'
import React, { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import type { SponsorMentionOut, StreamEventDetailOut } from '@/api/types'
import { apiFetch } from '@/api/client'
import { useStreamWs } from '@/hooks/useStreamWs'
import { AppLayout } from '@/layouts/AppLayout'
import { formatDateTimeRu } from '@/utils/datetime'

const formatElapsed = (totalSec: number) => {
  const sec = Math.max(0, Math.floor(totalSec))
  const h = Math.floor(sec / 3600)
  const m = Math.floor((sec % 3600) / 60)
  const s = sec % 60
  return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
}

export const ManagerStreamPage: React.FC = () => {
  const { id } = useParams()
  const streamId = id as string
  const screens = Grid.useBreakpoint()
  const isNarrow = !screens.sm
  const { message } = AntApp.useApp()
  const qc = useQueryClient()
  const [form] = Form.useForm()
  const [mentionDay, setMentionDay] = useState(1)

  const { data, isLoading } = useQuery({
    queryKey: ['stream', streamId],
    enabled: Boolean(streamId),
    queryFn: async () => (await apiFetch(`/stream-events/${streamId}`)) as StreamEventDetailOut,
  })

  useEffect(() => {
    if (!data) {
      return
    }
    const daysVals: Record<string, string> = {}
    for (const d of data.days) {
      daysVals[`day_${d.day_index}_stream_url`] = d.stream_url
      daysVals[`day_${d.day_index}_server_url`] = d.server_url
      daysVals[`day_${d.day_index}_stream_key`] = d.stream_key
    }
    form.setFieldsValue({
      title: data.title,
      start_date: dayjs(data.start_date),
      duration_days: data.duration_days,
      ...daysVals,
    })
  }, [data, form])

  useEffect(() => {
    if (!data) {
      return
    }
    if (mentionDay > data.duration_days) {
      setMentionDay(1)
    }
  }, [data, mentionDay])

  const mentionsQuery = useQuery({
    queryKey: ['mentions', streamId, mentionDay],
    enabled: Boolean(streamId) && Boolean(data),
    queryFn: async () =>
      (await apiFetch(`/stream-events/${streamId}/days/${mentionDay}/mentions`)) as SponsorMentionOut[],
  })

  useStreamWs(streamId, () => {
    void qc.invalidateQueries({ queryKey: ['mentions', streamId] })
    void qc.invalidateQueries({ queryKey: ['stream', streamId] })
  })

  const saveMut = useMutation({
    mutationFn: async (values: Record<string, unknown>) => {
      const duration = Number(values.duration_days)
      const days = Array.from({ length: duration }, (_, i) => {
        const idx = i + 1
        return {
          day_index: idx,
          stream_url: String(values[`day_${idx}_stream_url`] ?? ''),
          server_url: String(values[`day_${idx}_server_url`] ?? ''),
          stream_key: String(values[`day_${idx}_stream_key`] ?? ''),
        }
      })
      await apiFetch(`/stream-events/${streamId}`, {
        method: 'PATCH',
        body: JSON.stringify({
          title: values.title,
          start_date: (values.start_date as dayjs.Dayjs).format('YYYY-MM-DD'),
          duration_days: duration,
          days,
        }),
      })
    },
    onSuccess: async () => {
      message.success('Сохранено')
      await qc.invalidateQueries({ queryKey: ['stream', streamId] })
      await qc.invalidateQueries({ queryKey: ['streams'] })
    },
    onError: (e: Error) => message.error(e.message),
  })

  return (
    <AppLayout
      nav={
        <Space>
          <Link to="/manager">
            <Button type="link" icon={<ArrowLeftOutlined />}>
              Назад
            </Button>
          </Link>
          <Typography.Text type="secondary">Карточка события</Typography.Text>
        </Space>
      }
    >
      <Typography.Title level={3} style={{ marginTop: 0 }}>
        Редактирование
      </Typography.Title>

      <Card
        title="Упоминания оператора"
        style={{ marginBottom: 16, borderColor: '#1f2a3a', background: '#0d1219' }}
        styles={{ header: { borderBottom: '1px solid #1f2a3a' } }}
      >
        <Typography.Paragraph type="secondary" style={{ marginBottom: 12 }}>
          То же, что видит оператор в пульте: отметки по ходу эфира. Список обновляется при появлении новых записей
          (WebSocket).
        </Typography.Paragraph>
        {data ? (
          <>
            <Typography.Text type="secondary">День эфира</Typography.Text>
            <Select
              style={{ width: '100%', maxWidth: 360, marginTop: 8, marginBottom: 16, display: 'block' }}
              value={mentionDay}
              options={data.days.map((d) => ({ label: `День ${d.day_index}`, value: d.day_index }))}
              onChange={(v) => setMentionDay(v)}
            />
            <List
              loading={mentionsQuery.isLoading}
              dataSource={mentionsQuery.data ?? []}
              locale={{ emptyText: 'Пока нет упоминаний за этот день' }}
              renderItem={(item) => (
                <List.Item>
                  <List.Item.Meta
                    title={
                      <Space wrap>
                        <Typography.Text strong>{item.adjusted_timecode}</Typography.Text>
                        {item.is_adjusted ? <Badge status="warning" text="Скорректировано" /> : null}
                      </Space>
                    }
                    description={
                      <Space direction="vertical" size={4}>
                        <Typography.Text type="secondary">
                          Время: {item.absolute_moscow_adjusted}
                        </Typography.Text>
                        <Typography.Text type="secondary" style={{ fontSize: 12 }}>
                          Таймкод трансляции: {item.original_timecode}
                        </Typography.Text>
                        {item.adjustments && item.adjustments.length > 0 ? (
                          <div style={{ marginTop: 8 }}>
                            <Typography.Text
                              type="secondary"
                              style={{ fontSize: 12, display: 'block', marginBottom: 4 }}
                            >
                              Лог
                            </Typography.Text>
                            {item.adjustments.map((a) => (
                              <Typography.Text
                                key={a.id}
                                type="secondary"
                                style={{ fontSize: 12, display: 'block' }}
                              >
                                Запись: {formatDateTimeRu(a.created_at)} · {formatElapsed(a.previous_adjusted_sec)} →{' '}
                                {formatElapsed(a.new_adjusted_sec)}
                              </Typography.Text>
                            ))}
                          </div>
                        ) : null}
                      </Space>
                    }
                  />
                </List.Item>
              )}
            />
          </>
        ) : (
          <Typography.Text type="secondary">Загрузка события…</Typography.Text>
        )}
      </Card>

      <Card loading={isLoading} style={{ borderColor: '#1f2a3a', background: '#0d1219' }}>
        <Form
          layout="vertical"
          form={form}
          onFinish={async (v) => {
            await saveMut.mutateAsync(v)
          }}
        >
          <Form.Item name="title" label="Название" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Row gutter={[16, 16]}>
            <Col xs={24} sm={12}>
              <Form.Item name="start_date" label="Дата старта" rules={[{ required: true }]}>
                <DatePicker format="DD.MM.YYYY" style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col xs={24} sm={12}>
              <Form.Item name="duration_days" label="Дней" rules={[{ required: true }]}>
                <Select
                  style={{ width: '100%', minWidth: isNarrow ? undefined : 160 }}
                  options={[
                    { label: '1', value: 1 },
                    { label: '2', value: 2 },
                    { label: '3', value: 3 },
                    { label: '4', value: 4 },
                    { label: '5', value: 5 },
                  ]}
                />
              </Form.Item>
            </Col>
          </Row>

          <Typography.Title level={5}>Дни (URL и ключи)</Typography.Title>
          <Form.Item shouldUpdate noStyle>
            {() => {
              const n = Number(form.getFieldValue('duration_days') ?? data?.duration_days ?? 1)
              return Array.from({ length: n }, (_, i) => {
                const idx = i + 1
                return (
                  <Card
                    key={idx}
                    size="small"
                    title={`День ${idx}`}
                    style={{ marginBottom: 12, borderColor: '#1f2a3a', background: '#0a1018' }}
                  >
                    <Form.Item name={`day_${idx}_stream_url`} label="Ссылка на трансляцию">
                      <Input />
                    </Form.Item>
                    <Form.Item name={`day_${idx}_server_url`} label="URL сервера трансляции">
                      <Input />
                    </Form.Item>
                    <Form.Item name={`day_${idx}_stream_key`} label="Ключ трансляции">
                      <Input />
                    </Form.Item>
                  </Card>
                )
              })
            }}
          </Form.Item>

          <Button
            type="primary"
            htmlType="submit"
            icon={<SaveOutlined />}
            loading={saveMut.isPending}
            size="large"
            block={isNarrow}
          >
            Сохранить
          </Button>
        </Form>
      </Card>
    </AppLayout>
  )
}
