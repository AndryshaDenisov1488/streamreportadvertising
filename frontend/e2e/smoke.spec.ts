import { expect, test } from '@playwright/test'

test('страница входа отображается', async ({ page }) => {
  await page.goto('/login')
  await expect(page.locator('input[type="password"]')).toBeVisible()
})
