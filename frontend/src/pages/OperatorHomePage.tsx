import { PlayCircleOutlined } from '@ant-design/icons'
import { App as AntApp, Button, Card, Col, Empty, Row, Space, Tag, Typography } from 'antd'
import { useQuery } from '@tanstack/react-query'
import dayjs from 'dayjs'
import timezone from 'dayjs/plugin/timezone'
import utc from 'dayjs/plugin/utc'
import React, { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'

import type { StreamEventListOut } from '@/api/types'
import { apiFetch } from '@/api/client'
import { AppLayout } from '@/layouts/AppLayout'
import { formatDateRu } from '@/utils/datetime'

dayjs.extend(utc)
dayjs.extend(timezone)

const MOSCOW_TZ = 'Europe/Moscow'
/** Сколько дней после окончания турнир ещё доступен в блоке «Прошедшие» */
const PAST_RETENTION_DAYS = 14
/** Горизонт будущих турниров в основном списке */
const UPCOMING_HORIZON_DAYS = 7

const endedDaysStatusLabel = (dayIndices: number[] | undefined) => {
  const list = (dayIndices ?? []).filter((d) => Number.isInteger(d)).sort((a, b) => a - b)
  if (list.length === 0) {
    return 'Есть завершенные эфиры'
  }
  if (list.length === 1) {
    return `Завершен день ${list[0]}`
  }
  return `Завершены дни ${list.join(', ')}`
}

const eventEndDate = (ev: StreamEventListOut) =>
  dayjs.tz(ev.start_date, MOSCOW_TZ).startOf('day').add(ev.duration_days - 1, 'day')

const EventCard: React.FC<{
  ev: StreamEventListOut
  isLoading: boolean
  past?: boolean
  onBlockedClick: (ev: StreamEventListOut) => void
}> = ({ ev, isLoading, past = false, onBlockedClick }) => {
  const blocked = ev.has_slot_for_me === false
  return (
    <Col xs={24} md={12} lg={8}>
      <Link
        to={`/operator/${ev.id}`}
        onClick={(e) => {
          if (blocked) {
            e.preventDefault()
            onBlockedClick(ev)
          }
        }}
      >
        <Card
          hoverable={!blocked}
          loading={isLoading}
          style={{
            opacity: blocked || past ? 0.55 : 1,
            borderColor: '#e2e8f0',
            background: '#ffffff',
          }}
        >
          <Space direction="vertical" size={8} style={{ width: '100%' }}>
            <Typography.Title level={5} style={{ margin: 0, color: '#0f172a' }}>
              {ev.title}
            </Typography.Title>
            <Typography.Text type="secondary">
              Старт: {formatDateRu(ev.start_date)} · {ev.duration_days} дн.
            </Typography.Text>
            <Space wrap>
              {past ? <Tag>Прошедший</Tag> : null}
              {ev.has_active_broadcast ? (
                <Tag color="green">Эфир</Tag>
              ) : ev.has_ended_broadcast ? (
                <Tag color="orange">{endedDaysStatusLabel(ev.ended_day_indices)}</Tag>
              ) : (
                <Tag>Нет эфира</Tag>
              )}
              {blocked ? (
                <Tag color="red">Нет свободных дней</Tag>
              ) : ev.assignment_summary ? (
                <Tag color="blue">{ev.assignment_summary}</Tag>
              ) : (
                <Tag>Свободные дни</Tag>
              )}
            </Space>
            <Typography.Link>
              <PlayCircleOutlined /> Открыть пульт
            </Typography.Link>
          </Space>
        </Card>
      </Link>
    </Col>
  )
}

export const OperatorHomePage: React.FC = () => {
  const { message } = AntApp.useApp()
  const [showPast, setShowPast] = useState(false)

  const { data, isLoading } = useQuery({
    queryKey: ['streams'],
    queryFn: async () => (await apiFetch('/stream-events')) as StreamEventListOut[],
  })

  const handleCardClick = (ev: StreamEventListOut) => {
    if (!ev.has_slot_for_me) {
      message.warning('Все дни этого мероприятия уже распределены между операторами')
    }
  }

  const { currentEvents, pastEvents } = useMemo(() => {
    const today = dayjs().tz(MOSCOW_TZ).startOf('day')
    const upcomingLimit = today.add(UPCOMING_HORIZON_DAYS, 'day').endOf('day')
    const pastCutoff = today.subtract(PAST_RETENTION_DAYS, 'day')

    const current: StreamEventListOut[] = []
    const past: StreamEventListOut[] = []

    for (const ev of data ?? []) {
      const start = dayjs.tz(ev.start_date, MOSCOW_TZ).startOf('day')
      const end = eventEndDate(ev)
      // Прошедший только со следующего календарного дня после последнего дня турнира
      if (today.isAfter(end, 'day')) {
        if (!end.isBefore(pastCutoff, 'day')) {
          past.push(ev)
        }
        continue
      }
      if (start.isAfter(upcomingLimit)) {
        continue
      }
      current.push(ev)
    }

    current.sort((a, b) => a.start_date.localeCompare(b.start_date) || a.title.localeCompare(b.title))
    past.sort((a, b) => {
      const endA = eventEndDate(a).valueOf()
      const endB = eventEndDate(b).valueOf()
      return endB - endA || b.start_date.localeCompare(a.start_date)
    })

    return { currentEvents: current, pastEvents: past }
  }, [data])

  const handleTogglePast = () => {
    setShowPast((v) => !v)
  }

  const isEmpty = !isLoading && currentEvents.length === 0 && pastEvents.length === 0

  return (
    <AppLayout
      nav={
        <Typography.Text type="secondary" style={{ fontSize: 13 }}>
          Оператор
        </Typography.Text>
      }
    >
      <Typography.Title level={3} style={{ marginTop: 0 }}>
        Мероприятия
      </Typography.Title>
      <Typography.Paragraph type="secondary">
        Выберите мероприятие. Можно взять свободные дни турнира; если все дни заняты — карточка приглушена.
      </Typography.Paragraph>

      {pastEvents.length > 0 ? (
        <Space direction="vertical" size={12} style={{ width: '100%', marginBottom: 16 }}>
          <Button type="default" onClick={handleTogglePast} aria-expanded={showPast} aria-label="Показать прошедшие турниры">
            {showPast ? 'Скрыть прошедшие' : `Показать прошедшие (${pastEvents.length})`}
          </Button>
          {showPast ? (
            <Row gutter={[16, 16]}>
              {pastEvents.map((ev) => (
                <EventCard key={ev.id} ev={ev} isLoading={isLoading} past onBlockedClick={handleCardClick} />
              ))}
            </Row>
          ) : null}
        </Space>
      ) : null}

      {isEmpty ? (
        <Empty description="Нет мероприятий" />
      ) : currentEvents.length === 0 && !isLoading ? (
        <Empty description="Нет текущих и ближайших мероприятий" />
      ) : (
        <Row gutter={[16, 16]}>
          {currentEvents.map((ev) => (
            <EventCard key={ev.id} ev={ev} isLoading={isLoading} onBlockedClick={handleCardClick} />
          ))}
        </Row>
      )}
    </AppLayout>
  )
}
