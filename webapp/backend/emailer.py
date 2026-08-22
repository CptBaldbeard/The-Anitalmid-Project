"""Email sending via the Resend HTTP API (HTTPS/443 — cloud-egress safe).

Requires RESEND_API_KEY in the environment. If unset (local dev), the email
is logged server-side and send_email returns False.
"""
import html
import json
import os
import urllib.error
import urllib.request

FROM_ADDR = os.environ.get("SMTP_FROM") or "no-reply@theanitalmidproject.com"
BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
)
BASE_URL = os.environ.get("ANITALMID_BASE_URL", "https://theanitalmidproject.com").rstrip("/")


def send_email(to_email: str, subject: str, html: str, text: str = "") -> bool:
    """Send an HTML email via Resend. Returns True on success."""
    api_key = os.environ.get("RESEND_API_KEY")
    if not api_key:
        print(f"[emailer] no RESEND_API_KEY — would email {to_email}: {subject}")
        return False

    payload = {
        "from": f"Anitalmid <{FROM_ADDR}>",
        "to": [to_email],
        "subject": subject,
        "html": html,
    }
    if text:
        payload["text"] = text

    req = urllib.request.Request(
        "https://api.resend.com/emails",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": BROWSER_UA,
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


def build_results_email(username: str, signals: dict, top_matches: list) -> str:
    """Build the HTML for the individualized-results email."""
    def esc(s):
        return html.escape(str(s), quote=False) if s is not None else ""

    mbti = esc((signals.get("mbti") or {}).get("inferred_type") or "—").replace("X", "·")
    holland = esc((signals.get("holland") or {}).get("inferred_code") or "—")
    big5 = (signals.get("big_five") or {}).get("inferred_profile") or {}
    big5_txt = esc(" · ".join(f"{k}: {v}" for k, v in big5.items()) or "—")

    rows = ""
    for m in (top_matches or [])[:6]:
        title = esc(m.get("title") or "")
        score = int(round(float(m.get("composite_score") or 0)))
        desc = esc(m.get("description") or "")
        salary = esc(m.get("salary_range") or "")
        rows += (
            '<tr><td style="padding:14px 16px;border-bottom:1px solid #2a3450">'
            f'<div style="font-size:16px;font-weight:700;color:#e9eef7">{title} '
            f'<span style="color:#2dd4bf">({score}%)</span></div>'
            + (f'<div style="font-size:14px;color:#93a0b8;margin-top:3px">{desc}</div>' if desc else "")
            + (f'<div style="font-size:12px;color:#38bdf8;margin-top:4px">{salary}</div>' if salary else "")
            + "</td></tr>"
        )

    return f"""<!DOCTYPE html><html><body style="margin:0;padding:0;background:#0b0f1a;font-family:Arial,Helvetica,sans-serif">
<div style="max-width:560px;margin:0 auto;padding:32px 20px">
  <h1 style="color:#e9eef7;font-size:24px;margin:0 0 4px">Your Anitalmid career map</h1>
  <p style="color:#93a0b8;font-size:14px;margin:0 0 24px">Hi {esc(username)}, here's the individualized breakdown generated from your resume.</p>

  <div style="background:#131a29;border:1px solid #2a3450;border-radius:12px;padding:18px 20px;margin-bottom:20px">
    <div style="font-size:12px;color:#93a0b8;text-transform:uppercase;letter-spacing:.5px;margin-bottom:10px">Detected signals</div>
    <div style="font-size:15px;color:#e9eef7;line-height:1.9">
      <b style="color:#2dd4bf">MBTI</b> {mbti}<br>
      <b style="color:#2dd4bf">Holland</b> {holland}<br>
      <b style="color:#2dd4bf">Big Five</b> {big5_txt}
    </div>
  </div>

  <table style="width:100%;border-collapse:collapse;background:#131a29;border:1px solid #2a3450;border-radius:12px;overflow:hidden">
    {rows}
  </table>

  <p style="color:#93a0b8;font-size:14px;margin:24px 0 0">
    <a href="{BASE_URL}" style="color:#2dd4bf;text-decoration:none;font-weight:700">Return to The Anitalmid Project →</a>
  </p>
</div>
</body></html>"""
