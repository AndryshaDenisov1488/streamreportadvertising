import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
import test from 'node:test'
import ts from 'typescript'

const source = await readFile(new URL('../src/api/client.ts', import.meta.url), 'utf8')
const compiled = ts.transpileModule(
  source.replace('import.meta.env.VITE_API_BASE', "'/api/v1'"),
  { compilerOptions: { module: ts.ModuleKind.ESNext, target: ts.ScriptTarget.ES2022 } },
).outputText

const loadClient = async (t, fetch) => {
  t.mock.method(globalThis, 'fetch', fetch)
  const originalStorage = globalThis.localStorage
  globalThis.localStorage = { getItem: () => 'test-token', setItem: () => {} }
  t.after(() => { globalThis.localStorage = originalStorage })
  return import(`data:text/javascript;base64,${Buffer.from(compiled).toString('base64')}#${Math.random()}`)
}

test('request deadline aborts a stalled invite and reports unknown delivery status', async (t) => {
  let signal
  const { apiFetch } = await loadClient(t, (_url, init) => {
    signal = init.signal
    return new Promise(() => {})
  })
  await assert.rejects(apiFetch('/users/invites', {
    method: 'POST', timeoutMs: 20, timeoutMessage: 'Отправка не подтверждена',
  }), /Отправка не подтверждена/)
  assert.equal(signal.aborted, true)
})

test('deadline also covers a stalled token refresh', async (t) => {
  const calls = []
  const { apiFetch } = await loadClient(t, async (url) => {
    calls.push(url)
    if (url.endsWith('/auth/refresh')) return new Promise(() => {})
    return new Response(null, { status: 401 })
  })
  await assert.rejects(apiFetch('/users/invites', { timeoutMs: 20 }), /Сервер не ответил вовремя/)
  assert.deepEqual(calls, ['/api/v1/users/invites', '/api/v1/auth/refresh'])
})

test('successful invite returns response and clears its deadline', async (t) => {
  let signal
  const { apiFetch } = await loadClient(t, async (_url, init) => {
    signal = init.signal
    return Response.json({ id: 'invite-id' })
  })
  assert.deepEqual(await apiFetch('/users/invites', { timeoutMs: 20 }), { id: 'invite-id' })
  await new Promise((resolve) => setTimeout(resolve, 30))
  assert.equal(signal.aborted, false)
})

test('SMTP error remains visible to the caller', async (t) => {
  const { apiFetch } = await loadClient(t, async () => Response.json(
    { detail: 'Не удалось отправить письмо' }, { status: 503 },
  ))
  await assert.rejects(apiFetch('/users/invites', { timeoutMs: 100 }), /Не удалось отправить письмо/)
})
