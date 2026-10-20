import {
  CloudSyncOutlined,
  CopyOutlined,
  DeleteOutlined,
  DownloadOutlined,
  PlusOutlined,
  SaveOutlined,
} from '@ant-design/icons'
import {
  App as AntApp,
  Button,
  Card,
  Collapse,
  DatePicker,
  Form,
  Grid,
  Input,
  Modal,
  Select,
  Space,
  Table,
  Tooltip,
  Typography,
} from 'antd'
import type { ColumnsType } from 'antd/es/table'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import dayjs from 'dayjs'
import 'dayjs/locale/ru'
import React, { useMemo, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import type { FfkmAdminSyncResult, StreamEventListOut, StreamEventTemplateOut } from '@/api/types'
import {
  apiFetch,
  createTemplateFromEventRequest,
  deleteEventTemplateRequest,
  instantiateTemplateRequest,
  listEventTemplatesRequest,
} from '@/api/client'
import { ManagerOverviewPanel } from '@/components/ManagerOverviewPanel'
import { OperatorStatsPanel } from '@/components/OperatorStatsPanel'
import { StreamEventsFilterBar } from '@/components/StreamEventsFilterBar'
import { AppLayout } from '@/layouts/AppLayout'
import { formatDateRu } from '@/utils/datetime'
import {
  categoryLabel,
  filterStreamEvents,
  inferStreamCategory,
  type StreamCategory,
} from '@/utils/streamEventFilters'
import {
  currentSeasonYear,
  rangeForSeasonFilter,
  seasonsFromEvents,
  type SeasonFilter,
} from '@/utils/season'

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
  const { message, modal } = AntApp.useApp()
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
  const [seasonFilter, setSeasonFilter] = useState<SeasonFilter>(() => currentSeasonYear())
  const [category, setCategory] = useState<StreamCategory>('official_sports_significant')

  const { data, isLoading } = useQuery({
    queryKey: ['streams'],
    queryFn: async () => (await apiFetch('/stream-events')) as StreamEventListOut[],
  })

  const { data: templates, isLoading: tplLoading } = useQuery({
    queryKey: ['stream-event-templates'],
    queryFn: listEventTemplatesRequest,
  })

  const syncFfkmMut = useMutation({
    mutationFn: async () =>
      (await apiFetch('/stream-events/sync/ffkm-admin', { method: 'POST' })) as FfkmAdminSyncResult,
    onSuccess: async (r) => {
      message.success(
        `ffkm-admin: создано ${r.created}, обновлено ${r.updated}, привязано вручную ${r.linked_manual ?? 0}, ссылки отправлены ${r.pushed_urls ?? 0}/${r.push_attempted ?? 0}`,
      )
      if (r.errors?.length) {
        message.warning(`Ошибки: ${r.errors.slice(0, 3).join('; ')}`)
      }
      await qc.invalidateQueries({ queryKey: ['streams'] })
    },
    onError: (e: Error) => message.error(e.message || 'Не удалось синхронизировать календарь'),
  })

  const createMut = useMutation({
    mutationFn: async (values: {
      title: string
      start_date: dayjs.Dayjs
      duration_days: number
      template_id?: string
    }) => {
      if (values.template_id) {
        await apiFetch('/stream-events', {
          method: 'POST',
          body: JSON.stringify({
            title: values.title,
            start_date: values.start_date.format('YYYY-MM-DD'),
            duration_days: values.duration_days,
            template_id: values.template_id,
          }),
        })
        return
      }
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
      message.success('Мероприятие создано')
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
    mutationFn: async (values: {
      template_id: string
      title: string
      start_date: dayjs.Dayjs
      duration_days: number
    }) =>
      instantiateTemplateRequest(values.template_id, {
        title: values.title,
        start_date: values.start_date.format('YYYY-MM-DD'),
        duration_days: values.duration_days,
      }),
    onSuccess: async (detail) => {
      message.success('Мероприятие создано из шаблона')
      setInstantiateOpen(false)
      instantiateForm.resetFields()
      await qc.invalidateQueries({ queryKey: ['streams'] })
      nav(`/manager/${detail.id}`)
    },
    onError: (e: Error) => message.error(e.message),
  })

  const deleteStreamMut = useMutation({
    mutationFn: async (id: string) => {
      await apiFetch(`/stream-events/${id}`, { method: 'DELETE' })
    },
    onSuccess: async () => {
      message.success('Мероприятие удалено')
      await qc.invalidateQueries({ queryKey: ['streams'] })
    },
    onError: (e: Error) => message.error(e.message),
  })

  const seasonsAvailable = useMemo(
    () => seasonsFromEvents((data ?? []).map((ev) => ev.start_date)),
    [data],
  )

  const range = useMemo(() => rangeForSeasonFilter(seasonFilter), [seasonFilter])

  const filteredEvents = useMemo(
    () =>
      filterStreamEvents(data ?? [], {
        rangeStart: range[0],
        rangeEnd: range[1],
        category,
      }),
    [data, range, category],
  )

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
      title: 'Категория',
      key: 'category',
      width: 170,
      render: (_, r) => (
        <Typography.Text type="secondary" style={{ fontSize: 12 }}>
          {categoryLabel(inferStreamCategory(r))}
        </Typography.Text>
      ),
    },
    {
      title: 'Источник',
      key: 'source',
      width: 110,
      render: (_, r) =>
        r.ffkm_admin_tournament_id ? (
          <Typography.Text type="secondary" style={{ fontSize: 12 }}>
            ffkm-admin #{r.ffkm_admin_tournament_id}
          </Typography.Text>
        ) : (
          <Typography.Text type="secondary" style={{ fontSize: 12 }}>
            вручную
          </Typography.Text>
        ),
    },
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
      title: 'Трансляция',
      key: 'stream_links',
      width: 260,
      render: (_, r) => (
        <Space direction="vertical" size={6} style={{ maxWidth: 280 }}>
          {(r.day_stream_links ?? []).length === 0 ? (
            <Typography.Text type="secondary" style={{ fontSize: 12 }}>
              —
            </Typography.Text>
          ) : (
            (r.day_stream_links ?? []).map((d) => (
              <Space key={d.day_index} size={8} wrap align="center">
                <Typography.Text type="secondary" style={{ fontSize: 12, whiteSpace: 'nowrap' }}>
                  День {d.day_index}
                </Typography.Text>
                {d.stream_url ? (
                  <Tooltip title={d.stream_url}>
                    <Button
                      type="link"
                      size="small"
                      icon={<CopyOutlined />}
                      style={{ padding: 0 }}
                      onClick={async () => {
                        await navigator.clipboard.writeText(d.stream_url)
                        message.success(`День ${d.day_index}: ссылка скопирована`)
                      }}
                      aria-label={`Скопировать ссылку трансляции, день ${d.day_index}`}
                    >
                      Копировать
                    </Button>
                  </Tooltip>
                ) : (
                  <Typography.Text type="secondary" style={{ fontSize: 12 }}>
                    нет ссылки
                  </Typography.Text>
                )}
              </Space>
            ))
          )}
        </Space>
      ),
    },
    {
      title: '',
      key: 'actions',
      width: 280,
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
          <Button
            type="link"
            danger
            icon={<DeleteOutlined />}
            loading={deleteStreamMut.isPending}
            onClick={() => {
              if (r.has_active_broadcast) {
                message.warning('Сначала остановите активный эфир — иначе удаление заблокировано')
                return
              }
              modal.confirm({
                title: 'Удалить мероприятие?',
                content: `«${r.title}»: будут удалены дни, записи эфиров и упоминания. Действие необратимо.`,
                okText: 'Удалить',
                okButtonProps: { danger: true },
                cancelText: 'Отмена',
                onOk: async () => {
                  await deleteStreamMut.mutateAsync(r.id)
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

  const tplColumns: ColumnsType<StreamEventTemplateOut> = [
    { title: 'Имя шаблона', dataIndex: 'name', key: 'name' },
    { title: 'Заголовок', dataIndex: 'title', key: 'title' },
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
              instantiateForm.setFieldsValue({
                template_id: r.id,
                title: '',
                start_date: dayjs(),
                duration_days: r.duration_days,
              })
              setInstantiateOpen(true)
            }}
          >
            Создать мероприятие
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
          Перейти к трансляциям
        </Typography.Text>
      }
    >
      <Card
        title="Оперативная сводка"
        style={{ marginBottom: 16, borderColor: '#e2e8f0', background: '#ffffff' }}
        styles={{ header: { borderBottom: '1px solid #e2e8f0' } }}
      >
        <ManagerOverviewPanel events={data ?? []} category={category} />
      </Card>

      <Collapse
        style={{ marginBottom: 16 }}
        items={[
          {
            key: 'stats',
            label: 'Подробная статистика операторов',
            children: <OperatorStatsPanel compact />,
          },
        ]}
      />

      <Card
        title="Шаблоны мероприятий"
        style={{ marginBottom: 16, borderColor: '#e2e8f0', background: '#ffffff' }}
        styles={{ header: { borderBottom: '1px solid #e2e8f0' } }}
        extra={
          <Typography.Text type="secondary" style={{ fontSize: 12 }}>
            Шаблон запоминает URL сервера — при создании мероприятия он подставляется во все дни; название, даты и
            остальные поля вводятся заново
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
            Мероприятия
          </Typography.Title>
          <Typography.Paragraph type="secondary" style={{ marginBottom: 0 }}>
            Календарь подтягивается из ffkm-admin. Ссылку на трансляцию, URL и ключ заполняете здесь — ссылка уходит в
            ffkm-admin и на сайт автоматически.
          </Typography.Paragraph>
        </div>
        <Space wrap style={{ width: isNarrow ? '100%' : undefined }}>
          <Button
            icon={<CloudSyncOutlined />}
            loading={syncFfkmMut.isPending}
            onClick={() => syncFfkmMut.mutate()}
            block={isNarrow}
            size="large"
          >
            Синхронизировать ffkm-admin
          </Button>
          <Button icon={<DownloadOutlined />} onClick={() => setReportOpen(true)} block={isNarrow} size="large">
            Экспорт отчёта
          </Button>
          <Button type="primary" icon={<PlusOutlined />} onClick={() => setOpen(true)} block={isNarrow} size="large">
            Новое мероприятие
          </Button>
        </Space>
      </Space>

      <StreamEventsFilterBar
        seasonFilter={seasonFilter}
        onSeasonFilterChange={setSeasonFilter}
        seasonsAvailable={seasonsAvailable}
        category={category}
        onCategoryChange={setCategory}
        resultCount={filteredEvents.length}
      />

      <Card style={{ borderColor: '#e2e8f0', background: '#ffffff' }}>
        <Table
          rowKey="id"
          loading={isLoading}
          dataSource={filteredEvents}
          columns={columns}
          pagination={{ pageSize: 10 }}
          scroll={{ x: 1000 }}
          size={isNarrow ? 'small' : 'middle'}
          locale={{ emptyText: 'Нет мероприятий в выбранном сезоне' }}
        />
      </Card>

      <Modal
        title="Новое мероприятие"
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
          <Form.Item
            name="template_id"
            label="Шаблон (необязательно)"
            extra="Подставит один и тот же URL сервера трансляции во все дни. Ссылку, ключ и прочее вводите в карточке мероприятия отдельно."
          >
            <Select
              allowClear
              showSearch
              optionFilterProp="label"
              placeholder="Без шаблона"
              options={(templates ?? []).map((t) => ({ label: `${t.name} · ${t.title}`, value: t.id }))}
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
        title="Мероприятие из шаблона"
        open={instantiateOpen}
        okText="Создать"
        onCancel={() => setInstantiateOpen(false)}
        confirmLoading={instMut.isPending}
        onOk={async () => {
          const v = await instantiateForm.validateFields()
          await instMut.mutateAsync(
            v as {
              template_id: string
              title: string
              start_date: dayjs.Dayjs
              duration_days: number
            },
          )
        }}
      >
        <Form form={instantiateForm} layout="vertical">
          <Form.Item name="template_id" hidden>
            <Input />
          </Form.Item>
          <Form.Item name="title" label="Название мероприятия" rules={[{ required: true, message: 'Обязательно' }]}>
            <Input placeholder="Новое название турнира" />
          </Form.Item>
          <Form.Item name="start_date" label="Дата старта" rules={[{ required: true }]}>
            <DatePicker style={{ width: '100%' }} format="DD.MM.YYYY" />
          </Form.Item>
          <Form.Item name="duration_days" label="Длительность (дней)" rules={[{ required: true }]}>
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
          <Typography.Paragraph type="secondary" style={{ marginBottom: 0, fontSize: 12 }}>
            Из шаблона подставится только URL сервера во все дни; ссылки и ключи заполните в карточке.
          </Typography.Paragraph>
        </Form>
      </Modal>

      <Modal
        title="Экспорт отчёта по упоминаниям"
        open={reportOpen}
        onCancel={() => setReportOpen(false)}
        footer={null}
      >
        <Form form={reportForm} layout="vertical">
          <Form.Item name="stream_id" label="Фильтр: мероприятие (необязательно)">
            <Select
              allowClear
              placeholder="Все мероприятия"
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
