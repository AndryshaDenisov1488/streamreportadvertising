import { Select, Space, Typography } from 'antd'
import React from 'react'

import {
  STREAM_CATEGORY_OPTIONS,
  type StreamCategory,
} from '@/utils/streamEventFilters'
import {
  currentSeasonYear,
  seasonFilterLabel,
  seasonLabel,
  type SeasonFilter,
} from '@/utils/season'

type Props = {
  seasonFilter: SeasonFilter
  onSeasonFilterChange: (filter: SeasonFilter) => void
  seasonsAvailable: number[]
  category: StreamCategory
  onCategoryChange: (category: StreamCategory) => void
  resultCount?: number
}

export const StreamEventsFilterBar: React.FC<Props> = ({
  seasonFilter,
  onSeasonFilterChange,
  seasonsAvailable,
  category,
  onCategoryChange,
  resultCount,
}) => {
  const currentSeason = currentSeasonYear()

  return (
    <Space direction="vertical" size={12} style={{ width: '100%', marginBottom: 16 }}>
      <Space wrap align="center">
        <Typography.Text type="secondary">Сезон:</Typography.Text>
        <Select
          style={{ minWidth: 260 }}
          value={seasonFilter === 'all' ? 'all' : String(seasonFilter)}
          onChange={(v) => onSeasonFilterChange(v === 'all' ? 'all' : Number(v))}
          options={[
            { value: 'all', label: 'За всё время' },
            ...seasonsAvailable.map((s) => ({
              value: String(s),
              label: `Сезон ${seasonLabel(s)}${s === currentSeason ? ' (текущий)' : ''}`,
            })),
          ]}
        />
        <Select
          style={{ minWidth: 220 }}
          value={category}
          onChange={onCategoryChange}
          options={STREAM_CATEGORY_OPTIONS}
        />
        {typeof resultCount === 'number' ? (
          <Typography.Text type="secondary">Показано: {resultCount}</Typography.Text>
        ) : null}
      </Space>
      <Typography.Text type="secondary" style={{ fontSize: 12 }}>
        {seasonFilterLabel(seasonFilter)} · сезон = 01.07 — 30.06 · сортировка: ближайшие к сегодня.
      </Typography.Text>
    </Space>
  )
}

// Legacy export for report modals that still use date ranges
export type StreamRangePreset = 'month' | 'upcoming' | 'next_month' | 'season'

export { defaultManagerRange, upcomingRange } from '@/utils/streamEventFilters'
