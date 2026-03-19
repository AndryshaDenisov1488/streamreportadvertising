import type { Preview } from '@storybook/react'
import React from 'react'

import { ConfigProvider } from 'antd'
import ruRU from 'antd/locale/ru_RU'

import { appTheme } from '../src/theme'

const preview: Preview = {
  decorators: [
    (Story) => (
      <ConfigProvider locale={ruRU} theme={appTheme}>
        <div style={{ background: '#070b10', minHeight: '100vh', padding: 24 }}>
          <Story />
        </div>
      </ConfigProvider>
    ),
  ],
}

export default preview
