import { useEffect, useRef } from 'react'

import { getAccessToken } from '@/api/client'

const apiBase = import.meta.env.VITE_API_BASE ?? '/api/v1'

export const useStreamWs = (streamId: string | undefined, onEvent: (msg: Record<string, unknown>) => void) => {
  const cb = useRef(onEvent)
  cb.current = onEvent

  useEffect(() => {
    if (!streamId) {
      return
    }
    const token = getAccessToken()
    if (!token) {
      return
    }
    const proto = window.location.protocol === 'https:' ? 'wss' : 'ws'
    const url = `${proto}://${window.location.host}${apiBase}/ws/stream-events/${streamId}?token=${encodeURIComponent(token)}`
    const ws = new WebSocket(url)
    ws.onmessage = (ev) => {
      try {
        const data = JSON.parse(ev.data as string) as Record<string, unknown>
        cb.current(data)
      } catch {
        /* ignore */
      }
    }
    return () => {
      ws.close()
    }
  }, [streamId])
}
