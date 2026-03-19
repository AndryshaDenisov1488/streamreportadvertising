import { LogoutOutlined } from '@ant-design/icons'
import { Button, Grid, Layout, Space, Tooltip, Typography } from 'antd'
import React from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { BrandLogo } from '@/components/BrandLogo'
import { NotificationBell } from '@/components/NotificationBell'
import { SuggestPasswordModal } from '@/components/SuggestPasswordModal'
import { useAuth } from '@/auth/AuthContext'
import { userDisplayName } from '@/utils/userDisplay'

const { Header, Content, Footer } = Layout

export const AppLayout: React.FC<{ children: React.ReactNode; nav?: React.ReactNode }> = ({
  children,
  nav,
}) => {
  const { user, logout } = useAuth()
  const navHook = useNavigate()
  const screens = Grid.useBreakpoint()
  const isNarrow = !screens.md

  const handleLogout = async () => {
    await logout()
    navHook('/login')
  }

  const headerPad = isNarrow ? 12 : 20
  const safePad = {
    paddingLeft: `max(${headerPad}px, env(safe-area-inset-left, 0px))`,
    paddingRight: `max(${headerPad}px, env(safe-area-inset-right, 0px))`,
  }

  return (
    <Layout style={{ minHeight: '100%', background: '#f5f7fa', display: 'flex', flexDirection: 'column' }}>
      <Header
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: isNarrow ? 'wrap' : 'nowrap',
          gap: isNarrow ? 8 : 16,
          background: '#ffffff',
          boxShadow: '0 1px 0 rgba(15, 23, 42, 0.06)',
          borderBottom: '1px solid #e2e8f0',
          ...safePad,
          height: 'auto',
          minHeight: 64,
          lineHeight: isNarrow ? '1.35' : '64px',
          paddingBlock: isNarrow ? 10 : 0,
        }}
      >
        <Space
          size={isNarrow ? 'small' : 'large'}
          align="start"
          wrap
          style={{ flex: isNarrow ? '1 1 100%' : undefined, minWidth: 0 }}
        >
          <Link
            to="/dashboard"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: isNarrow ? 8 : 12,
              color: '#0f172a',
              fontWeight: 600,
              fontSize: isNarrow ? 15 : undefined,
              textDecoration: 'none',
            }}
            aria-label="MainStream — дашборд"
          >
            <BrandLogo height={isNarrow ? 22 : 30} />
            <span style={{ whiteSpace: 'nowrap' }}>Ops</span>
          </Link>
          <Link to="/dashboard" style={{ color: '#475569', fontSize: isNarrow ? 14 : 13 }}>
            Дашборд
          </Link>
          <Link to="/profile" style={{ color: '#475569', fontSize: isNarrow ? 14 : 13 }}>
            Профиль
          </Link>
          {user?.role === 'SUPERADMIN' ? (
            <Space size="small" wrap>
              <Link to="/admin" style={{ color: '#475569', fontSize: isNarrow ? 14 : 13 }}>
                Админ
              </Link>
              <Link to="/manager" style={{ color: '#475569', fontSize: isNarrow ? 14 : 13 }}>
                Менеджер
              </Link>
              <Link to="/operator" style={{ color: '#475569', fontSize: isNarrow ? 14 : 13 }}>
                Оператор
              </Link>
            </Space>
          ) : null}
          {nav ? (
            <div style={{ width: isNarrow ? '100%' : 'auto' }}>{nav}</div>
          ) : null}
        </Space>
        <Space
          align="center"
          wrap
          size="small"
          style={{
            flexShrink: 0,
            marginLeft: isNarrow ? 'auto' : undefined,
          }}
        >
          {!isNarrow ? (
            <>
              <div style={{ textAlign: 'right' as const }}>
                <Typography.Text strong style={{ display: 'block', maxWidth: 260 }} ellipsis>
                  {user ? userDisplayName(user) : ''}
                </Typography.Text>
                <Typography.Text type="secondary" ellipsis style={{ fontSize: 12, display: 'block', maxWidth: 260 }}>
                  {user?.email}
                </Typography.Text>
                <Typography.Text type="secondary" style={{ fontSize: 11 }}>
                  {user?.role === 'SUPERADMIN'
                    ? 'Суперадмин'
                    : user?.role === 'STREAM_MANAGER'
                      ? 'Менеджер'
                      : user?.role === 'OPERATOR'
                        ? 'Оператор'
                        : user?.role}
                </Typography.Text>
              </div>
            </>
          ) : (
            <Tooltip title={`${user ? userDisplayName(user) : ''} · ${user?.email ?? ''}`}>
              <Typography.Text strong ellipsis style={{ maxWidth: 100, fontSize: 12, display: 'block' }}>
                {user ? userDisplayName(user) : ''}
              </Typography.Text>
            </Tooltip>
          )}
          {user ? <NotificationBell /> : null}
          <Tooltip title="Выйти">
            <Button
              type="default"
              icon={<LogoutOutlined />}
              onClick={() => void handleLogout()}
              aria-label="Выйти из аккаунта"
            >
              {!isNarrow ? 'Выйти' : null}
            </Button>
          </Tooltip>
        </Space>
      </Header>
      <Content
        style={{
          flex: 1,
          padding: isNarrow ? 12 : 20,
          paddingBottom: `max(${isNarrow ? 12 : 20}px, env(safe-area-inset-bottom, 0px))`,
        }}
      >
        {children}
      </Content>
      <Footer
        style={{
          marginTop: 'auto',
          padding: isNarrow ? '14px 12px' : '16px 20px',
          paddingBottom: `max(${isNarrow ? 14 : 16}px, env(safe-area-inset-bottom, 0px))`,
          background: 'transparent',
          borderTop: '1px solid #e2e8f0',
          textAlign: 'center',
        }}
      >
        <Space direction="vertical" size={6} style={{ width: '100%' }}>
          <div style={{ display: 'flex', justifyContent: 'center', opacity: 0.9 }}>
            <BrandLogo height={18} />
          </div>
          <Typography.Text type="secondary" style={{ fontSize: 12 }}>
            Панель эфиров · Москва
          </Typography.Text>
        </Space>
      </Footer>
      <SuggestPasswordModal />
    </Layout>
  )
}
