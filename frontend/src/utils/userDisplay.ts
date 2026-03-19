import type { UserOut } from '@/api/types'

/** Обращение по ФИО; если с бэка нет полей — собираем из частей или email */
export const userDisplayName = (
  user: Pick<UserOut, 'display_name' | 'last_name' | 'first_name' | 'email'> | null | undefined,
): string => {
  if (!user) {
    return ''
  }
  if (user.display_name && user.display_name.trim()) {
    return user.display_name.trim()
  }
  const s = `${user.last_name ?? ''} ${user.first_name ?? ''}`.trim()
  return s || user.email
}
