from unittest.mock import MagicMock

import pytest
from app.services import invite_email_service as mail


@pytest.mark.parametrize("use_ssl", [False, True])
def test_invite_uses_fast_connect_and_longer_delivery_timeout(monkeypatch, use_ssl):
    factory = MagicMock()
    smtp = factory.return_value.__enter__.return_value
    monkeypatch.setattr(mail.smtplib, "SMTP_SSL" if use_ssl else "SMTP", factory)
    mail._send_invite_sync(host="smtp.example.test", port=465 if use_ssl else 587,
                          user="sender", password="secret", use_tls=not use_ssl,
                          use_ssl=use_ssl, from_addr="Streaming Mainstream <info@ffkm.ru>",
                          to_addr="recipient@example.test", subject="Invite", body_html="<p>Invite</p>")
    assert factory.call_args.kwargs["timeout"] == 5
    smtp.sock.settimeout.assert_called_once_with(30)
    smtp.login.assert_called_once_with("sender", "secret")
    smtp.send_message.assert_called_once()
    message = smtp.send_message.call_args.args[0]
    assert message["From"] == "Streaming Mainstream <info@ffkm.ru>"
    assert smtp.starttls.call_count == (0 if use_ssl else 1)
