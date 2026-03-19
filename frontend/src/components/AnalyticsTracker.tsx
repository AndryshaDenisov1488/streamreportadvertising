import { useEffect, useRef } from 'react'
import { useLocation } from 'react-router-dom'

import { useAuth } from '@/auth/AuthContext'
import { apiFetch } from '@/api/client'

/** Лёгкая продуктовая аналитика: события page_view на смене маршрута. */
export const AnalyticsTracker = () => {
  const loc = useLocation()
  const { user } = useAuth()
  const lastPath = useRef<string | null>(null)

  useEffect(() => {
    if (!user || loc.pathname === '/login') {
      return
    }
    if (lastPath.current === loc.pathname) {
      return
    }
    lastPath.current = loc.pathname
    void apiFetch('/analytics/events', {
      method: 'POST',
      body: JSON.stringify({
        event_name: 'page_view',
        meta: { path: loc.pathname },
      }),
    }).catch(() => {
      /* offline / 401 — не мешаем UX */
    })
  }, [loc.pathname, user])

  return null
}
