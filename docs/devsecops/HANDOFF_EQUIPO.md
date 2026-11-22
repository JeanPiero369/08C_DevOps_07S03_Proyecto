# Traspaso al equipo · Proyecto final DevSecOps «Kiwi» (IS4024 · UTEC)

Estado al **22/11/2026**. Este documento es autosuficiente: todo lo necesario
para continuar está en el repositorio (no depende de la laptop de nadie).

## 1. Dónde está cada cosa

| Qué | Dónde |
|---|---|
| Rama de trabajo actual | **`fix/security-mitigations`** (contiene todo; partir desde aquí) |
| PR 1 · pipeline + STRIDE + línea base | [#11](https://github.com/JeanPiero369/08C_DevOps_07S03_Proyecto/pull/11) `feat/devsecops-pipeline` → `main` (sin merge) |
| PR 2 · mitigaciones | [#12](https://github.com/JeanPiero369/08C_DevOps_07S03_Proyecto/pull/12) `fix/security-mitigations` → `feat/devsecops-pipeline` (apilado, sin merge) |
| Pipeline | `.github/workflows/devsecops.yml` (10 jobs) |
| Scripts | `security/scripts/` (resumen/gate, carga a DefectDojo, comparación antes/después) |
| Guía de seguridad y variables nuevas | `security/README.md` |
| Modelo STRIDE | `docs/devsecops/stride/` (`kiwi_stride.drawio`, `.png`, `.xlsx`) |
| Línea base local (referencia) | `docs/devsecops/baseline/` |
| **Línea base oficial de CI** | `docs/devsecops/baseline-ci/` (run 44965126475) |
| **Resultado final de CI** | `docs/devsecops/final-ci/` (run 44972251652) + `comparacion.md` |
| Capturas de DefectDojo (línea base) | `docs/devsecops/evidencias/01…06-*.png` |
| Informe parcial (para el punto a) | `Informe Parcial (1).pdf` en la raíz |

Runs de GitHub Actions relevantes (sus artifacts duran 30 días):

| Run | Qué es |
|---|---|
| `44965126475` | **Línea base oficial** (commit `7736ff3`) |
| `44966862163` | Primer run con ZAP autenticado (detectó el hash BCrypt expuesto) |
| `44972251652` | **Final** sobre `fix/security-mitigations` |

## 2. Resultados (cifras reales de los reportes)

| Severidad | Línea base CI | Final | Reducción |
|---|---:|---:|---:|
| CRITICAL | 33 | 6 | 81,8 % |
| HIGH | 382 | 158 | 58,6 % |
| MEDIUM | 485 | 287 | 40,8 % |
| LOW | 275 | 194 | 29,5 % |
| INFO | 23 | 22 | 4,3 % |
| **Total** | **1198** | **667** | **44,3 %** |
| CRITICAL + HIGH | 415 | 164 | 60,5 % |

Detalle por herramienta en `docs/devsecops/final-ci/comparacion.md`
(regenerable con `python security/scripts/compare_baseline.py ANTES.csv DESPUES.csv`).

DefectDojo (instancia local de Mateo, ya no accesible): 1197 hallazgos importados
de la línea base; tras el triage, 1194 activos (1 falso positivo, 2 riesgos aceptados).
Las capturas están en `docs/devsecops/evidencias/`.

## 3. Lo que ya está hecho

**Fase 1 · Pipeline (puntos d, e, i):** 10 jobs en GitHub Actions — Gitleaks,
pytest, Semgrep + Bandit, SonarCloud (opcional), Trivy fs + pip-audit, Trivy
config + Checkov, build + Trivy image, DAST con ZAP **autenticado** sobre un
staging efímero, carga a DefectDojo (opcional) y gate + release a GHCR. Todos en verde.

**Fase 2 · DefectDojo (punto f):** script `defectdojo_upload.py` validado contra
una instancia real (los 7 `scan_type` coinciden). Importados los 15 reportes de la
línea base, triage hecho, 6 capturas guardadas.

**Fase 3 · STRIDE y tabla (puntos b, c, g):** Excel con 14 amenazas (Top 5:
E-01, E-02, T-01, S-01, D-01), 20 mitigaciones priorizadas, hoja de línea base
con bloques local / CI / DefectDojo. Diagrama con I-03 y E-04 agregados.

**Fase 4 · Mitigaciones (PR #12, 20 commits):**
- Dependencias: next 15.5.29; fuera genkit/firebase; Spring Boot 3.5.16 + Tomcat
  10.1.56 + Jackson 2.21.7; java-jwt 4.6.2; PyPDF2 → pypdf; npm audit fix;
  versiones fijadas en Python; imágenes node:22-alpine sin npm/yarn en runtime.
- Código: registro docente con **código de invitación** (`TEACHER_INVITE_CODE`);
  identidad tomada del token en el gateway (IDOR → 403); roles en endpoints
  sensibles; el hash de contraseña ya no se devuelve; PATCH /me sin asignación
  masiva; CORS con lista blanca; 5xx genéricos; logs DEBUG/SQL solo en perfil
  `dev`; límites de tamaño y páginas del PDF; JWT de Bruno → variable secreta.
- Infra: cabeceras CSP y anti-clickjacking; HEALTHCHECK en todas las imágenes.
- Pruebas: gateway 29/29, ms-user 10/10 (JUnit), ms-quiz 6/6; stack completo
  levantado con 15 comprobaciones end-to-end OK.
- Bugs latentes encontrados y corregidos: ms-quiz no arrancaba en staging
  (SQLAlchemy 2.1 sin greenlet), axios era dependencia fantasma, ms-user
  importaba `HttpStatus` de testcontainers, el frontend instalaba TypeScript
  desde internet al arrancar, peticiones sin token devolvían 500.

## 4. Lo que falta (en orden)

### Fase 5 · Antes vs después (punto h)
1. **Quick win:** en `ms-user/pom.xml` cambiar `<tomcat.version>10.1.56</tomcat.version>`
   a `10.1.59` (corrige 4 de los 6 CRITICAL restantes). Push y nuevo run.
2. Los 2 CRITICAL de `spring-webmvc 6.2.19` (CVE-2026-47884/47890) solo se corrigen
   con Spring 7 (Spring Boot 4). La app **no usa XsltView** → documentar como
   **riesgo aceptado** con esa justificación (o migrar a Spring Boot 4 si hay tiempo).
3. Levantar DefectDojo propio (ver §5), importar la línea base (run 44965126475)
   y **reimportar el final en el mismo engagement `CI/CD main`** (`DD_BRANCH=main`)
   para que DefectDojo marque como mitigado lo que ya no aparece. Capturas antes/después.
4. Repetir el triage en DefectDojo: falso positivo del Gitleaks `aws-access-token`
   en `docs/devsecops/baseline/pip-audit-ms-quiz.json` (URL prefirmada pública);
   riesgo aceptado para Bandit B104 (bind 0.0.0.0 en contenedor) y spring-webmvc.
5. **Gate (requiere a Jean Piero, dueño del repo):** crear la variable de repositorio
   `SECURITY_GATE_SEVERITY=CRITICAL` (Settings → Secrets and variables → Actions →
   Variables) y mostrar que el job `security-gate` bloquea con los CRITICAL que
   queden. Capturas del gate bloqueando y, si se llega a 0 CRITICAL, en verde.
6. Clasificar lo que quede sin corregir: postcss/zod del frontend (requieren Next 16 /
   zod 4), paquetes Debian sin parche (util-linux, sqlite) → pendiente o aceptado, con justificación.
7. Actualizar el Excel: hoja «Linea base» con el bloque final y la columna Estado
   de «Mitigaciones» (Mitigado / Aceptado / Pendiente).

### Seguridad que requiere decisión del equipo
8. **Rotar `JWT_SECRET`** en todos los `.env` (`openssl rand -hex 32`). Los 24 JWT
   del historial expiraron (2025) pero permiten atacar la clave offline.
9. Purga del historial (`git filter-repo`) **solo con aprobación de Mateo y Jean Piero**;
   si no, `.gitleaksignore` por fingerprint tras confirmar la rotación (ver `security/README.md`).
10. Merge de los PR: primero #12 en `feat/devsecops-pipeline`, luego #11 en `main`
    (lo hace el dueño del repo). Tras el merge a `main` corre el job `release` (GHCR).

### Fase 6 · Diagrama CI/CD (punto i)
11. Diagrama de los 10 jobs con sus `needs`, herramientas y artefactos, más
    DefectDojo y GHCR (draw.io o Mermaid → PNG). Captura del grafo real de un run
    en GitHub Actions (pestaña Summary del run).

### Fase 7 · Informe y exposición
12. Links públicos: usar los de GitHub para `kiwi_stride.drawio` y `kiwi_stride.xlsx`.
13. Informe PDF con portada, índice y puntos a–k + anexos (YAML completo y links).
14. PPT de 10–12 diapositivas. Ensayo y reparto de partes.

## 5. Cómo trabajar en tu laptop

```bash
git clone https://github.com/JeanPiero369/08C_DevOps_07S03_Proyecto.git
cd 08C_DevOps_07S03_Proyecto
git checkout fix/security-mitigations
```

- **Levantar Kiwi:** `bash security/scripts/ci_env.sh` genera un `.env` y
  `secrets/` de prueba (valores aleatorios, ignorados por git); luego
  `docker compose up -d --build`. Frontend en http://localhost:5174, API en
  http://localhost:8000. Para registrarte como docente usa el
  `TEACHER_INVITE_CODE` del `.env`.
- **Pruebas:** `cd ms-orchestrator && pip install -r requirements-dev.txt && pytest`;
  `cd ms-quiz && pip install -r requirements-dev.txt && pytest`; ms-user con
  `mvn test -Dtest=AuthServiceSecurityTest` (o dentro de `maven:3.9.4-eclipse-temurin-17`).
- **Reportes de un run:** `gh run download <RUN_ID> -p 'report-*' -D reports-<nombre>`
  (no subir esas carpetas al repo).
- **DefectDojo:**
  ```bash
  git clone https://github.com/DefectDojo/django-DefectDojo   # fuera del repo de Kiwi
  cd django-DefectDojo && docker compose up -d
  docker compose logs initializer | grep "Admin password:"
  ```
  UI en http://localhost:8080 (usuario `admin`). Saca la API key en tu perfil
  (API v2 Key) y **no la guardes en el repo**. Importar:
  ```bash
  DEFECTDOJO_URL=http://localhost:8080 DEFECTDOJO_TOKEN=<tu_key> DD_BRANCH=main \
    python security/scripts/defectdojo_upload.py reports-ci-baseline
  ```
- **Comparar dos runs:** `python security/scripts/compare_baseline.py docs/devsecops/baseline-ci/findings.csv docs/devsecops/final-ci/findings.csv`

## 6. Reglas del proyecto

- Conventional Commits; ramas `feat/*` y `fix/*`; PR hacia la rama base; nada directo a `main`.
- Los escáneres nunca fallan su job; solo bloquea `security-gate`. **Nunca** modificar
  el gate, un validador o una prueba solo para que pase.
- Nunca subir `.env`, `secrets/`, tokens, API keys ni reportes sin redactar.
- Ninguna cifra inventada: todo número del informe sale de un reporte o de DefectDojo.
  Separar siempre línea base local, línea base de CI y resultado final; y lo que
  detectó una herramienta de lo que es revisión manual.
- Requieren permiso explícito del equipo: merge de PR, push a `main`, reescribir
  historial, borrar ramas, cambiar settings del repo y crear secrets/variables.

## 7. Prompt para Claude Code

Copia esto en Claude Code, abierto en la carpeta del repositorio clonado:

```text
Eres el ingeniero DevSecOps de nuestro proyecto final del curso IS4024 DevOps (UTEC):
"Kiwi", una plataforma educativa con frontend Next.js, gateway FastAPI y microservicios
Spring Boot (ms-user), Express+Prisma (ms-classroom) y FastAPI (ms-quiz), sobre PostgreSQL
con docker compose. Repositorio: https://github.com/JeanPiero369/08C_DevOps_07S03_Proyecto

Antes de hacer nada:
1. Lee docs/devsecops/HANDOFF_EQUIPO.md completo (estado, cifras, qué falta y reglas),
   security/README.md y .github/workflows/devsecops.yml.
2. Verifica el entorno (git, gh auth status, docker info, python3) y que estés en la rama
   fix/security-mitigations actualizada (git pull).

Contexto clave:
- Las fases 1 a 4 están hechas (pipeline, DefectDojo, STRIDE, mitigaciones). Los PR #11 y #12
  están abiertos y sin merge.
- Línea base oficial de CI: run 44965126475 (1198 hallazgos, 33 CRITICAL).
  Final actual: run 44972251652 (667 hallazgos, 6 CRITICAL). Las cifras y la comparación
  están en docs/devsecops/baseline-ci/ y docs/devsecops/final-ci/.
- DefectDojo no está compartido: hay que levantar una instancia local propia (sección 5 del handoff).

Continúa desde la sección 4 del handoff ("Lo que falta"), empezando por la tarea que yo te
indique (si no te indico, empieza por la 1: Tomcat 10.1.59). Trabaja una tarea a la vez:
explícame en pocas líneas qué vas a hacer, hazlo, verifícalo de verdad (pruebas, build o run de
CI) y repórtame qué hiciste, qué archivos tocaste, qué pruebas corriste, resultados con cifras
y qué queda pendiente. Después espera mi aprobación para seguir.

Reglas: respóndeme en español; Conventional Commits; nunca subas .env, secrets/, tokens ni API
keys; nunca modifiques el gate, un validador o una prueba solo para que pase; no inventes
cifras (cada número sale de un reporte o de DefectDojo). Pídeme permiso explícito antes de:
merge de PR, push a main, reescribir historial, borrar ramas, cambiar settings del repo o
crear secrets/variables.
```
