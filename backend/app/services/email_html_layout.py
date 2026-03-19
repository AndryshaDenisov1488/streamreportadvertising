"""Единая вёрстка писем (inline CSS, таблицы — для совместимости с клиентами почты)."""

import html


def wrap_email_html(
    *,
    headline: str,
    inner_html: str,
    public_base_url: str = "",
    footer_line: str = "MainStream Ops · Сервис для видеооператоров MainStream",
) -> str:
    """Оборачивает контент в шапку/подвал. headline и URL экранируются."""
    safe_headline = html.escape(headline.strip() or "MainStream Ops")
    base = (public_base_url or "").strip().rstrip("/")
    if base:
        logo_url = f"{base}/mainstream-logo.png"
        logo_block = (
            f'<img src="{html.escape(logo_url, quote=True)}" alt="MainStream" width="168" '
            'style="display:block;border:0;outline:none;height:auto;max-width:100%" />'
        )
    else:
        logo_block = (
            '<span style="font-size:20px;font-weight:700;color:#e8eef8;letter-spacing:0.02em">'
            "MainStream Ops</span>"
        )
    safe_footer = html.escape(footer_line)
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width">
<title>{safe_headline}</title>
</head>
<body style="margin:0;padding:0;background:#0a0e14;">
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:#0a0e14;padding:24px 12px;">
<tr><td align="center">
<table role="presentation" width="600" cellspacing="0" cellpadding="0" style="max-width:600px;width:100%;background:#111822;border:1px solid #1f2a3a;border-radius:12px;overflow:hidden;">
<tr><td style="padding:28px 28px 20px;background:linear-gradient(180deg,#152030 0%,#111822 100%);border-bottom:1px solid #1f2a3a;text-align:center;">
{logo_block}
</td></tr>
<tr><td style="padding:16px 28px 8px;">
<p style="margin:0;font-family:Segoe UI,Roboto,Helvetica,Arial,sans-serif;font-size:18px;color:#f0f4fa;line-height:1.45;font-weight:600;">{safe_headline}</p>
</td></tr>
<tr><td style="padding:8px 28px 28px;font-family:Segoe UI,Roboto,Helvetica,Arial,sans-serif;font-size:15px;line-height:1.6;color:#c5d0e0;">
{inner_html}
</td></tr>
<tr><td style="padding:16px 28px 22px;border-top:1px solid #1f2a3a;font-family:Segoe UI,Roboto,Helvetica,Arial,sans-serif;font-size:12px;color:#6b7c93;line-height:1.5;">
{safe_footer}
</td></tr>
</table>
</td></tr>
</table>
</body>
</html>"""
