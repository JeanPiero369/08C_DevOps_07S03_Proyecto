#!/usr/bin/env bash
# Genera .env y secrets/ efímeros para levantar el stack en CI.
# Valores aleatorios o de relleno: no son credenciales reales y se destruyen con el runner.
set -euo pipefail
cat > .env <<ENV
POSTGRES_USER=kiwi_ci
POSTGRES_DB=kiwi_ci
DB_PASSWORD=$(openssl rand -hex 16)
JWT_SECRET=$(openssl rand -hex 32)
MAIL_USERNAME=ci@example.com
MAIL_PASSWORD=unused
GOOGLE_API_KEY=unused
GEMINI_MODEL=gemini-2.0-flash
BACKEND_URL=http://localhost:8000
TEACHER_INVITE_CODE=$(openssl rand -hex 12)
ALLOWED_ORIGINS=http://localhost:5174
ENV
mkdir -p secrets
grep '^DB_PASSWORD=' .env | cut -d= -f2- | tr -d '\n' > secrets/db_password.txt
