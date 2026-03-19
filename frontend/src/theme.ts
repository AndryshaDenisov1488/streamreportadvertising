import { theme } from 'antd'

export const appTheme = {
  algorithm: theme.darkAlgorithm,
  token: {
    colorPrimary: '#3d7eff',
    colorBgLayout: '#070b10',
    colorBgContainer: '#0d1219',
    colorBorder: '#1f2a3a',
    borderRadius: 10,
    fontFamily: 'Inter, system-ui, -apple-system, sans-serif',
    colorText: 'rgba(255,255,255,0.88)',
    colorTextSecondary: 'rgba(255,255,255,0.55)',
  },
  components: {
    Layout: {
      headerBg: '#0d1219',
      bodyBg: '#070b10',
      siderBg: '#0a1018',
    },
    Table: {
      headerBg: '#0f1622',
      headerColor: 'rgba(255,255,255,0.75)',
    },
    Button: {
      controlHeightLG: 52,
      fontSizeLG: 17,
    },
  },
}
