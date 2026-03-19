/** Совпадает с backend app.utils.phone_ru.normalize_ru_mobile_phone */

export const normalizeRuMobilePhone = (raw: string): string => {
  const s = raw.trim()
  if (!s) {
    throw new Error('Пустой номер')
  }
  let digits = s.replace(/\D/g, '')
  if (digits.length === 11 && digits[0] === '8') {
    digits = `7${digits.slice(1)}`
  } else if (digits.length === 10 && digits[0] === '9') {
    digits = `7${digits}`
  }
  if (digits.length !== 11 || digits[0] !== '7') {
    throw new Error('Нужен российский мобильный: 10 цифр с 9 или 11 с 7/8')
  }
  if (digits[1] !== '9') {
    throw new Error('Поддерживаются только мобильные номера')
  }
  const rest = digits.slice(1)
  const a = rest.slice(0, 3)
  const b = rest.slice(3, 6)
  const c = rest.slice(6, 8)
  const d = rest.slice(8, 10)
  return `+7 (${a}) ${b} ${c} ${d}`
}
