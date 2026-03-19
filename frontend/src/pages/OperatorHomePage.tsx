import { PlayCircleOutlined } from '@ant-design/icons'
import { App as AntApp, Card, Col, Empty, Row, Space, Tag, Typography } from 'antd'
import { useQuery } from '@tanstack/react-query'
import React from 'react'
import { Link } from 'react-router-dom'

import type { StreamEventListOut } from '@/api/types'
import { apiFetch } from '@/api/client'
import { AppLayout } from '@/layouts/AppLayout'
import { formatDateRu } from '@/utils/datetime'
export const OperatorHomePage: React.FC = () => {
  const { message } = AntApp.useApp()

  const { data, isLoading } = useQuery({
    queryKey: ['streams'],
    queryFn: async () => (await apiFetch('/stream-events')) as StreamEventListOut[],
  })

  const handleCardClick = (ev: StreamEventListOut) => {
    if (!ev.has_slot_for_me) {
      message.warning('Все дни этого события уже распределены между операторами')
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
        События
      </Typography.Title>
      <Typography.Paragraph type="secondary">
        Выберите событие. Можно взять свободные дни турнира; если все дни заняты — карточка приглушена.
      </Typography.Paragraph>
      {!isLoading && (!data || data.length === 0) ? (
        <Empty description="Нет событий" />
      ) : (
        <Row gutter={[16, 16]}>
          {(data ?? []).map((ev) => {
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
                      borderColor: '#1f2a3a',
                      background: '#0d1219',
                    }}
                  >
                    <Space direction="vertical" size={8} style={{ width: '100%' }}>
                      <Typography.Title level={5} style={{ margin: 0, color: 'rgba(255,255,255,0.92)' }}>
                        {ev.title}
                      </Typography.Title>
                      <Typography.Text type="secondary">
                        Старт: {formatDateRu(ev.start_date)} · {ev.duration_days} дн.
                      </Typography.Text>
                      <Space wrap>
                        {ev.has_active_broadcast ? <Tag color="green">Эфир</Tag> : <Tag>Нет эфира</Tag>}
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
          })}
        </Row>
      )}
    </AppLayout>
  )
}
