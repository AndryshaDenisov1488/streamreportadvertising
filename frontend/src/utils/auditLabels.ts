/** Человекочитаемые подписи для журнала аудита */

export const auditActionLabel = (code: string): string => {
  const m: Record<string, string> = {
    LOGIN: 'Вход в систему',
    LOGOUT: 'Выход',
    USER_CREATE: 'Создание пользователя',
    USER_UPDATE: 'Изменение пользователя',
    USER_DELETE: 'Удаление пользователя',
    STREAM_CREATE: 'Создание события',
    STREAM_UPDATE: 'Изменение события',
    STREAM_DELETE: 'Удаление события',
    STREAM_LOCK: 'Событие взято в работу',
    STREAM_UNLOCK: 'Событие снято с работы',
    BROADCAST_START: 'Начало эфира',
    BROADCAST_STOP: 'Остановка эфира',
    MENTION_CREATE: 'Добавлено упоминание',
    MENTION_UPDATE: 'Изменено упоминание',
  }
  return m[code] ?? code
}

export const auditEntityLabel = (code: string): string => {
  const m: Record<string, string> = {
    user: 'Пользователь',
    stream_event: 'Событие',
    broadcast_session: 'Сессия эфира',
    sponsor_mention: 'Упоминание спонсора',
  }
  return m[code] ?? code
}

const payloadKeyLabel = (key: string): string => {
  const m: Record<string, string> = {
    before: 'было',
    after: 'стало',
    stream_event_id: 'событие',
    broadcast_session_id: 'сессия эфира',
    sponsor_mention_id: 'упоминание',
    mention_id: 'упоминание',
    day_index: 'день',
    started_at: 'начало',
    ended_at: 'окончание',
    title: 'название',
    start_date: 'дата старта',
    duration_days: 'дней',
    offset_sec: 'смещение, с',
    original_offset_sec: 'исходное смещение, с',
    adjusted_offset_sec: 'скорректировано, с',
    email: 'email',
    first_name: 'имя',
    last_name: 'фамилия',
    ip: 'IP',
    locked_by_user_id: 'заблокировал',
    entity_type: 'тип сущности',
    entity_id: 'id сущности',
  }
  return m[key] ?? key
}

const formatPayloadValue = (v: unknown): string => {
  if (v === null || v === undefined) {
    return '—'
  }
  if (typeof v === 'object' && v !== null && !Array.isArray(v)) {
    return formatAuditPayloadRu(v as Record<string, unknown>)
  }
  if (typeof v === 'string' && v.length > 120) {
    return `${v.slice(0, 120)}…`
  }
  return String(v)
}

/** Короткое русскоязычное описание JSON полезной нагрузки аудита */
export const formatAuditPayloadRu = (obj: Record<string, unknown> | null | undefined): string => {
  if (!obj || typeof obj !== 'object') {
    return '—'
  }
  const parts: string[] = []
  for (const [k, val] of Object.entries(obj)) {
    const label = payloadKeyLabel(k)
    if (val !== null && val !== undefined && typeof val === 'object' && !Array.isArray(val)) {
      parts.push(`${label}: { ${formatAuditPayloadRu(val as Record<string, unknown>)} }`)
      continue
    }
    parts.push(`${label}: ${formatPayloadValue(val)}`)
  }
  return parts.join('; ')
}
