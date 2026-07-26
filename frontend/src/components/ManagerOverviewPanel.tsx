import { AlertOutlined, LinkOutlined, TeamOutlined } from '@ant-design/icons'
import { Card, Col, Row, Statistic, Typography } from 'antd'
import React, { useMemo } from 'react'
import { Link } from 'react-router-dom'

import type { StreamEventListOut } from '@/api/types'
import {
  countMissingStreamLinks,
  filterStreamEvents,
  hasOperatorGap,
  upcomingRange,
  type StreamCategory,
} from '@/utils/streamEventFilters'

type Props = {
  events: StreamEventListOut[]
  category: StreamCategory
}

export const ManagerOverviewPanel: React.FC<Props> = ({ events, category }) => {
  const upcoming = useMemo(() => {
    const [from, to] = upcomingRange()
    return filterStreamEvents(events, { rangeStart: from, rangeEnd: to, category })
  }, [events, category])

  const activeCount = upcoming.filter((e) => e.has_active_broadcast).length
  const missingLinks = upcoming.filter((e) => countMissingStreamLinks(e) > 0)
  const withoutOperator = upcoming.filter((e) => hasOperatorGap(e))

  const nextEvent = upcoming.find((e) => !e.has_active_broadcast) ?? upcoming[0]

  return (
    <Row gutter={[16, 16]}>
      <Col xs={24} sm={12} lg={6}>
        <Card size="small" style={{ borderColor: '#e2e8f0' }}>
          <Statistic title="Ближайшие 60 дней" value={upcoming.length} suffix="меропр." />
        </Card>
      </Col>
      <Col xs={24} sm={12} lg={6}>
        <Card size="small" style={{ borderColor: '#e2e8f0' }}>
          <Statistic title="Эфир сейчас" value={activeCount} valueStyle={{ color: activeCount ? '#16a34a' : undefined }} />
        </Card>
      </Col>
      <Col xs={24} sm={12} lg={6}>
        <Card size="small" style={{ borderColor: '#e2e8f0' }}>
          <Statistic
            title="Без ссылки на трансляцию"
            value={missingLinks.length}
            valueStyle={{ color: missingLinks.length ? '#ea580c' : undefined }}
            prefix={<LinkOutlined />}
          />
        </Card>
      </Col>
      <Col xs={24} sm={12} lg={6}>
        <Card size="small" style={{ borderColor: '#e2e8f0' }}>
          <Statistic
            title="Без оператора"
            value={withoutOperator.length}
            valueStyle={{ color: withoutOperator.length ? '#dc2626' : undefined }}
            prefix={<TeamOutlined />}
          />
        </Card>
      </Col>
      {nextEvent ? (
        <Col span={24}>
          <Card size="small" style={{ borderColor: '#bae6fd', background: '#f0f9ff' }}>
            <Typography.Text>
              <AlertOutlined /> Следующее:{' '}
              <Link to={`/manager/${nextEvent.id}`} style={{ fontWeight: 600 }}>
                {nextEvent.title}
              </Link>
              {missingLinks.some((e) => e.id === nextEvent.id) ? ' — нужно заполнить ссылку на трансляцию' : ''}
            </Typography.Text>
          </Card>
        </Col>
      ) : null}
    </Row>
  )
}
