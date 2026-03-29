import { useEffect, useRef } from 'react'

import { getAccessToken } from '@/api/client'

const apiBase = import.meta.env.VITE_API_BASE ?? '/api/v1'

export const useStreamWs = (
  streamId: string | undefined,
  onEvent: (msg: Record<string, unknown>) => void,
  enabled = true,
) => {
  const cb = useRef(onEvent)
  cb.current = onEvent

  useEffect(() => {
    if (!streamId || !enabled) {
      return
    }
    const token = getAccessToken()
    if (!token) {
      return
    }
    const proto = window.location.protocol === 'https:' ? 'wss' : 'ws'
    const url = `${proto}://${window.location.host}${apiBase}/ws/stream-events/${streamId}`
    const ws = new WebSocket(url)
    ws.onopen = () => {
      const t = getAccessToken()
      if (!t || ws.readyState !== WebSocket.OPEN) {
        ws.close()
        return
      }
      ws.send(JSON.stringify({ type: 'auth', access_token: t }))
    }
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
  }, [streamId, enabled])
}
