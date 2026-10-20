import dayjs, { type Dayjs } from 'dayjs'

/** Season year = July start year (01.07.Y — 30.06.Y+1). */
export type SeasonFilter = number | 'all'

export const seasonYearFor = (d: Dayjs): number => (d.month() >= 6 ? d.year() : d.year() - 1)

export const currentSeasonYear = (today: Dayjs = dayjs()): number => seasonYearFor(today)

export const seasonBounds = (season: number): [Dayjs, Dayjs] => [
  dayjs(`${season}-07-01`).startOf('day'),
  dayjs(`${season + 1}-06-30`).endOf('day'),
]

export const seasonLabel = (season: number): string =>
  `${season}/${String(season + 1).slice(-2)}`

export const seasonsFromEvents = (startDates: string[], today: Dayjs = dayjs()): number[] => {
  const set = new Set<number>([currentSeasonYear(today)])
  for (const raw of startDates) {
    if (raw) {
      set.add(seasonYearFor(dayjs(raw)))
    }
  }
  return [...set].sort((a, b) => b - a)
}

export const rangeForSeasonFilter = (filter: SeasonFilter): [Dayjs, Dayjs] => {
  if (filter === 'all') {
    return [dayjs('2000-01-01').startOf('day'), dayjs('2100-12-31').endOf('day')]
  }
  return seasonBounds(filter)
}

export const seasonFilterLabel = (filter: SeasonFilter): string => {
  if (filter === 'all') {
    return 'За всё время'
  }
  const [start, end] = seasonBounds(filter)
  return `Сезон ${seasonLabel(filter)} (${start.format('DD.MM.YYYY')} — ${end.format('DD.MM.YYYY')})`
}
