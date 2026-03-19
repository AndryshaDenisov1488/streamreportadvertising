import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ConfigProvider, App as AntApp } from 'antd'
import ruRU from 'antd/locale/ru_RU'
import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'

import { AuthProvider } from '@/auth/AuthContext'
import { App } from '@/App'
import { AnalyticsTracker } from '@/components/AnalyticsTracker'
import { appTheme } from '@/theme'
import '@/styles/global.css'

if (import.meta.env.VITE_SENTRY_DSN) {
  void import('@sentry/react')
    .then((Sentry) => {
      Sentry.init({
        dsn: import.meta.env.VITE_SENTRY_DSN,
        environment: import.meta.env.MODE,
        tracesSampleRate: 0.15,
      })
    })
    .catch(() => {
      /* пакет не установлен — пропускаем */
    })
}

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: 1, refetchOnWindowFocus: false },
  },
})

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <ConfigProvider locale={ruRU} theme={appTheme}>
        <AntApp>
          <BrowserRouter>
            <AuthProvider>
              <AnalyticsTracker />
              <App />
            </AuthProvider>
          </BrowserRouter>
        </AntApp>
      </ConfigProvider>
    </QueryClientProvider>
  </React.StrictMode>,
)
