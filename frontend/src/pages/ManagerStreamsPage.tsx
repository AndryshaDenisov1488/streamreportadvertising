import { DeleteOutlined, DownloadOutlined, PlusOutlined, SaveOutlined } from '@ant-design/icons'
import {
  App as AntApp,
  Button,
  Card,
  DatePicker,
  Form,
  Grid,
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
import { Link, useNavigate } from 'react-router-dom'

import type { StreamEventListOut, StreamEventTemplateOut } from '@/api/types'
import {
  apiFetch,
  createTemplateFromEventRequest,
  deleteEventTemplateRequest,
  instantiateTemplateRequest,
  listEventTemplatesRequest,
} from '@/api/client'
import { OperatorStatsPanel } from '@/components/OperatorStatsPanel'
import { AppLayout } from '@/layouts/AppLayout'
import { formatDateRu } from '@/utils/datetime'

dayjs.locale('ru')

const buildReportPath = (
  format: 'docx' | 'csv' | 'xlsx',
  v: { stream_id?: string; range?: [dayjs.Dayjs, dayjs.Dayjs] },
) => {
  const params = new URLSearchParams()
  if (v.stream_id) {
    params.set('stream_id', v.stream_id)
  }
  if (v.range?.[0] && v.range?.[1]) {
    params.set('date_from', v.range[0].format('YYYY-MM-DD'))
    params.set('date_to', v.range[1].format('YYYY-MM-DD'))
  }
  const qs = params.toString()
  const ext = format === 'docx' ? 'export.docx' : format === 'csv' ? 'export.csv' : 'export.xlsx'
  return `/reports/${ext}${qs ? `?${qs}` : ''}`
}

export const ManagerStreamsPage: React.FC = () => {
  const { message } = AntApp.useApp()
  const qc = useQueryClient()
  const nav = useNavigate()
  const screens = Grid.useBreakpoint()
  const isNarrow = !screens.md
  const [open, setOpen] = useState(false)
  const [reportOpen, setReportOpen] = useState(false)
  const [tplNameOpen, setTplNameOpen] = useState(false)
  const [tplStreamId, setTplStreamId] = useState<string | null>(null)
  const [instantiateOpen, setInstantiateOpen] = useState(false)
  const [createForm] = Form.useForm()
  const [reportForm] = Form.useForm()
  const [tplNameForm] = Form.useForm()
  const [instantiateForm] = Form.useForm()

  const { data, isLoading } = useQuery({
    queryKey: ['streams'],
    queryFn: async () => (await apiFetch('/stream-events')) as StreamEventListOut[],
  })

  const { data: templates, isLoading: tplLoading } = useQuery({
    queryKey: ['stream-event-templates'],
    queryFn: listEventTemplatesRequest,
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

  const downloadExport = async (format: 'docx' | 'csv' | 'xlsx') => {
    const v = reportForm.getFieldsValue() as {
      stream_id?: string
      range?: [dayjs.Dayjs, dayjs.Dayjs]
    }
    const path = buildReportPath(format, v)
    const blob = (await apiFetch(path)) as Blob
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download =
      format === 'docx' ? 'mentions_report.docx' : format === 'csv' ? 'mentions_report.csv' : 'mentions_report.xlsx'
    a.click()
    URL.revokeObjectURL(url)
    message.success('Файл скачан')
  }

  const saveTplMut = useMutation({
    mutationFn: async ({ streamId, name }: { streamId: string; name: string }) =>
      createTemplateFromEventRequest(streamId, name),
    onSuccess: async () => {
      message.success('Шаблон сохранён')
      setTplNameOpen(false)
      setTplStreamId(null)
      tplNameForm.resetFields()
      await qc.invalidateQueries({ queryKey: ['stream-event-templates'] })
    },
    onError: (e: Error) => message.error(e.message),
  })

  const delTplMut = useMutation({
    mutationFn: deleteEventTemplateRequest,
    onSuccess: async () => {
      message.success('Шаблон удалён')
      await qc.invalidateQueries({ queryKey: ['stream-event-templates'] })
    },
    onError: (e: Error) => message.error(e.message),
  })

  const instMut = useMutation({
    mutationFn: async (values: { template_id: string; start_date: dayjs.Dayjs }) =>
      instantiateTemplateRequest(values.template_id, values.start_date.format('YYYY-MM-DD')),
    onSuccess: async (detail) => {
      message.success('Событие создано из шаблона')
      setInstantiateOpen(false)
      instantiateForm.resetFields()
      await qc.invalidateQueries({ queryKey: ['streams'] })
      nav(`/manager/${detail.id}`)
    },
    onError: (e: Error) => message.error(e.message),
  })

  const columns: ColumnsType<StreamEventListOut> = [
    { title: 'Название', dataIndex: 'title', key: 'title' },
    {
      title: 'Старт',
      dataIndex: 'start_date',
      key: 'start_date',
      width: 120,
      render: (v: string) => formatDateRu(v),
    },
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
            {r.assignment_summary
              ? r.assignment_summary
              : r.locked_by_user_id
                ? r.locked_by_display_name
                  ? `В работе: ${r.locked_by_display_name}`
                  : 'В работе у оператора'
                : 'Свободно'}
          </Typography.Text>
        </Space>
      ),
    },
    {
      title: '',
      key: 'actions',
      width: 220,
      render: (_, r) => (
        <Space wrap size="small">
          <Link to={`/manager/${r.id}`}>
            <Button type="link">Подробнее</Button>
          </Link>
          <Button
            type="link"
            icon={<SaveOutlined />}
            onClick={() => {
              setTplStreamId(r.id)
              tplNameForm.setFieldsValue({ name: `${r.title} (шаблон)` })
              setTplNameOpen(true)
            }}
          >
            В шаблон
          </Button>
        </Space>
      ),
    },
  ]

  const tplColumns: ColumnsType<StreamEventTemplateOut> = [
    { title: 'Имя шаблона', dataIndex: 'name', key: 'name' },
    { title: 'Заголовок эфира', dataIndex: 'title', key: 'title' },
    { title: 'Дней', dataIndex: 'duration_days', key: 'duration_days', width: 72 },
    {
      title: '',
      key: 'act',
      width: 200,
      render: (_, r) => (
        <Space>
          <Button
            type="link"
            onClick={() => {
              instantiateForm.setFieldsValue({ template_id: r.id, start_date: dayjs() })
              setInstantiateOpen(true)
            }}
          >
            Создать событие
          </Button>
          <Button
            type="text"
            danger
            icon={<DeleteOutlined />}
            onClick={() => void delTplMut.mutateAsync(r.id)}
            loading={delTplMut.isPending}
          />
        </Space>
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
      <Card
        title="Статистика операторов"
        style={{ marginBottom: 16, borderColor: '#1f2a3a', background: '#0d1219' }}
        styles={{ header: { borderBottom: '1px solid #1f2a3a' } }}
      >
        <OperatorStatsPanel compact />
      </Card>

      <Card
        title="Шаблоны эфиров"
        style={{ marginBottom: 16, borderColor: '#1f2a3a', background: '#0d1219' }}
        styles={{ header: { borderBottom: '1px solid #1f2a3a' } }}
        extra={
          <Typography.Text type="secondary" style={{ fontSize: 12 }}>
            Сохраняйте настройки дней из события или создавайте копию по кнопке ниже
          </Typography.Text>
        }
      >
        <Table
          rowKey="id"
          loading={tplLoading}
          dataSource={templates ?? []}
          columns={tplColumns}
          pagination={{ pageSize: 6 }}
          size="small"
          scroll={{ x: 640 }}
        />
      </Card>

      <Space
        style={{ width: '100%', justifyContent: 'space-between', marginBottom: 16 }}
        align="start"
        direction={isNarrow ? 'vertical' : 'horizontal'}
        size="middle"
      >
        <div>
          <Typography.Title level={3} style={{ marginTop: 0 }}>
            События
          </Typography.Title>
          <Typography.Paragraph type="secondary" style={{ marginBottom: 0 }}>
            Создание, шаблоны, отчёты — Word, CSV и Excel.
          </Typography.Paragraph>
        </div>
        <Space wrap style={{ width: isNarrow ? '100%' : undefined }}>
          <Button icon={<DownloadOutlined />} onClick={() => setReportOpen(true)} block={isNarrow} size="large">
            Экспорт отчёта
          </Button>
          <Button type="primary" icon={<PlusOutlined />} onClick={() => setOpen(true)} block={isNarrow} size="large">
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
          scroll={{ x: 720 }}
          size={isNarrow ? 'small' : 'middle'}
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
        title="Имя шаблона"
        open={tplNameOpen}
        okText="Сохранить"
        onCancel={() => {
          setTplNameOpen(false)
          setTplStreamId(null)
        }}
        confirmLoading={saveTplMut.isPending}
        onOk={async () => {
          const v = await tplNameForm.validateFields()
          if (!tplStreamId) {
            return
          }
          await saveTplMut.mutateAsync({ streamId: tplStreamId, name: v.name as string })
        }}
      >
        <Form form={tplNameForm} layout="vertical">
          <Form.Item name="name" label="Название шаблона" rules={[{ required: true, message: 'Обязательно' }]}>
            <Input />
          </Form.Item>
        </Form>
      </Modal>

      <Modal
        title="Событие из шаблона"
        open={instantiateOpen}
        okText="Создать"
        onCancel={() => setInstantiateOpen(false)}
        confirmLoading={instMut.isPending}
        onOk={async () => {
          const v = await instantiateForm.validateFields()
          await instMut.mutateAsync(v as { template_id: string; start_date: dayjs.Dayjs })
        }}
      >
        <Form form={instantiateForm} layout="vertical">
          <Form.Item name="template_id" label="Шаблон" rules={[{ required: true }]}>
            <Select
              options={(templates ?? []).map((t) => ({ label: `${t.name} · ${t.title}`, value: t.id }))}
              placeholder="Выберите шаблон"
            />
          </Form.Item>
          <Form.Item name="start_date" label="Дата старта" rules={[{ required: true }]}>
            <DatePicker style={{ width: '100%' }} format="DD.MM.YYYY" />
          </Form.Item>
        </Form>
      </Modal>

      <Modal
        title="Экспорт отчёта по упоминаниям"
        open={reportOpen}
        onCancel={() => setReportOpen(false)}
        footer={null}
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
          <Space wrap>
            <Button
              type="primary"
              icon={<DownloadOutlined />}
              onClick={async () => {
                try {
                  await downloadExport('docx')
                  setReportOpen(false)
                } catch (e) {
                  message.error(e instanceof Error ? e.message : 'Ошибка')
                }
              }}
            >
              Скачать Word (.docx)
            </Button>
            <Button
              onClick={async () => {
                try {
                  await downloadExport('csv')
                  setReportOpen(false)
                } catch (e) {
                  message.error(e instanceof Error ? e.message : 'Ошибка')
                }
              }}
            >
              Скачать CSV
            </Button>
            <Button
              onClick={async () => {
                try {
                  await downloadExport('xlsx')
                  setReportOpen(false)
                } catch (e) {
                  message.error(e instanceof Error ? e.message : 'Ошибка')
                }
              }}
            >
              Скачать Excel (.xlsx)
            </Button>
          </Space>
        </Form>
      </Modal>
    </AppLayout>
  )
}
