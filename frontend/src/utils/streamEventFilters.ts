import dayjs, { type Dayjs } from 'dayjs'

import type { StreamEventListOut } from '@/api/types'

export type StreamCategory =
  | 'all'
  | 'official_sports_significant'
  | 'all_russian'
  | 'official_physical_culture_and_mass_sports_show'
  | 'manual'

export const STREAM_CATEGORY_OPTIONS: { value: StreamCategory; label: string }[] = [
  { value: 'all', label: 'Все категории' },
  { value: 'official_sports_significant', label: 'Спортивное совершенство' },
  { value: 'all_russian', label: 'Всероссийские' },
  { value: 'official_physical_culture_and_mass_sports_show', label: 'Массовое спорт‑зрелищное' },
  { value: 'manual', label: 'Создано вручную' },
]

export const inferStreamCategory = (ev: StreamEventListOut): StreamCategory => {
  if (ev.ffkm_admin_rank) {
    return ev.ffkm_admin_rank as StreamCategory
  }
  if (!ev.ffkm_admin_tournament_id) {
    return 'manual'
  }
  const title = ev.title.toLowerCase()
  if (title.includes('всероссий') || title.includes('all-russian')) {
    return 'all_russian'
  }
  if (title.includes('массов') || title.includes('спорт-зрелищ') || title.includes('спорт‑зрелищ')) {
    return 'official_physical_culture_and_mass_sports_show'
  }
  if (title.includes('спортивное совершенство') || title.includes('спортивное и значимое')) {
    return 'official_sports_significant'
  }
  return 'all'
}

export const categoryLabel = (cat: StreamCategory): string =>
  STREAM_CATEGORY_OPTIONS.find((o) => o.value === cat)?.label ?? cat

export const eventEndDay = (ev: StreamEventListOut): Dayjs =>
  dayjs(ev.start_date).add(Math.max(ev.duration_days, 1) - 1, 'day')

export const eventOverlapsRange = (
  ev: StreamEventListOut,
  rangeStart: Dayjs,
  rangeEnd: Dayjs,
): boolean => {
  const start = dayjs(ev.start_date).startOf('day')
  const end = eventEndDay(ev).endOf('day')
  return !end.isBefore(rangeStart, 'day') && !start.isAfter(rangeEnd, 'day')
}

export const sortEventsUpcoming = (events: StreamEventListOut[], today = dayjs()): StreamEventListOut[] => {
  const todayStart = today.startOf('day')
  return [...events].sort((a, b) => {
    const aStart = dayjs(a.start_date).startOf('day')
    const bStart = dayjs(b.start_date).startOf('day')
    const aFuture = !aStart.isBefore(todayStart, 'day')
    const bFuture = !bStart.isBefore(todayStart, 'day')
    if (aFuture !== bFuture) {
      return aFuture ? -1 : 1
    }
    const aDist = Math.abs(aStart.diff(todayStart, 'day'))
    const bDist = Math.abs(bStart.diff(todayStart, 'day'))
    if (aDist !== bDist) {
      return aDist - bDist
    }
    if (!aStart.isSame(bStart, 'day')) {
      return aStart.isBefore(bStart) ? -1 : 1
    }
    return a.title.localeCompare(b.title, 'ru')
  })
}

export const filterStreamEvents = (
  events: StreamEventListOut[],
  opts: {
    rangeStart: Dayjs
    rangeEnd: Dayjs
    category: StreamCategory
    today?: Dayjs
  },
): StreamEventListOut[] => {
  const filtered = events.filter((ev) => {
    if (!eventOverlapsRange(ev, opts.rangeStart, opts.rangeEnd)) {
      return false
    }
    if (opts.category === 'all') {
      return true
    }
    return inferStreamCategory(ev) === opts.category
  })
  return sortEventsUpcoming(filtered, opts.today)
}

export const defaultManagerRange = (today = dayjs()): [Dayjs, Dayjs] => [
  today.startOf('month'),
  today.endOf('month'),
]

export const upcomingRange = (today = dayjs(), daysAhead = 60): [Dayjs, Dayjs] => [
  today.startOf('day'),
  today.add(daysAhead, 'day').endOf('day'),
]

export const countMissingStreamLinks = (ev: StreamEventListOut): number =>
  (ev.day_stream_links ?? []).filter((d) => !(d.stream_url || '').trim()).length

export const hasOperatorGap = (ev: StreamEventListOut): boolean => {
  if (ev.has_active_broadcast) {
    return false
  }
  if (!ev.assignment_summary && !ev.locked_by_user_id) {
    return true
  }
  const assignedDays = (ev.assignment_summary ?? '').match(/дни?\s+([\d,\s–-]+)/gi)
  if (!assignedDays && ev.duration_days > 0) {
    return true
  }
  return false
}
