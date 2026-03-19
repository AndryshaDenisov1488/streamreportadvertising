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

const buildHeaders = (init?: HeadersInit, token?: string | null): HeadersInit => {
  const h = new Headers(init ?? {})
  if (token) {
    h.set('Authorization', `Bearer ${token}`)
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
