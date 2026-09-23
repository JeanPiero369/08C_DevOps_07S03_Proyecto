#!/usr/bin/env bash
# Automatización del proyecto Kiwi
# Uso: ./kiwi.sh {clone|setup|test|up|down|logs|status}
set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/CAMBIAR/08C_DevOps_07S03_Proyecto.git}"
REPO_DIR="${REPO_DIR:-08C_DevOps_07S03_Proyecto}"

clone() {
  if [ -d "$REPO_DIR/.git" ]; then
    echo ">> El repo ya existe, actualizando..."
    git -C "$REPO_DIR" pull --ff-only
  else
    echo ">> Clonando $REPO_URL"
    git clone "$REPO_URL" "$REPO_DIR"
  fi
  echo ">> Listo. Siguiente paso: cd $REPO_DIR && ./kiwi.sh setup"
}

setup() {
  if [ ! -f .env ]; then
    cp .env.example .env
    echo ">> .env creado desde .env.example — complétalo antes de levantar."
  fi
  mkdir -p secrets
  if [ ! -f secrets/db_password.txt ]; then
    pass=$(grep '^DB_PASSWORD=' .env | cut -d= -f2-)
    printf '%s' "$pass" > secrets/db_password.txt
    echo ">> secrets/db_password.txt creado a partir de DB_PASSWORD (.env)"
  fi
}

run_tests() {
  echo ">> Ejecutando pruebas unitarias (ms-orchestrator)"
  cd ms-orchestrator
  if [ ! -d .venv ]; then
    python3 -m venv .venv
  fi
  # shellcheck disable=SC1091
  source .venv/bin/activate
  pip install -q -r requirements-dev.txt
  pytest -v
}

up() {
  setup
  echo ">> Levantando el stack con Docker Compose"
  docker compose up --build -d
  docker compose ps
  echo
  echo "Frontend:     http://localhost:5174"
  echo "Orchestrator: http://localhost:8000/docs"
}

case "${1:-}" in
  clone)  clone ;;
  setup)  setup ;;
  test)   run_tests ;;
  up)     up ;;
  down)   docker compose down ;;
  logs)   docker compose logs -f "${2:-}" ;;
  status) docker compose ps ;;
  *)
    echo "Uso: $0 {clone|setup|test|up|down|logs [servicio]|status}"
    exit 1
    ;;
esac
