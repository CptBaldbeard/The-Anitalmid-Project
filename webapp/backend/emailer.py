"""Email sending — Resend HTTP API (preferred) or SMTP (fallback), with a dev mode.

Preferred path: RESEND_API_KEY env var -> POST https://api.resend.com/emails
(HTTPS/443 — never blocked in cloud egress, unlike SMTP/587 which some PaaS drop).

Fallback: SMTP_* env vars (SMTP_HOST/PORT/USER/PASSWORD/FROM) for any provider.
Dev mode: if neither is configured, the verification link is logged server-side.
"""
import json
import os
import smtplib
import ssl
import urllib.error
import urllib.request
from email.message import EmailMessage


def send_verification_email(to_email: str, username: str, link: str) -> bool:
    if os.environ.get("RESEND_API_KEY"):
        return _send_via_resend(to_email, username, link)
    if os.environ.get("SMTP_HOST") and os.environ.get("SMTP_FROM"):
        return _send_via_smtp(to_email, username, link)
    print(f"[emailer] no mail transport configured — verification link for {to_email}:\n  {link}")
    return False


def _send_via_resend(to_email: str, username: str, link: str) -> bool:
    api_key = os.environ["RESEND_API_KEY"]
    from_addr = os.environ.get("SMTP_FROM") or "no-reply@theanitalmidproject.com"
    payload = {
        "from": f"Anitalmid <{from_addr}>",
        "to": [to_email],
        "subject": "Verify your Anitalmid account",
        "text": _text_body(username, link),
        "html": _html_body(username, link),
    }
    req = urllib.request.Request(
        "https://api.resend.com/emails",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return 200 <= resp.status < 300
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"[emailer] Resend API {e.code} {e.reason}: {body[:400]}")
        return False
    except Exception as e:
        print(f"[emailer] Resend API failed for {to_email}: {e}")
        return False


def _send_via_smtp(to_email: str, username: str, link: str) -> bool:
    msg = EmailMessage()
    msg["Subject"] = "Verify your Anitalmid account"
    msg["From"] = os.environ["SMTP_FROM"]
    msg["To"] = to_email
    msg.set_content(_text_body(username, link))
    msg.add_alternative(_html_body(username, link), subtype="html")

    host = os.environ["SMTP_HOST"]
    port = int(os.environ.get("SMTP_PORT", "587"))
    user = os.environ.get("SMTP_USER")
    password = os.environ.get("SMTP_PASSWORD")

    try:
        ctx = ssl.create_default_context()
        with smtplib.SMTP(host, port, timeout=30) as s:
            s.ehlo()
            s.starttls(context=ctx)
            s.ehlo()
            if user:
                s.login(user, password)
            s.send_message(msg)
        return True
    except Exception as e:
        print(f"[emailer] SMTP failed for {to_email}: {e}")
        return False


def _text_body(username: str, link: str) -> str:
    return (
        f"Hi {username},\n\n"
        f"Verify your email to finish setting up your Anitalmid account:\n\n{link}\n\n"
        "This link expires in 24 hours. If you didn't create an account, ignore this email.\n"
    )


def _html_body(username: str, link: str) -> str:
    return f"""<html><body style="font-family:sans-serif;color:#222">
    <p>Hi {username},</p>
    <p>Verify your email to finish setting up your <b>Anitalmid</b> account:</p>
    <p><a href="{link}" style="background:#2dd4bf;color:#061018;padding:10px 18px;border-radius:6px;text-decoration:none;font-weight:bold">Verify email</a></p>
    <p style="color:#888">This link expires in 24 hours. If you didn't create an account, ignore this email.</p>
    </body></html>"""
