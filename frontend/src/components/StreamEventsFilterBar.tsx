import { DatePicker, Segmented, Select, Space, Typography } from 'antd'
import type { Dayjs } from 'dayjs'
import dayjs from 'dayjs'
import React from 'react'

import {
  defaultManagerRange,
  STREAM_CATEGORY_OPTIONS,
  type StreamCategory,
  upcomingRange,
} from '@/utils/streamEventFilters'

const { RangePicker } = DatePicker

export type StreamRangePreset = 'month' | 'upcoming' | 'next_month' | 'season'

type Props = {
  range: [Dayjs, Dayjs]
  onRangeChange: (range: [Dayjs, Dayjs]) => void
  category: StreamCategory
  onCategoryChange: (category: StreamCategory) => void
  preset: StreamRangePreset
  onPresetChange: (preset: StreamRangePreset) => void
  resultCount?: number
}

const presetRange = (preset: StreamRangePreset, today = dayjs()): [Dayjs, Dayjs] => {
  switch (preset) {
    case 'month':
      return defaultManagerRange(today)
    case 'upcoming':
      return upcomingRange(today, 60)
    case 'next_month':
      return [today.add(1, 'month').startOf('month'), today.add(1, 'month').endOf('month')]
    case 'season':
      return [today.startOf('month'), today.add(10, 'month').endOf('month')]
    default:
      return defaultManagerRange(today)
  }
}

export const StreamEventsFilterBar: React.FC<Props> = ({
  range,
  onRangeChange,
  category,
  onCategoryChange,
  preset,
  onPresetChange,
  resultCount,
}) => (
  <Space direction="vertical" size={12} style={{ width: '100%', marginBottom: 16 }}>
    <Space wrap align="center">
      <Typography.Text type="secondary">Период:</Typography.Text>
      <Segmented
        value={preset}
        onChange={(v) => {
          const next = v as StreamRangePreset
          onPresetChange(next)
          onRangeChange(presetRange(next))
        }}
        options={[
          { label: 'Текущий месяц', value: 'month' },
          { label: 'Ближайшие 60 дней', value: 'upcoming' },
          { label: 'Следующий месяц', value: 'next_month' },
          { label: 'Сезон вперёд', value: 'season' },
        ]}
      />
      <RangePicker
        value={range}
        onChange={(v) => {
          if (v?.[0] && v[1]) {
            onRangeChange([v[0].startOf('day'), v[1].endOf('day')])
            onPresetChange('month')
          }
        }}
        format="DD.MM.YYYY"
        allowClear={false}
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
      Сортировка: ближайшие к сегодня ({dayjs().format('DD.MM.YYYY')}) — сначала предстоящие, затем недавние.
    </Typography.Text>
  </Space>
)

export { presetRange }
