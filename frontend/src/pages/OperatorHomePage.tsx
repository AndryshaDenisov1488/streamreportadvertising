import { App as AntApp, Card, Col, Empty, Row, Space, Tag, Typography } from 'antd'
import { useQuery } from '@tanstack/react-query'
import React, { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'

import type { StreamEventListOut } from '@/api/types'
import { apiFetch } from '@/api/client'
import { StreamEventsFilterBar } from '@/components/StreamEventsFilterBar'
import { AppLayout } from '@/layouts/AppLayout'
import { formatDateRu } from '@/utils/datetime'
import {
  filterStreamEvents,
  type StreamCategory,
} from '@/utils/streamEventFilters'
import {
  currentSeasonYear,
  rangeForSeasonFilter,
  seasonsFromEvents,
  type SeasonFilter,
} from '@/utils/season'

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

export const OperatorHomePage: React.FC = () => {
  const { message } = AntApp.useApp()
  const [seasonFilter, setSeasonFilter] = useState<SeasonFilter>(() => currentSeasonYear())
  const [category, setCategory] = useState<StreamCategory>('all')

  const { data, isLoading } = useQuery({
    queryKey: ['streams'],
    queryFn: async () => (await apiFetch('/stream-events')) as StreamEventListOut[],
  })

  const seasonsAvailable = useMemo(
    () => seasonsFromEvents((data ?? []).map((ev) => ev.start_date)),
    [data],
  )

  const range = useMemo(() => rangeForSeasonFilter(seasonFilter), [seasonFilter])

  const visibleEvents = useMemo(
    () =>
      filterStreamEvents(data ?? [], {
        rangeStart: range[0],
        rangeEnd: range[1],
        category,
      }),
    [data, range, category],
  )

  const handleCardClick = (ev: StreamEventListOut) => {
    if (!ev.has_slot_for_me) {
      message.warning('Все дни этого мероприятия уже распределены между операторами')
    }
  }

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
        Ближайшие турниры по выбранному периоду. Можно взять свободные дни; если все дни заняты — карточка
        приглушена.
      </Typography.Paragraph>

      <StreamEventsFilterBar
        seasonFilter={seasonFilter}
        onSeasonFilterChange={setSeasonFilter}
        seasonsAvailable={seasonsAvailable}
        category={category}
        onCategoryChange={setCategory}
        resultCount={visibleEvents.length}
      />

      {!isLoading && visibleEvents.length === 0 ? (
        <Empty description="Нет мероприятий в выбранном периоде" />
      ) : (
        <Row gutter={[16, 16]}>
          {visibleEvents.map((ev) => {
            const blocked = ev.has_slot_for_me === false
            return (
              <Col xs={24} md={12} lg={8} key={ev.id}>
                <Link
                  to={`/operator/${ev.id}`}
                  onClick={(e) => {
                    if (blocked) {
                      e.preventDefault()
                      handleCardClick(ev)
                    }
                  }}
                >
                  <Card
                    hoverable={!blocked}
                    loading={isLoading}
                    style={{
                      opacity: blocked ? 0.55 : 1,
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
                        Открыть пульт
                      </Typography.Link>
                    </Space>
                  </Card>
                </Link>
              </Col>
            )
          })}
        </Row>
      )}
    </AppLayout>
  )
}
