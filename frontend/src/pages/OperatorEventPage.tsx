import { ArrowLeftOutlined, PlusOutlined, PlayCircleOutlined, StopOutlined } from '@ant-design/icons'
import {
  App as AntApp,
  Badge,
  Button,
  Card,
  Col,
  InputNumber,
  List,
  Modal,
  Row,
  Select,
  Space,
  Typography,
} from 'antd'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import React, { useEffect, useMemo, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import type { SponsorMentionOut, StreamEventDetailOut } from '@/api/types'
import { apiFetch } from '@/api/client'
import { useAuth } from '@/auth/AuthContext'
import { useStreamWs } from '@/hooks/useStreamWs'
import { AppLayout } from '@/layouts/AppLayout'

const formatElapsed = (totalSec: number) => {
  const sec = Math.max(0, Math.floor(totalSec))
  const h = Math.floor(sec / 3600)
  const m = Math.floor((sec % 3600) / 60)
  const s = sec % 60
  return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
}

export const OperatorEventPage: React.FC = () => {
  const { id } = useParams()
  const streamId = id as string
  const { user } = useAuth()
  const { message, modal } = AntApp.useApp()
  const qc = useQueryClient()
  const [day, setDay] = useState(1)
  const [tick, setTick] = useState(0)
  const [adjustTarget, setAdjustTarget] = useState<SponsorMentionOut | null>(null)
  const [adjustSec, setAdjustSec] = useState(0)

  const detailQuery = useQuery({
    queryKey: ['stream', streamId],
    enabled: Boolean(streamId),
    queryFn: async () => (await apiFetch(`/stream-events/${streamId}`)) as StreamEventDetailOut,
  })

  useStreamWs(streamId, () => {
    void qc.invalidateQueries({ queryKey: ['stream', streamId] })
    void qc.invalidateQueries({ queryKey: ['mentions', streamId, day] })
  })

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

  const foreignLock = Boolean(
    data?.locked_by_user_id && data.locked_by_user_id !== user?.id && user?.role !== 'SUPERADMIN',
  )
  const iHaveLock = Boolean(user && (user.role === 'SUPERADMIN' || data?.locked_by_user_id === user.id))

  const lockMut = useMutation({
    mutationFn: async () => {
      await apiFetch(`/stream-events/${streamId}/lock`, { method: 'POST', body: '{}' })
    },
    onSuccess: async () => {
      message.success('Событие у вас в работе')
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
      message.warning('Событие занято другим оператором')
      return
    }
    mentionMut.mutate(activeSession.id)
  }

  const handleStart = () => {
    if (foreignLock) {
      message.warning('Событие занято другим оператором')
      return
    }
    if (!iHaveLock) {
      message.warning('Сначала возьмите событие в работу')
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
        <Space>
          <Link to="/operator">
            <Button type="link" icon={<ArrowLeftOutlined />}>
              К списку
            </Button>
          </Link>
          <Typography.Text type="secondary">Пульт оператора</Typography.Text>
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
              Старт: {data.start_date} · {data.duration_days} дн. · Москва
            </Typography.Text>
          </div>

          <Card size="small" style={{ borderColor: '#1f2a3a', background: '#0d1219' }}>
            <Space wrap>
              <Typography.Text>Статус блокировки:</Typography.Text>
              {foreignLock ? (
                <Badge status="error" text="Занято другим оператором" />
              ) : data.locked_by_user_id ? (
                <Badge status="processing" text="У вас в работе" />
              ) : (
                <Badge status="success" text="Свободно" />
              )}
              <Button
                type="primary"
                disabled={foreignLock}
                loading={lockMut.isPending}
                onClick={() => lockMut.mutate()}
              >
                Взять в работу
              </Button>
              <Button danger disabled={!iHaveLock} loading={unlockMut.isPending} onClick={() => unlockMut.mutate()}>
                Снять с работы
              </Button>
            </Space>
          </Card>

          <Row gutter={[16, 16]}>
            <Col xs={24} lg={10}>
              <Card
                title="Управление эфиром"
                style={{ borderColor: '#1f2a3a', background: '#0d1219' }}
                styles={{ header: { borderBottom: '1px solid #1f2a3a' } }}
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
                  </div>
                  <div
                    style={{
                      padding: 16,
                      borderRadius: 12,
                      border: '1px solid #1f2a3a',
                      background: '#0a1018',
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
                    disabled={Boolean(activeSession) || foreignLock || !iHaveLock}
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
                </Space>
              </Card>
            </Col>
            <Col xs={24} lg={14}>
              <Card
                title="Упоминания"
                style={{ borderColor: '#1f2a3a', background: '#0d1219' }}
                styles={{ header: { borderBottom: '1px solid #1f2a3a' } }}
              >
                <List
                  loading={mentionsQuery.isLoading}
                  dataSource={mentionsQuery.data ?? []}
                  locale={{ emptyText: 'Пока нет упоминаний' }}
                  renderItem={(item) => (
                    <List.Item
                      actions={[
                        <Button
                          key="adj"
                          type="link"
                          disabled={foreignLock || !iHaveLock}
                          onClick={() => {
                            setAdjustTarget(item)
                            setAdjustSec(item.adjusted_offset_sec)
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
                              Абсолютное (МСК): {item.absolute_moscow_adjusted}
                            </Typography.Text>
                            <Typography.Text type="secondary" style={{ fontSize: 12 }}>
                              Исходный таймкод: {item.original_timecode}
                            </Typography.Text>
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
          await adjustMut.mutateAsync({ id: adjustTarget.id, sec: adjustSec })
        }}
      >
        <Typography.Paragraph type="secondary">
          Укажите скорректированное смещение в секундах от старта эфира.
        </Typography.Paragraph>
        <InputNumber min={0} style={{ width: '100%' }} value={adjustSec} onChange={(v) => setAdjustSec(Number(v ?? 0))} />
      </Modal>
    </AppLayout>
  )
}
