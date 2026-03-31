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

let refreshInFlight: Promise<boolean> | null = null

/** Обновляет access JWT по httpOnly refresh-cookie; дедупликация параллельных вызовов */
export const tryRefreshAccessToken = async (): Promise<boolean> => {
  if (refreshInFlight) {
    return refreshInFlight
  }
  refreshInFlight = (async () => {
    try {
      const res = await fetch(`${API_BASE}/auth/refresh`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          'X-Request-ID': getOrCreateRequestId(),
        },
        body: '{}',
      })
      if (!res.ok) {
        return false
      }
      const data = (await res.json()) as { access_token?: string }
      if (!data.access_token) {
        return false
      }
      setAccessToken(data.access_token)
      return true
    } catch {
      return false
    }
  })().finally(() => {
    refreshInFlight = null
  })
  return refreshInFlight
}

const fetchWithAuthRetry = async (url: string, init: RequestInit): Promise<Response> => {
  const run = async () => {
    const token = getAccessToken()
    const h = new Headers(init.headers)
    if (!h.has('X-Request-ID')) {
      h.set('X-Request-ID', getOrCreateRequestId())
    }
    if (token) {
      h.set('Authorization', `Bearer ${token}`)
    }
    return fetch(url, { ...init, credentials: 'include', headers: h })
  }
  let res = await run()
  if (res.status === 401) {
    const ok = await tryRefreshAccessToken()
    if (ok) {
      res = await run()
    }
  }
  return res
}

/** Скачивание бинарного ответа с авторизацией (ZIP, файлы) */
export const fetchAuthorizedBlob = async (path: string): Promise<{ blob: Blob; filename: string }> => {
  const res = await fetchWithAuthRetry(`${API_BASE}${path}`, { method: 'GET' })
  if (!res.ok) {
    let detail = res.statusText
    try {
      const errJson = (await res.json()) as { detail?: unknown }
      if (errJson?.detail) {
        detail = typeof errJson.detail === 'string' ? errJson.detail : JSON.stringify(errJson.detail)
      }
    } catch {
      /* ignore */
    }
    throw new Error(detail)
  }
  const blob = await res.blob()
  let filename = 'download'
  const cd = res.headers.get('Content-Disposition')
  if (cd) {
    const star = /filename\*=UTF-8''([^;\n]+)/i.exec(cd)
    const plain = /filename="([^"]+)"/i.exec(cd)
    if (star?.[1]) {
      filename = decodeURIComponent(star[1].trim())
    } else if (plain?.[1]) {
      filename = plain[1].trim()
    }
  }
  return { blob, filename }
}

export const triggerBlobDownload = (blob: Blob, filename: string) => {
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  a.rel = 'noopener'
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

export const uploadLogoRequest = async (file: File) => {
  const form = new FormData()
  form.append('file', file)
  const res = await fetchWithAuthRetry(`${API_BASE}/logos/upload`, {
    method: 'POST',
    body: form,
  })
  if (!res.ok) {
    let detail = res.statusText
    try {
      const errJson = (await res.json()) as { detail?: unknown }
      if (errJson?.detail) {
        detail = typeof errJson.detail === 'string' ? errJson.detail : JSON.stringify(errJson.detail)
      }
    } catch {
      /* ignore */
    }
    throw new Error(detail)
  }
  return (await res.json()) as import('@/api/types').LogoLibraryItemOut
}

/** Несколько файлов за один запрос (медиатека логотипов) */
export const uploadLogosBatchRequest = async (files: File[]) => {
  if (!files.length) {
    throw new Error('Не выбраны файлы')
  }
  const form = new FormData()
  for (const f of files) {
    form.append('files', f)
  }
  const res = await fetchWithAuthRetry(`${API_BASE}/logos/upload-batch`, {
    method: 'POST',
    body: form,
  })
  if (!res.ok) {
    let detail = res.statusText
    try {
      const errJson = (await res.json()) as { detail?: unknown }
      if (errJson?.detail) {
        detail = typeof errJson.detail === 'string' ? errJson.detail : JSON.stringify(errJson.detail)
      }
    } catch {
      /* ignore */
    }
    throw new Error(detail)
  }
  return (await res.json()) as import('@/api/types').LogoLibraryItemOut[]
}

export const apiFetch = async (path: string, options: FetchOptions = {}) => {
  const { skipAuth, headers, body, ...rest } = options
  const url = `${API_BASE}${path}`
  const pathOnly = path.split('?')[0]
  const allowRefreshOn401 = !skipAuth && pathOnly !== '/auth/login'
  const execute = async (): Promise<Response> => {
    const token = skipAuth ? null : getAccessToken()
    const merged = new Headers(buildHeaders(headers, token))
    if (body && typeof body === 'string' && !merged.has('Content-Type')) {
      merged.set('Content-Type', 'application/json')
    }
    return fetch(url, {
      ...rest,
      body,
      credentials: 'include',
      headers: merged,
    })
  }
  let res = await execute()
  if (res.status === 401 && allowRefreshOn401) {
    const refreshed = await tryRefreshAccessToken()
    if (refreshed) {
      res = await execute()
    }
  }
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

export const forgotPasswordRequest = async (email: string) => {
  return (await apiFetch('/auth/forgot-password', {
    method: 'POST',
    skipAuth: true,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email }),
  })) as { message: string }
}

export const validatePasswordResetTokenRequest = async (token: string) => {
  const q = new URLSearchParams({ token })
  return (await apiFetch(`/auth/password-reset/validate?${q.toString()}`, {
    skipAuth: true,
  })) as { ok: boolean }
}

export const resetPasswordRequest = async (payload: {
  token: string
  new_password: string
  new_password_confirm: string
}) => {
  await apiFetch('/auth/reset-password', {
    method: 'POST',
    skipAuth: true,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
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
  const res = await fetchWithAuthRetry(`${API_BASE}/profile/avatar`, {
    method: 'POST',
    body: form,
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
