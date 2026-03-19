export type UserRole = 'SUPERADMIN' | 'STREAM_MANAGER' | 'OPERATOR'

export type UserOut = {
  id: string
  email: string
  first_name: string
  last_name: string
  /** «Фамилия Имя», для обращения в интерфейсе */
  display_name: string
  role: UserRole
  is_active: boolean
  created_at: string
}

export type StreamEventListOut = {
  id: string
  title: string
  start_date: string
  duration_days: number
  locked_by_user_id: string | null
  /** Фамилия Имя того, кто взял событие в работу */
  locked_by_display_name: string | null
  has_active_broadcast: boolean
  created_at: string
}

export type StreamDayOut = {
  id: string
  day_index: number
  stream_url: string
  server_url: string
  stream_key: string
}

export type BroadcastSessionOut = {
  id: string
  stream_event_id: string
  day_index: number
  operator_id: string
  started_at: string
  ended_at: string | null
  is_active: boolean
}

export type BroadcastChecklistOut = {
  stream_event_id: string
  mic_ok: boolean
  scene_ok: boolean
  sponsor_slots_ok: boolean
  keys_tested_ok: boolean
  updated_at: string
}

export type StreamEventDetailOut = {
  id: string
  title: string
  start_date: string
  duration_days: number
  locked_by_user_id: string | null
  locked_by_display_name: string | null
  days: StreamDayOut[]
  active_broadcasts: BroadcastSessionOut[]
  created_at: string
  updated_at: string
}

export type SponsorMentionOut = {
  id: string
  broadcast_session_id: string
  original_offset_sec: number
  adjusted_offset_sec: number
  original_timecode: string
  adjusted_timecode: string
  absolute_moscow_original: string
  absolute_moscow_adjusted: string
  is_adjusted: boolean
  created_at: string
  adjustments: {
    id: string
    editor_user_id: string
    previous_adjusted_sec: number
    new_adjusted_sec: number
    created_at: string
  }[]
}

export type AuditLogOut = {
  id: string
  user_id: string | null
  action_type: string
  entity_type: string
  entity_id: string | null
  payload_before: Record<string, unknown> | null
  payload_after: Record<string, unknown> | null
  created_at: string
}

export type ReportMentionsOut = {
  items: {
    mention_id: string
    stream_event_id: string
    stream_title: string
    event_day_date: string
    day_index: number
    broadcast_session_id: string
    original_timecode: string
    adjusted_timecode: string
    absolute_moscow_adjusted: string
    is_adjusted: boolean
    mention_created_at: string
  }[]
  total: number
}
