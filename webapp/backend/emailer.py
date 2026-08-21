"""Email sending via SMTP (env-configured), with a dev fallback that logs the link.

Configure via env vars:
  SMTP_HOST, SMTP_PORT (default 587), SMTP_USER, SMTP_PASSWORD, SMTP_FROM
When SMTP_HOST/SMTP_FROM are unset, send_verification_email logs the link instead
and returns False (so local dev can surface the link without an SMTP server).
"""
import os
import smtplib
import ssl
from email.message import EmailMessage


def smtp_configured() -> bool:
    return bool(os.environ.get("SMTP_HOST") and os.environ.get("SMTP_FROM"))


def send_verification_email(to_email: str, username: str, link: str) -> bool:
    if not smtp_configured():
        print(f"[emailer] SMTP not configured — verification link for {to_email}:\n  {link}")
        return False

    msg = EmailMessage()
    msg["Subject"] = "Verify your Anitalmid account"
    msg["From"] = os.environ["SMTP_FROM"]
    msg["To"] = to_email
    msg.set_content(
        f"Hi {username},\n\n"
        f"Verify your email to finish setting up your Anitalmid account:\n\n{link}\n\n"
        "This link expires in 24 hours. If you didn't create an account, ignore this email.\n"
    )
    msg.add_alternative(
        f"""<html><body style="font-family:sans-serif;color:#222">
        <p>Hi {username},</p>
        <p>Verify your email to finish setting up your <b>Anitalmid</b> account:</p>
        <p><a href="{link}" style="background:#d4a24e;color:#111;padding:10px 18px;border-radius:6px;text-decoration:none;font-weight:bold">Verify email</a></p>
        <p style="color:#888">This link expires in 24 hours. If you didn't create an account, ignore this email.</p>
        </body></html>""",
        subtype="html",
    )

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
        print(f"[emailer] failed to send to {to_email}: {e}")
        return False
