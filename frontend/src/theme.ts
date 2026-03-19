import { theme } from 'antd'

/** Светлая тема: белый фон, акценты в духе логотипа (лазурь / тёмно-синий) */
export const appTheme = {
  algorithm: theme.defaultAlgorithm,
  token: {
    colorPrimary: '#0284c7',
    colorInfo: '#0891b2',
    colorLink: '#0284c7',
    colorBgLayout: '#f4f6f9',
    colorBgContainer: '#ffffff',
    colorBorder: '#e2e8f0',
    borderRadius: 10,
    fontFamily: '"Inter", system-ui, -apple-system, "Segoe UI", sans-serif',
    colorText: '#0f172a',
    colorTextSecondary: '#64748b',
    fontSize: 15,
    fontSizeLG: 16,
    controlHeight: 40,
    controlHeightLG: 52,
    paddingContentHorizontalLG: 20,
  },
  components: {
    Layout: {
      headerBg: '#ffffff',
      bodyBg: '#f4f6f9',
      footerBg: 'transparent',
    },
    Table: {
      headerBg: '#f1f5f9',
      headerColor: '#334155',
      cellPaddingBlockMD: 12,
      cellPaddingInlineMD: 10,
    },
    Button: {
      controlHeightLG: 52,
      fontSizeLG: 17,
      paddingInlineLG: 20,
    },
    Card: {
      paddingLG: 16,
    },
    List: {
      itemPaddingSM: '12px 0',
      itemPaddingLG: '14px 0',
    },
  },
}
