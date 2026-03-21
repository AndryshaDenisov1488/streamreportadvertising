import { App as AntApp, Button, DatePicker, Space, Typography } from 'antd'
import dayjs from 'dayjs'
import utc from 'dayjs/plugin/utc'
import timezone from 'dayjs/plugin/timezone'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import React, { useEffect, useState } from 'react'

import { apiFetch } from '@/api/client'

dayjs.extend(utc)
dayjs.extend(timezone)

const toMoscowDayjs = (v: dayjs.Dayjs) =>
  dayjs.tz(v.format('YYYY-MM-DD HH:mm'), 'YYYY-MM-DD HH:mm', 'Europe/Moscow')

type BroadcastActualStartPanelProps = {
  streamId: string
  dayIndex: number
  startedAtIso: string
  disabled?: boolean
}

export const BroadcastActualStartPanel: React.FC<BroadcastActualStartPanelProps> = ({
  streamId,
  dayIndex,
  startedAtIso,
  disabled,
}) => {
  const { message } = AntApp.useApp()
  const qc = useQueryClient()
  const [pick, setPick] = useState(() => dayjs.utc(startedAtIso).tz('Europe/Moscow'))

  useEffect(() => {
    setPick(dayjs.utc(startedAtIso).tz('Europe/Moscow'))
  }, [startedAtIso])

  const mut = useMutation({
    mutationFn: async (value: dayjs.Dayjs) => {
      const msk = toMoscowDayjs(value)
      const iso = msk.utc().toISOString()
      await apiFetch(`/stream-events/${streamId}/days/${dayIndex}/broadcast/actual-start`, {
        method: 'POST',
        body: JSON.stringify({ actual_started_at: iso }),
      })
    },
    onSuccess: async () => {
      message.success('Время начала эфира обновлено, таймкоды сдвинуты')
      await qc.invalidateQueries({ queryKey: ['stream', streamId] })
      await qc.invalidateQueries({ queryKey: ['mentions', streamId, dayIndex] })
    },
    onError: (e: Error) => message.error(e.message),
  })

  return (
    <div
      style={{
        padding: 12,
        borderRadius: 10,
        border: '1px solid #fde68a',
        background: '#fffbeb',
      }}
    >
      <Typography.Text strong style={{ display: 'block', marginBottom: 8 }}>
        Фактическое начало эфира (МСК)
      </Typography.Text>
      <Typography.Paragraph type="secondary" style={{ fontSize: 12, marginBottom: 10 }}>
        Если нажали «Начать эфир» позже, чем реально пошла картинка (например в 18:13 вместо 18:00), укажите время,
        когда эфир реально начался. Все таймкоды упоминаний и абсолютные времена сдвинутся; расстояния между отметками
        не изменятся.
      </Typography.Paragraph>
      <Space wrap style={{ width: '100%' }} align="center">
        <DatePicker
          showTime
          format="DD.MM.YYYY HH:mm"
          minuteStep={1}
          value={pick}
          onChange={(v) => {
            if (v) {
              setPick(toMoscowDayjs(v))
            }
          }}
          disabled={disabled || mut.isPending}
          style={{ minWidth: 240 }}
        />
        <Button type="primary" loading={mut.isPending} disabled={disabled} onClick={() => mut.mutate(pick)}>
          Применить
        </Button>
      </Space>
    </div>
  )
}
