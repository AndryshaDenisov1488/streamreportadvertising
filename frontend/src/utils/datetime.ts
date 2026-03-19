import dayjs from 'dayjs'
import timezone from 'dayjs/plugin/timezone'
import utc from 'dayjs/plugin/utc'

dayjs.extend(utc)
dayjs.extend(timezone)

/** Отображение: dd.mm.yyyy HH:mm (24ч), время в Europe/Moscow */
export const formatDateTimeRu = (value: string | undefined | null): string => {
  if (value == null || value === '') {
    return '—'
  }
  const d = dayjs(value)
  if (!d.isValid()) {
    return value
  }
  return d.tz('Europe/Moscow').format('DD.MM.YYYY HH:mm')
}

/** Только дата: dd.mm.yyyy (поля даты с API в виде YYYY-MM-DD) */
export const formatDateRu = (value: string | undefined | null): string => {
  if (value == null || value === '') {
    return '—'
  }
  const d = dayjs(value)
  if (!d.isValid()) {
    return value
  }
  return d.format('DD.MM.YYYY')
}
