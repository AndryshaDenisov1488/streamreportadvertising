import {
  ArrowLeftOutlined,
  CheckOutlined,
  CopyOutlined,
  DownloadOutlined,
  FileZipOutlined,
  LinkOutlined,
  PlusOutlined,
  PlayCircleOutlined,
  StopOutlined,
} from '@ant-design/icons'
import {
  App as AntApp,
  Badge,
  Button,
  Card,
  Checkbox,
  Col,
  Divider,
  Grid,
  Row,
  InputNumber,
  List,
  Modal,
  Select,
  Space,
  Tooltip,
  Typography,
} from 'antd'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import type { BroadcastChecklistOut, SponsorMentionOut, StreamEventDetailOut } from '@/api/types'
import { apiFetch, fetchAuthorizedBlob, triggerBlobDownload } from '@/api/client'
import { useAuth } from '@/auth/AuthContext'
import { BroadcastActualStartPanel } from '@/components/BroadcastActualStartPanel'
import { useStreamWs } from '@/hooks/useStreamWs'
import { AppLayout } from '@/layouts/AppLayout'
import { formatDateRu, formatDateTimeRu } from '@/utils/datetime'

const formatElapsed = (totalSec: number) => {
  const sec = Math.max(0, Math.floor(totalSec))
  const h = Math.floor(sec / 3600)
  const m = Math.floor((sec % 3600) / 60)
  const s = sec % 60
  return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
}

const IDLE_REMINDER_MS = 2 * 60 * 60 * 1000

const MENTION_SLOT_LABELS = ['Начало эфира', 'Середина 1', 'Середина 2', 'Конец эфира'] as const

export const OperatorEventPage: React.FC = () => {
  const { id } = useParams()
  const streamId = id as string
  const { user } = useAuth()
  const { message, modal } = AntApp.useApp()
  const handleCopyLinkField = useCallback(
    async (text: string) => {
      const t = text.trim()
      if (!t) {
        return
      }
      try {
        await navigator.clipboard.writeText(t)
        message.success('Скопировано в буфер обмена')
      } catch {
        message.error('Не удалось скопировать')
      }
    },
    [message],
  )
  const qc = useQueryClient()
  const screens = Grid.useBreakpoint()
  const isComfortable = Boolean(screens.md)
  const [day, setDay] = useState(1)
  const [tick, setTick] = useState(0)
  const [adjustTarget, setAdjustTarget] = useState<SponsorMentionOut | null>(null)
  const [adjustMinutes, setAdjustMinutes] = useState(0)
  const [adjustSecondsPart, setAdjustSecondsPart] = useState(0)

  const detailQuery = useQuery({
    queryKey: ['stream', streamId],
    enabled: Boolean(streamId),
    queryFn: async () => (await apiFetch(`/stream-events/${streamId}`)) as StreamEventDetailOut,
  })

  const checklistQuery = useQuery({
    queryKey: ['checklist', streamId, day],
    enabled: Boolean(streamId) && detailQuery.isSuccess,
    queryFn: async () =>
      (await apiFetch(`/stream-events/${streamId}/days/${day}/checklist`)) as BroadcastChecklistOut,
  })

  const checklistMut = useMutation({
    mutationFn: async (patch: {
      picture_exposure_ok?: boolean
      judges_stream_ok?: boolean
      splitter_socket_ok?: boolean
      key_stream_started_ok?: boolean
      kick_ok?: boolean
      mentions_four_ok?: boolean
    }) => {
      await apiFetch(`/stream-events/${streamId}/days/${day}/checklist`, {
        method: 'PUT',
        body: JSON.stringify(patch),
      })
    },
    onSuccess: async () => {
      await qc.invalidateQueries({ queryKey: ['checklist', streamId] })
    },
  })

  const [wsViewers, setWsViewers] = useState<number | null>(null)

  useStreamWs(
    streamId,
    (msg) => {
      if (msg.type === 'presence') {
        const p = msg.payload as { viewers?: number } | undefined
        if (p?.viewers != null) {
          setWsViewers(p.viewers)
        }
        return
      }
      void qc.invalidateQueries({ queryKey: ['stream', streamId] })
      void qc.invalidateQueries({ queryKey: ['mentions', streamId, day] })
    },
    detailQuery.isSuccess,
  )

  const mentionsQuery = useQuery({
    queryKey: ['mentions', streamId, day],
    enabled: Boolean(streamId),
    queryFn: async () =>
      (await apiFetch(`/stream-events/${streamId}/days/${day}/mentions`)) as SponsorMentionOut[],
  })

  const data = detailQuery.data

  useEffect(() => {
    if (!data) {
      return
    }
    if (day > data.duration_days) {
      setDay(1)
    }
  }, [data, day])

  useEffect(() => {
    const t = window.setInterval(() => setTick((x) => x + 1), 1000)
    return () => window.clearInterval(t)
  }, [])

  const activeSession = useMemo(
    () => data?.active_broadcasts.find((b) => b.day_index === day),
    [data, day, tick],
  )

  const elapsedSec = useMemo(() => {
    if (!activeSession) {
      return 0
    }
    const start = new Date(activeSession.started_at).getTime()
    return Math.floor((Date.now() - start) / 1000)
  }, [activeSession, tick])

  const takenDays = useMemo(
    () => new Set((data?.day_assignments ?? []).map((a) => a.day_index)),
    [data?.day_assignments],
  )

  const freeDays = useMemo(() => {
    if (!data) {
      return [] as number[]
    }
    return Array.from({ length: data.duration_days }, (_, i) => i + 1).filter((d) => !takenDays.has(d))
  }, [data, takenDays])

  const myDayIndices = useMemo(
    () =>
      (data?.day_assignments ?? [])
        .filter((a) => a.operator_id === user?.id)
        .map((a) => a.day_index)
        .sort((a, b) => a - b),
    [data?.day_assignments, user?.id],
  )

  const operatorForSelectedDay = useMemo(() => {
    const a = (data?.day_assignments ?? []).find((x) => x.day_index === day)
    return a?.operator_id
  }, [data?.day_assignments, day])

  const foreignLock = Boolean(
    user?.role !== 'SUPERADMIN' && operatorForSelectedDay && operatorForSelectedDay !== user?.id,
  )

  const iHaveLock = Boolean(user && (user.role === 'SUPERADMIN' || myDayIndices.length > 0))

  const iHaveThisDay = Boolean(
    user?.role === 'SUPERADMIN' || (operatorForSelectedDay != null && operatorForSelectedDay === user?.id),
  )

  const canRealignBroadcast = useMemo(
    () =>
      Boolean(
        activeSession &&
          (user?.role === 'SUPERADMIN' || (user?.role === 'OPERATOR' && !foreignLock && iHaveThisDay)),
      ),
    [activeSession, user?.role, foreignLock, iHaveThisDay],
  )

  const canTakeLock = useMemo(() => {
    if (!data || !user) {
      return false
    }
    if (user.role === 'SUPERADMIN') {
      return true
    }
    return freeDays.length > 0
  }, [data, user, freeDays.length])

  const [lockModalOpen, setLockModalOpen] = useState(false)
  const [lockDayPick, setLockDayPick] = useState<number[]>([])

  const selectedDayRow = useMemo(() => data?.days.find((d) => d.day_index === day), [data, day])

  const [streamCredsVisible, setStreamCredsVisible] = useState(true)
  const lastIdleDismissAtRef = useRef(0)
  const [idleDismissVersion, setIdleDismissVersion] = useState(0)

  const orderedMentionsForPlan = useMemo(() => {
    const list = [...(mentionsQuery.data ?? [])]
    list.sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime())
    return list
  }, [mentionsQuery.data])

  const lastMentionMs = useMemo(() => {
    const list = mentionsQuery.data ?? []
    if (!list.length) {
      return null
    }
    return Math.max(...list.map((m) => new Date(m.created_at).getTime()))
  }, [mentionsQuery.data])

  useEffect(() => {
    lastIdleDismissAtRef.current = 0
    setIdleDismissVersion((v) => v + 1)
  }, [activeSession?.id, day])

  const idleAnchorMs = useMemo(() => {
    if (!activeSession) {
      return null
    }
    const t0 = new Date(activeSession.started_at).getTime()
    const dismiss = lastIdleDismissAtRef.current
    const parts = [t0, dismiss]
    if (lastMentionMs) {
      parts.push(lastMentionMs)
    }
    return Math.max(...parts)
  }, [activeSession, lastMentionMs, idleDismissVersion, tick])

  const showIdleReminder = useMemo(() => {
    if (!idleAnchorMs || !activeSession || foreignLock || !iHaveThisDay) {
      return false
    }
    if (user?.role !== 'OPERATOR') {
      return false
    }
    return Date.now() - idleAnchorMs >= IDLE_REMINDER_MS
  }, [idleAnchorMs, activeSession, foreignLock, iHaveThisDay, tick, user?.role])

  const handleIdleReminderDismiss = () => {
    lastIdleDismissAtRef.current = Date.now()
    setIdleDismissVersion((v) => v + 1)
  }

  const adjustTotalSec = useMemo(
    () => Math.max(0, adjustMinutes * 60 + adjustSecondsPart),
    [adjustMinutes, adjustSecondsPart],
  )

  const lockMut = useMutation({
    mutationFn: async (day_indices: number[]) => {
      await apiFetch(`/stream-events/${streamId}/lock`, {
        method: 'POST',
        body: JSON.stringify({ day_indices }),
      })
    },
    onSuccess: async () => {
      message.success('Дни назначены')
      setLockModalOpen(false)
      await qc.invalidateQueries({ queryKey: ['stream', streamId] })
    },
    onError: (e: Error) => message.error(e.message),
  })

  const unlockMut = useMutation({
    mutationFn: async () => {
      await apiFetch(`/stream-events/${streamId}/unlock`, { method: 'POST', body: '{}' })
    },
    onSuccess: async () => {
      message.success('Снято с работы')
      await qc.invalidateQueries({ queryKey: ['stream', streamId] })
    },
    onError: (e: Error) => message.error(e.message),
  })

  const startMut = useMutation({
    mutationFn: async () => {
      await apiFetch(`/stream-events/${streamId}/days/${day}/broadcast/start`, { method: 'POST' })
    },
    onSuccess: async () => {
      message.success('Эфир начат (время старта зафиксировано)')
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

  const downloadOneLogoMut = useMutation({
    mutationFn: async (logoId: string) => {
      const { blob, filename } = await fetchAuthorizedBlob(`/stream-events/${streamId}/logos/${logoId}/file`)
      triggerBlobDownload(blob, filename)
    },
    onError: (e: Error) => message.error(e.message),
  })

  const stopMut = useMutation({
    mutationFn: async () => {
      await apiFetch(`/stream-events/${streamId}/days/${day}/broadcast/stop`, { method: 'POST' })
    },
    onSuccess: async () => {
      message.success('Эфир остановлен')
      await qc.invalidateQueries({ queryKey: ['stream', streamId] })
      await qc.invalidateQueries({ queryKey: ['mentions', streamId, day] })
    },
    onError: (e: Error) => message.error(e.message),
  })

  const mentionMut = useMutation({
    mutationFn: async (sessionId: string) => {
      await apiFetch(`/broadcast-sessions/${sessionId}/mentions`, { method: 'POST', body: '{}' })
    },
    onSuccess: async () => {
      message.success('Упоминание добавлено')
      await qc.invalidateQueries({ queryKey: ['mentions', streamId, day] })
    },
    onError: (e: Error) => message.error(e.message),
  })

  const adjustMut = useMutation({
    mutationFn: async (payload: { id: string; sec: number }) => {
      await apiFetch(`/sponsor-mentions/${payload.id}`, {
        method: 'PATCH',
        body: JSON.stringify({ adjusted_offset_sec: payload.sec }),
      })
    },
    onSuccess: async () => {
      message.success('Таймкод обновлён')
      setAdjustTarget(null)
      await qc.invalidateQueries({ queryKey: ['mentions', streamId, day] })
    },
    onError: (e: Error) => message.error(e.message),
  })

  const handleAddMention = () => {
    if (!activeSession) {
      message.warning('Сначала начните эфир')
      return
    }
    if (foreignLock) {
      message.warning('Мероприятие занято другим оператором')
      return
    }
    mentionMut.mutate(activeSession.id)
  }

  const handleStart = () => {
    if (foreignLock) {
      message.warning('Мероприятие занято другим оператором')
      return
    }
    if (!iHaveThisDay) {
      message.warning('Сначала возьмите этот день в работу')
      return
    }
    startMut.mutate()
  }

  const handleStop = () => {
    modal.confirm({
      title: 'Остановить эфир?',
      content: 'Новые упоминания для этого дня будут невозможны до нового старта.',
      okText: 'Остановить',
      cancelText: 'Отмена',
      onOk: async () => {
        await stopMut.mutateAsync()
      },
    })
  }

  const dayOptions =
    data?.days.map((d) => ({ label: `День ${d.day_index}`, value: d.day_index })) ??
    Array.from({ length: 5 }, (_, i) => ({ label: `День ${i + 1}`, value: i + 1 }))

  return (
    <AppLayout
      nav={
        <Space direction={isComfortable ? 'horizontal' : 'vertical'} size="small" style={{ width: '100%' }}>
          <Link to="/operator">
            <Button type="link" icon={<ArrowLeftOutlined />} style={{ paddingInline: 0 }}>
              К списку
            </Button>
          </Link>
          <Typography.Text type="secondary" style={{ fontSize: isComfortable ? undefined : 13 }}>
            Пульт оператора
          </Typography.Text>
        </Space>
      }
    >
      {!data ? (
        <Typography.Paragraph>Загрузка…</Typography.Paragraph>
      ) : (
        <Space direction="vertical" size={16} style={{ width: '100%' }}>
          <div>
            <Typography.Title level={3} style={{ marginBottom: 4 }}>
              {data.title}
            </Typography.Title>
            <Typography.Text type="secondary">
              Старт: {formatDateRu(data.start_date)} · {data.duration_days} дн. · Москва
              {wsViewers != null ? (
                <>
                  {' '}
                  · Сейчас с пультом: {wsViewers}
                </>
              ) : null}
            </Typography.Text>
          </div>

          <Card size="small" style={{ borderColor: '#e2e8f0', background: '#ffffff' }}>
            <Space direction={isComfortable ? 'horizontal' : 'vertical'} size="middle" style={{ width: '100%' }}>
              <Typography.Text>Статус (день {day}):</Typography.Text>
              {user?.role === 'SUPERADMIN' ? (
                <Badge status="warning" text="Суперадмин — полный доступ" />
              ) : foreignLock ? (
                <Badge status="error" text="Этот день назначен другому оператору" />
              ) : operatorForSelectedDay === user?.id ? (
                <Badge status="processing" text="Этот день у вас" />
              ) : freeDays.length > 0 ? (
                <Badge status="success" text="Есть свободные дни — возьмите в работу" />
              ) : (
                <Badge status="default" text="Все дни распределены" />
              )}
              <Space
                direction={isComfortable ? 'horizontal' : 'vertical'}
                style={{ width: isComfortable ? 'auto' : '100%' }}
                size="middle"
              >
                <Button
                  type={canTakeLock ? 'primary' : 'default'}
                  disabled={!canTakeLock}
                  loading={lockMut.isPending}
                  onClick={() => {
                    if (freeDays.length === 0) {
                      message.info('Нет свободных дней для назначения')
                      return
                    }
                    setLockDayPick(freeDays)
                    setLockModalOpen(true)
                  }}
                  block={!isComfortable}
                  size="large"
                >
                  Взять в работу
                </Button>
                <Button
                  danger
                  disabled={!iHaveLock}
                  loading={unlockMut.isPending}
                  onClick={() => unlockMut.mutate()}
                  block={!isComfortable}
                  size="large"
                >
                  Снять с работы
                </Button>
              </Space>
            </Space>
            {data.day_assignments.length > 0 ? (
              <Typography.Paragraph type="secondary" style={{ marginBottom: 0, marginTop: 12, fontSize: 12 }}>
                Назначения:{' '}
                {[...data.day_assignments]
                  .sort((a, b) => a.day_index - b.day_index)
                  .map((a) => `день ${a.day_index} — ${a.operator_display_name || a.operator_email}`)
                  .join('; ')}
              </Typography.Paragraph>
            ) : null}
          </Card>

          <Card size="small" style={{ borderColor: '#e2e8f0', background: '#ffffff' }} title="Материалы и логотипы">
            <Space direction="vertical" size={12} style={{ width: '100%' }}>
              <div>
                <Typography.Text type="secondary" style={{ display: 'block', marginBottom: 6 }}>
                  Ссылка на материалы (контент)
                </Typography.Text>
                {data.content_url ? (
                  <Space wrap align="start">
                    <Tooltip title="Нажмите, чтобы скопировать в буфер обмена">
                      <Typography.Text
                        role="button"
                        tabIndex={0}
                        style={{
                          wordBreak: 'break-all',
                          cursor: 'pointer',
                          color: '#1677ff',
                          textDecoration: 'underline',
                        }}
                        onClick={() => void handleCopyLinkField(data.content_url as string)}
                        onKeyDown={(e) => {
                          if (e.key === 'Enter' || e.key === ' ') {
                            e.preventDefault()
                            void handleCopyLinkField(data.content_url as string)
                          }
                        }}
                        aria-label="Скопировать ссылку на материалы"
                      >
                        {data.content_url}
                      </Typography.Text>
                    </Tooltip>
                    <Button
                      size="small"
                      icon={<CopyOutlined />}
                      onClick={() => void handleCopyLinkField(data.content_url as string)}
                    >
                      Копировать
                    </Button>
                    <Button
                      size="small"
                      icon={<LinkOutlined />}
                      onClick={() =>
                        window.open(data.content_url as string, '_blank', 'noopener,noreferrer')
                      }
                    >
                      Открыть
                    </Button>
                  </Space>
                ) : (
                  <Typography.Text type="secondary">Не указана</Typography.Text>
                )}
              </div>
              <Divider style={{ margin: '8px 0' }} />
              <div>
                <Space wrap style={{ marginBottom: 8 }}>
                  <Typography.Text strong>Логотипы</Typography.Text>
                  <Button
                    size="small"
                    icon={<FileZipOutlined />}
                    disabled={!(data.logos ?? []).length}
                    loading={downloadZipMut.isPending}
                    onClick={() => downloadZipMut.mutate()}
                  >
                    Скачать все (ZIP)
                  </Button>
                </Space>
                {!(data.logos ?? []).length ? (
                  <Typography.Text type="secondary">Нет прикреплённых логотипов</Typography.Text>
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
                              style={{ maxHeight: 100, objectFit: 'contain', padding: 8 }}
                            />
                          }
                        >
                          <Typography.Text ellipsis style={{ fontSize: 12 }} title={lg.filename_original}>
                            {lg.filename_original}
                          </Typography.Text>
                          <Button
                            size="small"
                            block
                            style={{ marginTop: 8 }}
                            icon={<DownloadOutlined />}
                            loading={downloadOneLogoMut.isPending}
                            onClick={() => downloadOneLogoMut.mutate(lg.id)}
                          >
                            Скачать
                          </Button>
                        </Card>
                      </Col>
                    ))}
                  </Row>
                )}
              </div>
            </Space>
          </Card>

          <Modal
            title="Какие дни берёте в работу?"
            open={lockModalOpen}
            onCancel={() => setLockModalOpen(false)}
            okText="Подтвердить"
            onOk={() => {
              if (lockDayPick.length === 0) {
                message.warning('Выберите хотя бы один день')
                return Promise.reject(new Error('no days'))
              }
              return lockMut.mutateAsync(lockDayPick)
            }}
            confirmLoading={lockMut.isPending}
          >
            <Checkbox.Group
              style={{ display: 'flex', flexDirection: 'column', gap: 8 }}
              options={freeDays.map((d) => ({ label: `День ${d}`, value: d }))}
              value={lockDayPick}
              onChange={(v) => setLockDayPick(v as number[])}
            />
          </Modal>

          <Row gutter={[16, 16]}>
            <Col xs={24} lg={10}>
              <Card
                title="Управление эфиром"
                style={{ borderColor: '#e2e8f0', background: '#ffffff' }}
                styles={{ header: { borderBottom: '1px solid #e2e8f0' } }}
              >
                <Space direction="vertical" size={16} style={{ width: '100%' }}>
                  <div>
                    <Typography.Text type="secondary">День</Typography.Text>
                    <Select
                      style={{ width: '100%', marginTop: 8 }}
                      value={day}
                      options={dayOptions.filter((o) => o.value <= data.duration_days)}
                      onChange={(v) => setDay(v)}
                    />
                    {selectedDayRow ? (
                      <>
                        <div
                          style={{
                            display: 'flex',
                            justifyContent: 'space-between',
                            alignItems: 'center',
                            marginTop: 14,
                            gap: 8,
                            flexWrap: 'wrap',
                          }}
                        >
                          <Typography.Text style={{ color: '#0f172a' }}>
                            Параметры дня {day}
                          </Typography.Text>
                          <Button
                            type="link"
                            size="small"
                            onClick={() => setStreamCredsVisible((v) => !v)}
                            aria-expanded={streamCredsVisible}
                            aria-label={streamCredsVisible ? 'Скрыть параметры трансляции' : 'Показать параметры трансляции'}
                          >
                            {streamCredsVisible ? 'Скрыть' : 'Показать'}
                          </Button>
                        </div>
                        {streamCredsVisible ? (
                          <div
                            style={{
                              marginTop: 10,
                              padding: 12,
                              borderRadius: 10,
                              border: '1px solid #e2e8f0',
                              background: '#f8fafc',
                            }}
                          >
                            {(
                              [
                                {
                                  label: 'Ссылка на трансляцию',
                                  value: selectedDayRow.stream_url,
                                },
                                {
                                  label: 'URL сервера трансляции',
                                  value: selectedDayRow.server_url,
                                },
                                {
                                  label: 'Ключ трансляции',
                                  value: selectedDayRow.stream_key,
                                },
                              ] as const
                            ).map((row, idx, arr) => (
                              <div
                                key={row.label}
                                style={{ marginBottom: idx < arr.length - 1 ? 12 : 0 }}
                              >
                                <Typography.Text type="secondary" style={{ fontSize: 12, display: 'block' }}>
                                  {row.label}
                                </Typography.Text>
                                <Tooltip
                                  title={row.value ? 'Нажмите, чтобы скопировать в буфер обмена' : undefined}
                                >
                                  <Typography.Paragraph
                                    role={row.value ? 'button' : undefined}
                                    tabIndex={row.value ? 0 : undefined}
                                    style={{
                                      marginBottom: 0,
                                      wordBreak: 'break-all',
                                      cursor: row.value ? 'pointer' : 'default',
                                      color: row.value ? '#1677ff' : undefined,
                                      textDecoration: row.value ? 'underline' : undefined,
                                    }}
                                    onClick={() => row.value && void handleCopyLinkField(row.value)}
                                    onKeyDown={(e) => {
                                      if (!row.value) {
                                        return
                                      }
                                      if (e.key === 'Enter' || e.key === ' ') {
                                        e.preventDefault()
                                        void handleCopyLinkField(row.value)
                                      }
                                    }}
                                    aria-label={
                                      row.value ? `Скопировать: ${row.label}` : undefined
                                    }
                                  >
                                    {row.value || '—'}
                                  </Typography.Paragraph>
                                </Tooltip>
                              </div>
                            ))}
                          </div>
                        ) : null}
                      </>
                    ) : null}
                  </div>
                  <Divider style={{ margin: '4px 0' }} />
                  <div>
                    <Typography.Text strong style={{ display: 'block', marginBottom: 8 }}>
                      Чек-лист перед эфиром · день {day}
                    </Typography.Text>
                    <Space direction="vertical" size="small" style={{ width: '100%' }}>
                      <Checkbox
                        checked={checklistQuery.data?.picture_exposure_ok ?? false}
                        disabled={checklistMut.isPending || checklistQuery.isLoading}
                        onChange={(e) => checklistMut.mutate({ picture_exposure_ok: e.target.checked })}
                      >
                        Картинка, баланс белого и экспозиция (чтобы не в норме, но и не слепило)
                      </Checkbox>
                      <Checkbox
                        checked={checklistQuery.data?.judges_stream_ok ?? false}
                        disabled={checklistMut.isPending || checklistQuery.isLoading}
                        onChange={(e) => checklistMut.mutate({ judges_stream_ok: e.target.checked })}
                      >
                        Поток судьям
                      </Checkbox>
                      <Checkbox
                        checked={checklistQuery.data?.splitter_socket_ok ?? false}
                        disabled={checklistMut.isPending || checklistQuery.isLoading}
                        onChange={(e) => checklistMut.mutate({ splitter_socket_ok: e.target.checked })}
                      >
                        Сплиттер и сокет
                      </Checkbox>
                      <Checkbox
                        checked={checklistQuery.data?.key_stream_started_ok ?? false}
                        disabled={checklistMut.isPending || checklistQuery.isLoading}
                        onChange={(e) => checklistMut.mutate({ key_stream_started_ok: e.target.checked })}
                      >
                        Ключ скопирован, поток запущен
                      </Checkbox>
                      <Checkbox
                        checked={checklistQuery.data?.kick_ok ?? false}
                        disabled={checklistMut.isPending || checklistQuery.isLoading}
                        onChange={(e) => checklistMut.mutate({ kick_ok: e.target.checked })}
                      >
                        Кик стоит, у тебя тоже
                      </Checkbox>
                      <Checkbox
                        checked={checklistQuery.data?.mentions_four_ok ?? false}
                        disabled={checklistMut.isPending || checklistQuery.isLoading}
                        onChange={(e) => checklistMut.mutate({ mentions_four_ok: e.target.checked })}
                      >
                        4 упоминания
                      </Checkbox>
                    </Space>
                  </div>
                  <div
                    style={{
                      padding: 16,
                      borderRadius: 12,
                      border: '1px solid #e2e8f0',
                      background: '#f8fafc',
                      textAlign: 'center',
                    }}
                  >
                    <Typography.Text type="secondary">Таймер эфира</Typography.Text>
                    <Typography.Title level={2} style={{ margin: '8px 0 0', letterSpacing: 2 }}>
                      {activeSession ? formatElapsed(elapsedSec) : '— : — : —'}
                    </Typography.Title>
                  </div>
                  <Button
                    type="primary"
                    size="large"
                    block
                    icon={<PlayCircleOutlined />}
                    disabled={Boolean(activeSession) || foreignLock || !iHaveThisDay}
                    loading={startMut.isPending}
                    onClick={() => handleStart()}
                  >
                    Начать эфир
                  </Button>
                  <Button
                    size="large"
                    block
                    danger
                    icon={<StopOutlined />}
                    disabled={!activeSession || foreignLock}
                    loading={stopMut.isPending}
                    onClick={() => handleStop()}
                  >
                    Остановить эфир
                  </Button>
                  {activeSession ? (
                    <BroadcastActualStartPanel
                      streamId={streamId}
                      dayIndex={day}
                      startedAtIso={activeSession.started_at}
                      disabled={!canRealignBroadcast}
                    />
                  ) : null}
                  <Button
                    type="default"
                    size="large"
                    block
                    icon={<PlusOutlined />}
                    disabled={!activeSession || foreignLock}
                    loading={mentionMut.isPending}
                    onClick={() => handleAddMention()}
                  >
                    Добавить упоминание
                  </Button>
                  <div
                    style={{
                      padding: 12,
                      borderRadius: 10,
                      border: '1px solid #e2e8f0',
                      background: '#f8fafc',
                    }}
                  >
                    <Typography.Text strong style={{ display: 'block', marginBottom: 10 }}>
                      План: 4 упоминания за эфир
                    </Typography.Text>
                    <Typography.Paragraph type="secondary" style={{ fontSize: 12, marginBottom: 10 }}>
                      Добавляйте по порядку: начало → две середины → конец. Ниже отмечается, какие из четырёх шагов уже
                      есть.
                    </Typography.Paragraph>
                    {MENTION_SLOT_LABELS.map((label, i) => {
                      const done = Boolean(orderedMentionsForPlan[i])
                      return (
                        <div
                          key={label}
                          style={{
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'space-between',
                            gap: 8,
                            padding: '8px 0',
                            borderTop: i === 0 ? undefined : '1px solid #e2e8f0',
                          }}
                        >
                          <Typography.Text style={{ fontSize: 13 }}>
                            {i + 1}. {label}
                          </Typography.Text>
                          {done ? (
                            <CheckOutlined style={{ color: '#52c41a', fontSize: 16 }} aria-label="Отмечено" />
                          ) : (
                            <Typography.Text type="secondary" style={{ fontSize: 12 }}>
                              нет
                            </Typography.Text>
                          )}
                        </div>
                      )
                    })}
                  </div>
                </Space>
              </Card>
            </Col>
            <Col xs={24} lg={14}>
              <Card
                title="Упоминания"
                style={{ borderColor: '#e2e8f0', background: '#ffffff' }}
                styles={{ header: { borderBottom: '1px solid #e2e8f0' } }}
              >
                <List
                  itemLayout={isComfortable ? 'horizontal' : 'vertical'}
                  loading={mentionsQuery.isLoading}
                  dataSource={mentionsQuery.data ?? []}
                  locale={{ emptyText: 'Пока нет упоминаний' }}
                  renderItem={(item) => (
                    <List.Item
                      actions={[
                        <Button
                          key="adj"
                          type={isComfortable ? 'link' : 'default'}
                          disabled={foreignLock || !iHaveThisDay}
                          block={!isComfortable}
                          size={isComfortable ? 'middle' : 'large'}
                          onClick={() => {
                            setAdjustTarget(item)
                            const t = Math.max(0, item.adjusted_offset_sec)
                            setAdjustMinutes(Math.floor(t / 60))
                            setAdjustSecondsPart(t % 60)
                          }}
                        >
                          Корректировка
                        </Button>,
                      ]}
                    >
                      <List.Item.Meta
                        title={
                          <Space>
                            <Typography.Text strong>{item.adjusted_timecode}</Typography.Text>
                            {item.is_adjusted ? <Badge status="warning" text="Скорректировано" /> : null}
                          </Space>
                        }
                        description={
                          <Space direction="vertical" size={0}>
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
                                    Запись: {formatDateTimeRu(a.created_at)} · {formatElapsed(a.previous_adjusted_sec)}{' '}
                                    → {formatElapsed(a.new_adjusted_sec)}
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
              </Card>
            </Col>
          </Row>
        </Space>
      )}

      <Modal
        title="Корректировка таймкода"
        open={Boolean(adjustTarget)}
        okText="Сохранить"
        cancelText="Отмена"
        confirmLoading={adjustMut.isPending}
        onCancel={() => setAdjustTarget(null)}
        onOk={async () => {
          if (!adjustTarget) {
            return
          }
          await adjustMut.mutateAsync({ id: adjustTarget.id, sec: adjustTotalSec })
        }}
      >
        <Typography.Paragraph type="secondary" style={{ marginBottom: 12 }}>
          Смещение от старта эфира: введите минуты и секунды (секунды — от 0 до 59).
        </Typography.Paragraph>
        <div
          style={{
            border: '1px solid #e2e8f0',
            borderRadius: 10,
            overflow: 'hidden',
            background: '#f8fafc',
          }}
        >
          <Row
            wrap={false}
            style={{
              borderBottom: '1px solid #e2e8f0',
              background: '#f1f5f9',
              color: '#64748b',
              fontSize: 13,
              fontWeight: 500,
            }}
          >
            <Col flex="1" style={{ padding: '10px 12px' }}>
              Минуты
            </Col>
            <Col
              flex="1"
              style={{
                padding: '10px 12px',
                borderLeft: '1px solid #e2e8f0',
              }}
            >
              Секунды
            </Col>
          </Row>
          <Row wrap={false}>
            <Col flex="1" style={{ padding: 12 }}>
              <InputNumber
                min={0}
                max={99999}
                step={1}
                controls
                size="large"
                style={{ width: '100%' }}
                value={adjustMinutes}
                onChange={(v) => setAdjustMinutes(Math.max(0, Math.floor(Number(v ?? 0))))}
                aria-label="Минуты от старта эфира"
              />
            </Col>
            <Col
              flex="1"
              style={{
                padding: 12,
                borderLeft: '1px solid #e2e8f0',
              }}
            >
              <InputNumber
                min={0}
                max={59}
                step={1}
                controls
                size="large"
                style={{ width: '100%' }}
                value={adjustSecondsPart}
                onChange={(v) => setAdjustSecondsPart(Math.min(59, Math.max(0, Math.floor(Number(v ?? 0)))))}
                aria-label="Секунды от старта эфира, 0–59"
              />
            </Col>
          </Row>
        </div>
        <Typography.Paragraph type="secondary" style={{ marginTop: 14, marginBottom: 0 }}>
          Итого от старта эфира:{' '}
          <Typography.Text strong style={{ color: '#0f172a' }}>
            {formatElapsed(adjustTotalSec)}
          </Typography.Text>
          <Typography.Text type="secondary" style={{ fontSize: 12, marginLeft: 8 }}>
            ({adjustTotalSec} с)
          </Typography.Text>
        </Typography.Paragraph>
      </Modal>

      {showIdleReminder ? (
        <div
          role="alertdialog"
          aria-modal="true"
          aria-labelledby="idle-reminder-title"
          style={{
            position: 'fixed',
            inset: 0,
            zIndex: 1100,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: 24,
            paddingTop: 'max(24px, env(safe-area-inset-top))',
            paddingBottom: 'max(24px, env(safe-area-inset-bottom))',
            background: 'rgba(7, 11, 16, 0.97)',
            backdropFilter: 'blur(6px)',
          }}
        >
          <div style={{ maxWidth: 440, textAlign: 'center' }}>
            <Typography.Title level={3} id="idle-reminder-title" style={{ color: '#0f172a' }}>
              Не забудьте про напоминалки
            </Typography.Title>
            <Typography.Paragraph type="secondary" style={{ marginBottom: 24, fontSize: 15 }}>
              Прошло больше двух часов с последнего упоминания (или с того момента, как вы закрыли это сообщение).
              Проверьте план из четырёх отметок и спонсорские вставки.
            </Typography.Paragraph>
            <Button type="primary" size="large" block onClick={handleIdleReminderDismiss}>
              Понятно, скрыть
            </Button>
          </div>
        </div>
      ) : null}
    </AppLayout>
  )
}
