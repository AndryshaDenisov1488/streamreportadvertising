import path from 'node:path'
import { fileURLToPath } from 'node:url'

import { defineConfig, devices } from '@playwright/test'

const e2eDir = path.dirname(fileURLToPath(import.meta.url))

export default defineConfig({
  testDir: e2eDir,
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'list',
  use: {
    baseURL: process.env.E2E_BASE_URL ?? 'http://127.0.0.1',
    trace: 'on-first-retry',
    ...devices['Desktop Chrome'],
  },
})
