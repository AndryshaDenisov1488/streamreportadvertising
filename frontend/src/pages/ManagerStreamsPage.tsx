import { DownloadOutlined, PlusOutlined } from '@ant-design/icons'
import {
  App as AntApp,
  Button,
  Card,
  DatePicker,
  Form,
  Input,
  Modal,
  Select,
  Space,
  Table,
  Typography,
} from 'antd'
import type { ColumnsType } from 'antd/es/table'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import dayjs from 'dayjs'
import 'dayjs/locale/ru'
import React, { useState } from 'react'
import { Link } from 'react-router-dom'

import type { StreamEventListOut } from '@/api/types'
import { apiFetch } from '@/api/client'
import { AppLayout } from '@/layouts/AppLayout'

dayjs.locale('ru')

export const ManagerStreamsPage: React.FC = () => {
  const { message } = AntApp.useApp()
  const qc = useQueryClient()
  const [open, setOpen] = useState(false)
  const [reportOpen, setReportOpen] = useState(false)
  const [createForm] = Form.useForm()
  const [reportForm] = Form.useForm()

  const { data, isLoading } = useQuery({
    queryKey: ['streams'],
    queryFn: async () => (await apiFetch('/stream-events')) as StreamEventListOut[],
  })

  const createMut = useMutation({
    mutationFn: async (values: { title: string; start_date: dayjs.Dayjs; duration_days: number }) => {
      const days = Array.from({ length: values.duration_days }, (_, i) => ({
        day_index: i + 1,
        stream_url: '',
        server_url: '',
        stream_key: '',
      }))
      await apiFetch('/stream-events', {
        method: 'POST',
        body: JSON.stringify({
          title: values.title,
          start_date: values.start_date.format('YYYY-MM-DD'),
          duration_days: values.duration_days,
          days,
        }),
      })
    },
    onSuccess: async () => {
      message.success('Событие создано')
      setOpen(false)
      createForm.resetFields()
      await qc.invalidateQueries({ queryKey: ['streams'] })
    },
    onError: (e: Error) => message.error(e.message),
  })

  const handleExport = async () => {
    const v = reportForm.getFieldsValue() as {
      stream_id?: string
      range?: [dayjs.Dayjs, dayjs.Dayjs]
    }
    const params = new URLSearchParams()
    if (v.stream_id) {
      params.set('stream_id', v.stream_id)
    }
    if (v.range?.[0] && v.range?.[1]) {
      params.set('date_from', v.range[0].format('YYYY-MM-DD'))
      params.set('date_to', v.range[1].format('YYYY-MM-DD'))
    }
    const qs = params.toString()
    const path = `/reports/export.docx${qs ? `?${qs}` : ''}`
    const blob = (await apiFetch(path)) as Blob
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'mentions_report.docx'
    a.click()
    URL.revokeObjectURL(url)
    message.success('Файл скачан')
  }

  const columns: ColumnsType<StreamEventListOut> = [
    { title: 'Название', dataIndex: 'title', key: 'title' },
    { title: 'Старт', dataIndex: 'start_date', key: 'start_date', width: 140 },
    { title: 'Дней', dataIndex: 'duration_days', key: 'duration_days', width: 90 },
    {
      title: 'Статус',
      key: 'status',
      render: (_, r) => (
        <Space direction="vertical" size={0}>
          <Typography.Text type="secondary">
            {r.has_active_broadcast ? 'Эфир активен' : 'Нет эфира'}
          </Typography.Text>
          <Typography.Text type="secondary" style={{ fontSize: 12 }}>
            {r.locked_by_user_id ? 'В работе у оператора' : 'Свободно'}
          </Typography.Text>
        </Space>
      ),
    },
    {
      title: '',
      key: 'actions',
      width: 160,
      render: (_, r) => (
        <Link to={`/manager/${r.id}`}>
          <Button type="link">Подробнее</Button>
        </Link>
      ),
    },
  ]

  return (
    <AppLayout
      nav={
        <Typography.Text type="secondary" style={{ fontSize: 13 }}>
          Менеджер стримов
        </Typography.Text>
      }
    >
      <Space style={{ width: '100%', justifyContent: 'space-between', marginBottom: 16 }} align="start" wrap>
        <div>
          <Typography.Title level={3} style={{ marginTop: 0 }}>
            События
          </Typography.Title>
          <Typography.Paragraph type="secondary" style={{ marginBottom: 0 }}>
            Создание, редактирование, отчёты и выгрузка в Word.
          </Typography.Paragraph>
        </div>
        <Space wrap>
          <Button icon={<DownloadOutlined />} onClick={() => setReportOpen(true)}>
            Экспорт Word
          </Button>
          <Button type="primary" icon={<PlusOutlined />} onClick={() => setOpen(true)}>
            Новое событие
          </Button>
        </Space>
      </Space>

      <Card style={{ borderColor: '#1f2a3a', background: '#0d1219' }}>
        <Table
          rowKey="id"
          loading={isLoading}
          dataSource={data ?? []}
          columns={columns}
          pagination={{ pageSize: 10 }}
        />
      </Card>

      <Modal
        title="Новое событие"
        open={open}
        okText="Создать"
        cancelText="Отмена"
        confirmLoading={createMut.isPending}
        onCancel={() => setOpen(false)}
        onOk={async () => {
          const v = await createForm.validateFields()
          await createMut.mutateAsync(v)
        }}
      >
        <Form form={createForm} layout="vertical">
          <Form.Item name="title" label="Название" rules={[{ required: true, message: 'Обязательно' }]}>
            <Input />
          </Form.Item>
          <Form.Item name="start_date" label="Дата старта" rules={[{ required: true, message: 'Обязательно' }]}>
            <DatePicker style={{ width: '100%' }} format="DD.MM.YYYY" />
          </Form.Item>
          <Form.Item
            name="duration_days"
            label="Длительность (дней)"
            initialValue={3}
            rules={[{ required: true }]}
          >
            <Select
              options={[
                { label: '1', value: 1 },
                { label: '2', value: 2 },
                { label: '3', value: 3 },
                { label: '4', value: 4 },
                { label: '5', value: 5 },
              ]}
            />
          </Form.Item>
        </Form>
      </Modal>

      <Modal
        title="Экспорт отчёта"
        open={reportOpen}
        onCancel={() => setReportOpen(false)}
        okText="Скачать .docx"
        onOk={async () => {
          try {
            await handleExport()
            setReportOpen(false)
          } catch (e) {
            message.error(e instanceof Error ? e.message : 'Ошибка')
          }
        }}
      >
        <Form form={reportForm} layout="vertical">
          <Form.Item name="stream_id" label="Фильтр: событие (необязательно)">
            <Select
              allowClear
              placeholder="Все события"
              options={(data ?? []).map((s) => ({ label: s.title, value: s.id }))}
            />
          </Form.Item>
          <Form.Item name="range" label="Диапазон дат (по времени создания упоминания, МСК)">
            <DatePicker.RangePicker style={{ width: '100%' }} format="DD.MM.YYYY" />
          </Form.Item>
        </Form>
      </Modal>
    </AppLayout>
  )
}
