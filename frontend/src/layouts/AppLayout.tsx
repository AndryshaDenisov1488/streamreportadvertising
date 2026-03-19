import { LogoutOutlined } from '@ant-design/icons'
import { Button, Layout, Space, Typography } from 'antd'
import React from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { useAuth } from '@/auth/AuthContext'

const { Header, Content } = Layout

export const AppLayout: React.FC<{ children: React.ReactNode; nav?: React.ReactNode }> = ({
  children,
  nav,
}) => {
  const { user, logout } = useAuth()
  const navHook = useNavigate()

  const handleLogout = async () => {
    await logout()
    navHook('/login')
  }

  return (
    <Layout style={{ minHeight: '100%', background: '#070b10' }}>
      <Header
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          borderBottom: '1px solid #1f2a3a',
          paddingInline: 20,
          height: 64,
          lineHeight: '64px',
        }}
      >
        <Space size="large" align="center" wrap>
          <Link to="/" style={{ color: 'rgba(255,255,255,0.92)', fontWeight: 600 }}>
            MainStream Ops
          </Link>
          {user?.role === 'SUPERADMIN' ? (
            <Space size="middle" wrap>
              <Link to="/admin" style={{ color: 'rgba(255,255,255,0.65)', fontSize: 13 }}>
                Админ
              </Link>
              <Link to="/manager" style={{ color: 'rgba(255,255,255,0.65)', fontSize: 13 }}>
                Менеджер
              </Link>
              <Link to="/operator" style={{ color: 'rgba(255,255,255,0.65)', fontSize: 13 }}>
                Оператор
              </Link>
            </Space>
          ) : null}
          {nav}
        </Space>
        <Space align="center">
          <Typography.Text type="secondary">{user?.email}</Typography.Text>
          <Typography.Text type="secondary" style={{ fontSize: 12 }}>
            {user?.role}
          </Typography.Text>
          <Button icon={<LogoutOutlined />} onClick={() => void handleLogout()}>
            Выйти
          </Button>
        </Space>
      </Header>
      <Content style={{ padding: 20 }}>{children}</Content>
    </Layout>
  )
}
