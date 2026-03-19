import { ArrowLeftOutlined, SaveOutlined } from '@ant-design/icons'
import { App as AntApp, Button, Card, DatePicker, Form, Input, Select, Space, Typography } from 'antd'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import dayjs from 'dayjs'
import React, { useEffect } from 'react'
import { Link, useParams } from 'react-router-dom'

import type { StreamEventDetailOut } from '@/api/types'
import { apiFetch } from '@/api/client'
import { AppLayout } from '@/layouts/AppLayout'

export const ManagerStreamPage: React.FC = () => {
  const { id } = useParams()
  const streamId = id as string
  const { message } = AntApp.useApp()
  const qc = useQueryClient()
  const [form] = Form.useForm()

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
          <Space wrap style={{ width: '100%' }}>
            <Form.Item name="start_date" label="Дата старта" rules={[{ required: true }]}>
              <DatePicker format="DD.MM.YYYY" />
            </Form.Item>
            <Form.Item name="duration_days" label="Дней" rules={[{ required: true }]}>
              <Select
                style={{ width: 160 }}
                options={[
                  { label: '1', value: 1 },
                  { label: '2', value: 2 },
                  { label: '3', value: 3 },
                  { label: '4', value: 4 },
                  { label: '5', value: 5 },
                ]}
              />
            </Form.Item>
          </Space>

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
                    <Form.Item name={`day_${idx}_stream_url`} label="stream_url">
                      <Input />
                    </Form.Item>
                    <Form.Item name={`day_${idx}_server_url`} label="server_url">
                      <Input />
                    </Form.Item>
                    <Form.Item name={`day_${idx}_stream_key`} label="stream_key">
                      <Input />
                    </Form.Item>
                  </Card>
                )
              })
            }}
          </Form.Item>

          <Button type="primary" htmlType="submit" icon={<SaveOutlined />} loading={saveMut.isPending}>
            Сохранить
          </Button>
        </Form>
      </Card>
    </AppLayout>
  )
}
