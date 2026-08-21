FROM python:3.12-slim

WORKDIR /app

COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

COPY backend/ backend/
COPY frontend/ frontend/

# JWT secret + DB URL are runtime env vars (see README). Default DB = SQLite in /app/backend.
EXPOSE 8300

CMD sh -c "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8300}"
