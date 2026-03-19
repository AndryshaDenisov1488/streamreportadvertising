def seconds_to_hhmmss(total_sec: int) -> str:
    sec = max(0, int(total_sec))
    h, r = divmod(sec, 3600)
    m, s = divmod(r, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"
