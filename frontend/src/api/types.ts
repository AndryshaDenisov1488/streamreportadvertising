export type UserRole = 'SUPERADMIN' | 'STREAM_MANAGER' | 'OPERATOR'

export type UserOut = {
  id: string
  email: string
  first_name: string
  last_name: string
  /** «Фамилия Имя», для обращения в интерфейсе */
  display_name?: string
  phone?: string | null
  telegram?: string | null
  avatar_url?: string | null
  role: UserRole
  is_active: boolean
  /** Рекомендация сменить пароль после входа с временным паролем */
  suggest_password_change?: boolean
  /** false — показать интерактивное знакомство при первом входе */
  onboarding_completed?: boolean
  /** Последний вход по паролю / accept-invite (UTC с бэкенда) */
  last_login_at?: string | null
  last_login_ip?: string | null
  created_at: string
}

export type UserCreatedOut = {
  user: UserOut
  welcome_email_queued: boolean
  welcome_email_skipped_reason: string | null
}

export type DashboardSummaryOut = {
  role: string
  title: string
  cards: { key: string; title: string; value: string | number; hint: string }[]
}

export type SessionOut = {
  id: string
  created_at: string
  expires_at: string
  user_agent: string | null
  is_current: boolean
}

export type StreamEventTemplateOut = {
  id: string
  name: string
  title: string
  duration_days: number
  created_at: string
}

export type DayAssignmentOut = {
  day_index: number
  operator_id: string
  operator_display_name: string
  operator_email: string
}

export type StreamEventListOut = {
  id: string
  title: string
  start_date: string
  duration_days: number
  locked_by_user_id: string | null
  /** Устар.: один оператор; при нескольких — assignment_summary */
  locked_by_display_name: string | null
  assignment_summary: string | null
  has_slot_for_me: boolean
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
  day_index: number
  picture_exposure_ok: boolean
  judges_stream_ok: boolean
  splitter_socket_ok: boolean
  key_stream_started_ok: boolean
  kick_ok: boolean
  mentions_four_ok: boolean
  updated_at: string
}

export type StreamLogoItemOut = {
  id: string
  filename_original: string
  public_url: string
  sort_order: number
  created_at: string
}

export type LogoLibraryItemOut = {
  id: string
  filename_original: string
  public_url: string
  created_at: string
  uploaded_by_id: string | null
}

export type StreamEventDetailOut = {
  id: string
  title: string
  start_date: string
  duration_days: number
  locked_by_user_id: string | null
  locked_by_display_name: string | null
  day_assignments: DayAssignmentOut[]
  days: StreamDayOut[]
  active_broadcasts: BroadcastSessionOut[]
  /** С бэкенда v2+; при старых ответах может отсутствовать */
  content_url?: string | null
  logos?: StreamLogoItemOut[]
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
