# Deploy Anitalmid to Render (free tier)

The app is a FastAPI backend + static frontend, containerized via `Dockerfile`.
Render's **Blueprint** (`render.yaml` at the repo root) turns a `git push` into a
live deployment — no manual server setup.

## One-time: free persistent Postgres (Neon)

Render's free Postgres **expires after 30 days**, so use Neon's free tier instead
(persistent, no expiry):

1. Go to https://neon.tech → create a free project → new database `anitalmid`.
2. Copy the **connection string** (starts `postgresql://...`).
3. Change the `postgres://` scheme to `postgresql+psycopg2://` (SQLAlchemy's dialect).

## Deploy via Blueprint

1. Go to https://render.com → **New → Blueprint**.
2. Connect the GitHub repo `CptBaldbeard/The-Anitalmid-Project`.
3. Render reads `render.yaml` and creates the `anitalmid` web service (free plan).
4. Wait for the first build (~3–5 min). It runs `/health` as the health check.

## Configure env vars

Render dashboard → `anitalmid` → **Environment**:

1. `ANITALMID_SECRET` — auto-generated, leave it.
2. `ANITALMID_BASE_URL` — `https://theanitalmidproject.com` (already in `render.yaml`).
3. Add `ANITALMID_DATABASE_URL` → your Neon connection string (`postgresql+psycopg2://…`).
4. Add SMTP vars so verification emails actually send (see below).
5. Click **"Save Changes"** → Render restarts the service automatically.

### Email verification (Resend — recommended)

Accounts must verify their email before they can analyze. Verification emails are
sent via **Resend's HTTP API** (HTTPS/443 — never blocked, unlike SMTP/587):

| Variable | Value |
|---|---|
| `RESEND_API_KEY` | your Resend API key (`re_…`) |
| `SMTP_FROM` | the "from" address, e.g. `no-reply@theanitalmidproject.com` |

Verify `theanitalmidproject.com` in Resend (Domains → Add Domain → add the DNS
records in Cloudflare) so you can send from your own address.

*(An SMTP fallback — `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`,
`SMTP_FROM` — is still supported for other providers, but SMTP/587 can be dropped
by some cloud egress. The Resend HTTP API is preferred.)*

If no transport is configured, the app still works but verification links are only
logged server-side (dev mode) — users can't actually verify via email.

Without `ANITALMID_DATABASE_URL` the app falls back to SQLite, but Render's free
disk is ephemeral — data would be lost on redeploy. Set the Neon URL.

## Point the domain (Cloudflare → Render)

1. Render → `anitalmid` → **Settings → Custom Domains** → add `theanitalmidproject.com`.
2. Copy the DNS target Render gives you (a `*.onrender.com` hostname).
3. Cloudflare → your domain → **DNS**:
   - Type `CNAME`, Name `@`, Target `<render target>`, Proxy **on** (DNS only is fine too).
   - Add a second: Type `CNAME`, Name `www`, Target `<render target>`.
4. Wait for DNS + SSL provisioning (a few minutes to an hour).

## Done

Visit `https://theanitalmidproject.com` — sign up, upload a resume, get matches.

### Free-tier caveats (honest)
- **Sleep after ~15 min idle** → first hit after idle takes ~30–60s to cold-start.
- 512 MB RAM / 0.1 CPU — plenty for this app (the Camoufox expansion is *not*
  deployed here; it degrades gracefully to "no matches").
