const API_BASE = import.meta.env.VITE_API_BASE ?? '/api/v1'

const ACCESS_KEY = 'access_token'

export const getAccessToken = (): string | null => localStorage.getItem(ACCESS_KEY)

export const setAccessToken = (token: string | null) => {
  if (!token) {
    localStorage.removeItem(ACCESS_KEY)
    return
  }
  localStorage.setItem(ACCESS_KEY, token)
}

type FetchOptions = RequestInit & { skipAuth?: boolean }

export const getOrCreateRequestId = (): string => {
  try {
    if (typeof crypto !== 'undefined' && crypto.randomUUID) {
      return crypto.randomUUID()
    }
  } catch {
    /* ignore */
  }
  return `${Date.now()}-${Math.random().toString(36).slice(2, 11)}`
}

const buildHeaders = (init?: HeadersInit, token?: string | null): HeadersInit => {
  const h = new Headers(init ?? {})
  if (token) {
    h.set('Authorization', `Bearer ${token}`)
  }
  if (!h.has('X-Request-ID')) {
    h.set('X-Request-ID', getOrCreateRequestId())
  }
  if (!h.has('Content-Type') && init && 'body' in (init as object)) {
    /* empty */
  }
  return h
}

export const apiFetch = async (path: string, options: FetchOptions = {}) => {
  const { skipAuth, headers, body, ...rest } = options
  const token = skipAuth ? null : getAccessToken()
  const merged = new Headers(buildHeaders(headers, token))
  if (body && typeof body === 'string' && !merged.has('Content-Type')) {
    merged.set('Content-Type', 'application/json')
  }
  const res = await fetch(`${API_BASE}${path}`, {
    ...rest,
    body,
    credentials: 'include',
    headers: merged,
  })
  if (!res.ok) {
    let detail = res.statusText
    try {
      const errJson = await res.json()
      if (errJson?.detail) {
        detail = typeof errJson.detail === 'string' ? errJson.detail : JSON.stringify(errJson.detail)
      }
    } catch {
      /* ignore */
    }
    throw new Error(detail)
  }
  if (res.status === 204) {
    return null
  }
  const ct = res.headers.get('content-type')
  if (ct?.includes('application/json')) {
    return res.json()
  }
  return res.blob()
}

export const loginRequest = async (email: string, password: string) => {
  const data = (await apiFetch('/auth/login', {
    method: 'POST',
    skipAuth: true,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  })) as { access_token: string; user: import('@/api/types').UserOut }
  setAccessToken(data.access_token)
  return data
}

export const logoutRequest = async () => {
  await apiFetch('/auth/logout', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}' })
  setAccessToken(null)
}

export const meRequest = async () => {
  return (await apiFetch('/auth/me')) as { user: import('@/api/types').UserOut }
}

export const getDashboardSummary = async () => {
  return (await apiFetch('/dashboard')) as import('@/api/types').DashboardSummaryOut
}

export const patchProfileRequest = async (body: {
  first_name?: string
  last_name?: string
  phone?: string
  telegram?: string
  onboarding_completed?: boolean
  /** только false — отклонить подсказку смены пароля */
  suggest_password_change?: boolean
}) => {
  return (await apiFetch('/profile', {
    method: 'PATCH',
    body: JSON.stringify(body),
  })) as import('@/api/types').UserOut
}

export const uploadAvatarRequest = async (file: File) => {
  const form = new FormData()
  form.append('file', file)
  const token = getAccessToken()
  const headers: Record<string, string> = {
    'X-Request-ID': getOrCreateRequestId(),
  }
  if (token) {
    headers.Authorization = `Bearer ${token}`
  }
  const res = await fetch(`${API_BASE}/profile/avatar`, {
    method: 'POST',
    body: form,
    credentials: 'include',
    headers,
  })
  if (!res.ok) {
    let detail = res.statusText
    try {
      const errJson = await res.json()
      if (errJson?.detail) {
        detail = typeof errJson.detail === 'string' ? errJson.detail : JSON.stringify(errJson.detail)
      }
    } catch {
      /* ignore */
    }
    throw new Error(detail)
  }
  return (await res.json()) as import('@/api/types').UserOut
}

export const getMyActivityPage = async (page: number, pageSize: number) => {
  const q = new URLSearchParams({ page: String(page), page_size: String(pageSize) })
  return (await apiFetch(`/profile/activity?${q.toString()}`)) as {
    items: import('@/api/types').AuditLogOut[]
    total: number
    page: number
    page_size: number
  }
}

export const changePasswordRequest = async (current_password: string, new_password: string) => {
  await apiFetch('/auth/change-password', {
    method: 'POST',
    body: JSON.stringify({ current_password, new_password }),
  })
}

export const listSessionsRequest = async () => {
  return (await apiFetch('/auth/sessions')) as import('@/api/types').SessionOut[]
}

export const revokeSessionRequest = async (sessionId: string) => {
  await apiFetch(`/auth/sessions/${sessionId}`, { method: 'DELETE' })
}

export const listEventTemplatesRequest = async () => {
  return (await apiFetch('/stream-event-templates')) as import('@/api/types').StreamEventTemplateOut[]
}

export const deleteEventTemplateRequest = async (id: string) => {
  await apiFetch(`/stream-event-templates/${id}`, { method: 'DELETE' })
}

export const instantiateTemplateRequest = async (
  templateId: string,
  body: { title: string; start_date: string; duration_days: number },
) => {
  return (await apiFetch(`/stream-event-templates/${templateId}/instantiate`, {
    method: 'POST',
    body: JSON.stringify(body),
  })) as import('@/api/types').StreamEventDetailOut
}

export const createTemplateFromEventRequest = async (streamId: string, name: string) => {
  return (await apiFetch(`/stream-event-templates/from-event/${streamId}`, {
    method: 'POST',
    body: JSON.stringify({ name }),
  })) as import('@/api/types').StreamEventTemplateOut
}
