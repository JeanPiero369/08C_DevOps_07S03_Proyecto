# Kiwi — Plataforma educativa gamificada

Plataforma de aulas virtuales donde docentes crean quizzes (manuales o generados con IA a partir de PDF/texto) y estudiantes los resuelven ganando monedas y personajes.

## Arquitectura

| Servicio | Tecnología | Puerto interno | Expuesto al host |
|---|---|---|---|
| `frontend` | Next.js | 3000 | `5174` |
| `orchestrator` | FastAPI (API Gateway) | 8000 | `8000` |
| `users` | Spring Boot | 8080 | No |
| `classrooms` | Express + Prisma | 3000 | No |
| `quices` | FastAPI + Gemini | 8001 | No |
| `db` | PostgreSQL 13 | 5432 | No |

Redes: `web` (frontend ↔ orchestrator), `backend` (orchestrator ↔ microservicios) y `data` (`internal: true`, microservicios ↔ PostgreSQL). La base de datos no tiene salida a internet ni puerto publicado.

## Prerrequisitos

- Git
- Docker Desktop (Docker Engine 24+ con Docker Compose v2)
- Python 3.11+ (solo para ejecutar las pruebas fuera de Docker)

## Configuración

```bash
# Crear manualmente el archivo .env con las variables requeridas
./kiwi.sh setupD
```

`Los archivos `.env`, `.env.example` y el directorio `secrets/` están excluidos mediante `.gitignore`, por lo que las credenciales no se versionan.

## Levantar la aplicación

```bash
./kiwi.sh up
```

- Frontend: http://localhost:5174
- API (Swagger): http://localhost:8000/docs

Detener: `./kiwi.sh down`

## Pruebas unitarias

Las pruebas están en `ms-orchestrator/tests/` (pytest + respx para simular el microservicio de usuarios).

Comando exacto:

```bash
./kiwi.sh test
```

O manualmente:

```bash
cd ms-orchestrator
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -v
```

## Script de automatización

`kiwi.sh` en la raíz:

| Comando | Acción |
|---|---|
| `./kiwi.sh clone` | Clona (o actualiza) el repositorio |
| `./kiwi.sh setup` | Crea `.env` y el secreto de la DB |
| `./kiwi.sh test` | Ejecuta las pruebas unitarias |
| `./kiwi.sh up` | Construye y levanta el stack |
| `./kiwi.sh down` | Detiene el stack (conserva datos) |
| `./kiwi.sh logs [servicio]` | Logs en vivo |
| `./kiwi.sh status` | Estado de los contenedores |

## Flujo de trabajo Git

- Ramas: `main` (estable) y `feature/<descripcion>` de corta duración, integradas vía Pull Request.
- Mensajes con [Conventional Commits](https://www.conventionalcommits.org/): `feat`, `fix`, `docs`, `test`, `chore`, `ci`, `refactor`.
