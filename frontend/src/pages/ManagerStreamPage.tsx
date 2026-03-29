import {
  ArrowLeftOutlined,
  CopyOutlined,
  DeleteOutlined,
  DownloadOutlined,
  FileZipOutlined,
  LinkOutlined,
  PlusOutlined,
  SaveOutlined,
} from '@ant-design/icons'
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
  Modal,
  Row,
  Select,
  Space,
  Spin,
  Tabs,
  Typography,
  Upload,
} from 'antd'
import type { UploadFile } from 'antd/es/upload/interface'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import dayjs from 'dayjs'
import React, { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import type { LogoLibraryItemOut, SponsorMentionOut, StreamEventDetailOut } from '@/api/types'
import { apiFetch, fetchAuthorizedBlob, triggerBlobDownload, uploadLogosBatchRequest } from '@/api/client'
import { BroadcastActualStartPanel } from '@/components/BroadcastActualStartPanel'
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

const LOGO_UPLOAD_MAX_FILES = 30
const LOGO_UPLOAD_MAX_BYTES = 15 * 1024 * 1024

export const ManagerStreamPage: React.FC = () => {
  const { id } = useParams()
  const streamId = id as string
  const screens = Grid.useBreakpoint()
  const isNarrow = !screens.sm
  const { message } = AntApp.useApp()
  const qc = useQueryClient()
  const [form] = Form.useForm()
  const [mentionDay, setMentionDay] = useState(1)
  const [addLogoOpen, setAddLogoOpen] = useState(false)
  const [logoModalUploadList, setLogoModalUploadList] = useState<UploadFile[]>([])
  const [logoBatchBusy, setLogoBatchBusy] = useState(false)

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
      content_url: data.content_url ?? '',
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

  useEffect(() => {
    if (!addLogoOpen) {
      setLogoModalUploadList([])
      setLogoBatchBusy(false)
    }
  }, [addLogoOpen])

  const handleConfirmLogoUpload = async () => {
    const raw: File[] = []
    for (const f of logoModalUploadList) {
      if (f.originFileObj) {
        raw.push(f.originFileObj as File)
      }
    }
    if (!raw.length) {
      message.warning('Выберите файлы, затем нажмите «Загрузить к эфиру»')
      return
    }
    if (raw.length > LOGO_UPLOAD_MAX_FILES) {
      message.warning(`Не больше ${LOGO_UPLOAD_MAX_FILES} файлов за раз`)
      return
    }
    for (const f of raw) {
      if (f.size > LOGO_UPLOAD_MAX_BYTES) {
        message.error(`Файл «${f.name}» больше 15 МБ`)
        return
      }
    }
    setLogoBatchBusy(true)
    try {
      const items = await uploadLogosBatchRequest(raw)
      for (const item of items) {
        await apiFetch(`/stream-events/${streamId}/logos`, {
          method: 'POST',
          body: JSON.stringify({ logo_id: item.id }),
        })
      }
      message.success(`Добавлено файлов: ${items.length}`)
      await qc.invalidateQueries({ queryKey: ['stream', streamId] })
      await qc.invalidateQueries({ queryKey: ['logos-library'] })
      setLogoModalUploadList([])
      setAddLogoOpen(false)
    } catch (e) {
      message.error((e as Error).message)
    } finally {
      setLogoBatchBusy(false)
    }
  }

  const mentionsQuery = useQuery({
    queryKey: ['mentions', streamId, mentionDay],
    enabled: Boolean(streamId) && Boolean(data),
    queryFn: async () =>
      (await apiFetch(`/stream-events/${streamId}/days/${mentionDay}/mentions`)) as SponsorMentionOut[],
  })

  useStreamWs(
    streamId,
    () => {
      void qc.invalidateQueries({ queryKey: ['mentions', streamId] })
      void qc.invalidateQueries({ queryKey: ['stream', streamId] })
    },
    Boolean(data),
  )

  const logosLibraryQuery = useQuery({
    queryKey: ['logos-library'],
    enabled: addLogoOpen,
    queryFn: async () => (await apiFetch('/logos')) as LogoLibraryItemOut[],
  })

  const attachLogoMut = useMutation({
    mutationFn: async (logoId: string) => {
      await apiFetch(`/stream-events/${streamId}/logos`, {
        method: 'POST',
        body: JSON.stringify({ logo_id: logoId }),
      })
    },
    onSuccess: async () => {
      message.success('Логотип добавлен к мероприятию')
      setAddLogoOpen(false)
      await qc.invalidateQueries({ queryKey: ['stream', streamId] })
      await qc.invalidateQueries({ queryKey: ['logos-library'] })
    },
    onError: (e: Error) => message.error(e.message),
  })

  const detachLogoMut = useMutation({
    mutationFn: async (logoId: string) => {
      await apiFetch(`/stream-events/${streamId}/logos/${logoId}`, { method: 'DELETE' })
    },
    onSuccess: async () => {
      message.success('Логотип откреплён')
      await qc.invalidateQueries({ queryKey: ['stream', streamId] })
    },
    onError: (e: Error) => message.error(e.message),
  })

  const downloadZipMut = useMutation({
    mutationFn: async () => {
      const { blob, filename } = await fetchAuthorizedBlob(`/stream-events/${streamId}/logos/archive.zip`)
      triggerBlobDownload(blob, filename)
    },
    onError: (e: Error) => message.error(e.message),
  })

  const downloadOneMut = useMutation({
    mutationFn: async (logoId: string) => {
      const { blob, filename } = await fetchAuthorizedBlob(`/stream-events/${streamId}/logos/${logoId}/file`)
      triggerBlobDownload(blob, filename)
    },
    onError: (e: Error) => message.error(e.message),
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
      const rawUrl = values.content_url
      const content_url =
        rawUrl == null || String(rawUrl).trim() === '' ? null : String(rawUrl).trim()
      await apiFetch(`/stream-events/${streamId}`, {
        method: 'PATCH',
        body: JSON.stringify({
          title: values.title,
          start_date: (values.start_date as dayjs.Dayjs).format('YYYY-MM-DD'),
          duration_days: duration,
          days,
          content_url,
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

  const handleCopyContentUrl = async () => {
    const v = form.getFieldValue('content_url') as string | undefined
    if (!v || !String(v).trim()) {
      message.warning('Ссылка пустая')
      return
    }
    await navigator.clipboard.writeText(String(v).trim())
    message.success('Скопировано')
  }

  const handleOpenContentUrl = () => {
    const v = form.getFieldValue('content_url') as string | undefined
    if (!v || !String(v).trim()) {
      message.warning('Ссылка пустая')
      return
    }
    window.open(String(v).trim(), '_blank', 'noopener,noreferrer')
  }

  return (
    <AppLayout
      nav={
        <Space>
          <Link to="/manager">
            <Button type="link" icon={<ArrowLeftOutlined />}>
              Назад
            </Button>
          </Link>
          <Typography.Text type="secondary">Карточка мероприятия</Typography.Text>
        </Space>
      }
    >
      <Typography.Title level={3} style={{ marginTop: 0 }}>
        Редактирование
      </Typography.Title>

      {data && data.active_broadcasts.length > 0 ? (
        <Card
          size="small"
          title="Активный эфир — фактическое время начала"
          style={{ marginBottom: 16, borderColor: '#e2e8f0', background: '#ffffff' }}
          styles={{ header: { borderBottom: '1px solid #e2e8f0' } }}
        >
          <Typography.Paragraph type="secondary" style={{ marginBottom: 12 }}>
            Если оператор нажал «Начать эфир» позже, чем реально пошла картинка, укажите время старта в МСК — таймкоды
            сдвинутся.
          </Typography.Paragraph>
          <Space direction="vertical" size={16} style={{ width: '100%' }}>
            {data.active_broadcasts.map((b) => (
              <div key={b.id}>
                <Typography.Text strong style={{ display: 'block', marginBottom: 8 }}>
                  День {b.day_index}
                </Typography.Text>
                <BroadcastActualStartPanel streamId={streamId} dayIndex={b.day_index} startedAtIso={b.started_at} />
              </div>
            ))}
          </Space>
        </Card>
      ) : null}

      <Card
        title="Упоминания оператора"
        style={{ marginBottom: 16, borderColor: '#e2e8f0', background: '#ffffff' }}
        styles={{ header: { borderBottom: '1px solid #e2e8f0' } }}
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
          <Typography.Text type="secondary">Загрузка мероприятия…</Typography.Text>
        )}
      </Card>

      <Card
        title="Логотипы"
        style={{ marginBottom: 16, borderColor: '#e2e8f0', background: '#ffffff' }}
        styles={{ header: { borderBottom: '1px solid #e2e8f0' } }}
        extra={
          <Space wrap>
            <Button
              icon={<FileZipOutlined />}
              onClick={() => downloadZipMut.mutate()}
              loading={downloadZipMut.isPending}
              disabled={!(data?.logos ?? []).length}
            >
              Скачать ZIP
            </Button>
            <Button type="primary" icon={<PlusOutlined />} onClick={() => setAddLogoOpen(true)}>
              Добавить логотип
            </Button>
          </Space>
        }
      >
        {!data ? (
          <Typography.Text type="secondary">Загрузка…</Typography.Text>
        ) : (data.logos ?? []).length === 0 ? (
          <Typography.Text type="secondary">Нет логотипов — нажмите «Добавить логотип»</Typography.Text>
        ) : (
          <Row gutter={[12, 12]}>
            {(data.logos ?? []).map((lg) => (
              <Col xs={12} sm={8} md={6} key={lg.id}>
                <Card
                  size="small"
                  cover={
                    <img
                      alt={lg.filename_original}
                      src={lg.public_url}
                      style={{ maxHeight: 120, objectFit: 'contain', padding: 8 }}
                    />
                  }
                >
                  <Space direction="vertical" size={4} style={{ width: '100%' }}>
                    <Typography.Text ellipsis style={{ fontSize: 12 }} title={lg.filename_original}>
                      {lg.filename_original}
                    </Typography.Text>
                    <Space wrap>
                      <Button
                        size="small"
                        icon={<DownloadOutlined />}
                        loading={downloadOneMut.isPending}
                        onClick={() => downloadOneMut.mutate(lg.id)}
                        aria-label={`Скачать ${lg.filename_original}`}
                      />
                      <Button
                        size="small"
                        danger
                        icon={<DeleteOutlined />}
                        loading={detachLogoMut.isPending}
                        onClick={() => detachLogoMut.mutate(lg.id)}
                        aria-label="Открепить логотип"
                      />
                    </Space>
                  </Space>
                </Card>
              </Col>
            ))}
          </Row>
        )}
      </Card>

      <Modal
        title="Добавить логотип"
        open={addLogoOpen}
        onCancel={() => setAddLogoOpen(false)}
        footer={null}
        destroyOnClose
        width={720}
      >
        <Tabs
          items={[
            {
              key: 'lib',
              label: 'Из медиатеки',
              children: (
                <div style={{ minHeight: 200 }}>
                  {logosLibraryQuery.isLoading ? (
                    <Typography.Text type="secondary">Загрузка списка…</Typography.Text>
                  ) : (
                    <Row gutter={[12, 12]}>
                      {(logosLibraryQuery.data ?? []).map((item) => (
                        <Col xs={12} sm={8} key={item.id}>
                          <Card
                            size="small"
                            hoverable
                            onClick={() => attachLogoMut.mutate(item.id)}
                            cover={
                              <img
                                alt={item.filename_original}
                                src={item.public_url}
                                style={{ maxHeight: 100, objectFit: 'contain', padding: 8 }}
                              />
                            }
                          >
                            <Typography.Text ellipsis style={{ fontSize: 12 }} title={item.filename_original}>
                              {item.filename_original}
                            </Typography.Text>
                          </Card>
                        </Col>
                      ))}
                    </Row>
                  )}
                </div>
              ),
            },
            {
              key: 'up',
              label: 'Загрузить файл',
              children: (
                <Spin spinning={logoBatchBusy} tip="Загрузка…">
                  <Space direction="vertical" style={{ width: '100%' }} size="middle">
                    <Upload.Dragger
                      multiple
                      maxCount={LOGO_UPLOAD_MAX_FILES}
                      accept="image/png,image/jpeg,image/gif,image/webp,image/svg+xml"
                      fileList={logoModalUploadList}
                      disabled={logoBatchBusy}
                      beforeUpload={() => false}
                      onChange={({ fileList }) => setLogoModalUploadList(fileList)}
                    >
                      <p className="ant-upload-text">Перетащите файлы или нажмите для выбора</p>
                      <p className="ant-upload-hint" style={{ color: '#64748b' }}>
                        Можно выбрать несколько файлов сразу. PNG, JPEG, GIF, WebP, SVG до 15 МБ каждый, не более{' '}
                        {LOGO_UPLOAD_MAX_FILES} за раз. После выбора нажмите кнопку ниже.
                      </p>
                    </Upload.Dragger>
                    <Button
                      type="primary"
                      block
                      loading={logoBatchBusy}
                      disabled={logoModalUploadList.length === 0 || logoBatchBusy}
                      onClick={() => void handleConfirmLogoUpload()}
                    >
                      Загрузить к эфиру
                    </Button>
                  </Space>
                </Spin>
              ),
            },
          ]}
        />
      </Modal>

      <Card loading={isLoading} style={{ borderColor: '#e2e8f0', background: '#ffffff' }}>
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

          <Form.Item
            name="content_url"
            label="Ссылка на материалы (контент, например Яндекс.Диск)"
            rules={[
              {
                validator: async (_, v) => {
                  if (v == null || String(v).trim() === '') {
                    return Promise.resolve()
                  }
                  try {
                    // eslint-disable-next-line no-new
                    new URL(String(v))
                    return Promise.resolve()
                  } catch {
                    return Promise.reject(new Error('Введите корректный URL'))
                  }
                },
              },
            ]}
          >
            <Input
              placeholder="https://..."
              addonAfter={
                <Space size={0}>
                  <Button
                    type="text"
                    size="small"
                    icon={<CopyOutlined />}
                    onClick={(e) => {
                      e.preventDefault()
                      void handleCopyContentUrl()
                    }}
                    aria-label="Копировать ссылку"
                  />
                  <Button
                    type="text"
                    size="small"
                    icon={<LinkOutlined />}
                    onClick={(e) => {
                      e.preventDefault()
                      handleOpenContentUrl()
                    }}
                    aria-label="Открыть в новой вкладке"
                  />
                </Space>
              }
            />
          </Form.Item>

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
                    style={{ marginBottom: 12, borderColor: '#e2e8f0', background: '#f8fafc' }}
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
