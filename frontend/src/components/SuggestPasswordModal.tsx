import { Button, Modal, Typography } from 'antd'
import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { useAuth } from '@/auth/AuthContext'

const dismissKey = (userId: string) => `streaming_ops_suggest_pwd_dismiss_${userId}`

export const SuggestPasswordModal: React.FC = () => {
  const { user } = useAuth()
  const nav = useNavigate()
  const [open, setOpen] = useState(false)

  useEffect(() => {
    if (!user?.suggest_password_change) {
      setOpen(false)
      return
    }
    if (typeof localStorage !== 'undefined' && localStorage.getItem(dismissKey(user.id))) {
      setOpen(false)
      return
    }
    setOpen(true)
  }, [user?.id, user?.suggest_password_change])

  const handleLater = () => {
    if (user) {
      localStorage.setItem(dismissKey(user.id), '1')
    }
    setOpen(false)
  }

  const handleGoProfile = () => {
    setOpen(false)
    nav('/profile')
  }

  return (
    <Modal
      title="Рекомендуем сменить пароль"
      open={open}
      onCancel={handleLater}
      footer={[
        <Button key="later" onClick={handleLater}>
          Позже
        </Button>,
        <Button key="go" type="primary" onClick={handleGoProfile}>
          Открыть профиль
        </Button>,
      ]}
    >
      <Typography.Paragraph style={{ marginBottom: 0 }}>
        Вы вошли с временным или начальным паролем. Для безопасности лучше задать свой пароль в разделе «Профиль» —
        смена по желанию, можно отложить.
      </Typography.Paragraph>
    </Modal>
  )
}
