"""Нормализация российских мобильных номеров в вид +7 (XXX) XXX XX XX."""


def normalize_ru_mobile_phone(raw: str) -> str:
    """
    Принимает ввод в любом распространённом виде: 79060943936, 89060943936, +7 906 094-39-36 и т.д.
    Возвращает канонический формат. Только мобильные РФ (вторая цифра 9).
    """
    s = (raw or "").strip()
    if not s:
        raise ValueError("Пустой номер")
    digits = "".join(c for c in s if c.isdigit())
    if len(digits) == 11 and digits[0] == "8":
        digits = "7" + digits[1:]
    elif len(digits) == 10 and digits[0] == "9":
        digits = "7" + digits
    if len(digits) != 11 or digits[0] != "7":
        raise ValueError("Нужен российский мобильный: 10 цифр с 9 или 11 с 7/8")
    if digits[1] != "9":
        raise ValueError("Поддерживаются только мобильные номера (9XXXXXXXXX)")
    rest = digits[1:]
    a, b, c, d = rest[:3], rest[3:6], rest[6:8], rest[8:10]
    return f"+7 ({a}) {b} {c} {d}"


def normalize_ru_mobile_phone_or_empty(raw: str | None) -> str | None:
    """Пустая строка → None. Иначе нормализация или ValueError."""
    if raw is None:
        return None
    s = raw.strip()
    if not s:
        return None
    return normalize_ru_mobile_phone(s)
