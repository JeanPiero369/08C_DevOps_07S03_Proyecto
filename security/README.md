# DevSecOps · Kiwi

Pipeline: `.github/workflows/devsecops.yml` (GitHub Actions).

```
secret-scan ─┐
unit-tests ──┴─► build (imágenes + Trivy image) ─► dast (deploy:staging efímero + OWASP ZAP) ─┐
sast (Semgrep + Bandit) · sonarcloud (opcional) · sca (Trivy fs + pip-audit) · iac (Trivy + Checkov) ─┤
                                                                                                    ├─► defectdojo (import)
                                                                                                    └─► security-gate ─► release (GHCR, solo main)
```

| Etapa | Herramienta | Reporte | Tipo en DefectDojo |
|---|---|---|---|
| Secret scanning | Gitleaks 8.30.1 (historial completo, `--redact`) | `gitleaks.json` | Gitleaks Scan |
| SAST | Semgrep (p/default, p/owasp-top-ten, p/secrets) | `semgrep.json` | Semgrep JSON Report |
| SAST | Bandit (servicios Python) | `bandit.json` | Bandit Scan |
| SAST (opcional) | SonarCloud | panel de SonarCloud | — |
| SCA | Trivy fs (npm, Maven, pip) | `trivy-fs.json` | Trivy Scan |
| SCA | pip-audit (requirements sin versión fija) | `pip-audit-*.json` | pip-audit Scan |
| IaC | Trivy config + Checkov (Dockerfiles, GitHub Actions) | `trivy-config.json`, `checkov.json` | Trivy Scan / Checkov Scan |
| Contenedores | Trivy image (5 imágenes) | `trivy-image-*.json` | Trivy Scan |
| DAST | OWASP ZAP API scan (OpenAPI del orchestrator, autenticado) + baseline (frontend) | `zap-*.xml/json/html` | ZAP Scan |

Los hallazgos de los escáneres no fallan sus jobs por severidad: ese umbral lo aplica
`security-gate`, que consolida con `security/scripts/security_summary.py`. La ausencia de reportes y el fallo de autenticación de ZAP sí bloquean
la validación. `verify_reports.py` exige los 15 JSON previstos antes de consolidar.
El valor predeterminado del gate es CRITICAL y el release espera pruebas y escaneos.

## Configuración en GitHub (Settings → Secrets and variables → Actions)

| Nombre | Tipo | Uso |
|---|---|---|
| `DEFECTDOJO_URL` | Secret | URL pública de DefectDojo, sin `/` final (opcional) |
| `DEFECTDOJO_TOKEN` | Secret | API v2 key del usuario de DefectDojo (opcional) |
| `SONAR_TOKEN` | Secret | Token de SonarCloud (opcional) |
| `SONAR_ORGANIZATION`, `SONAR_PROJECT_KEY` | Variables | Proyecto en SonarCloud (opcional) |
| `SECURITY_GATE_SEVERITY` | Variable | Sin definir = CRITICAL. Puede fijarse a HIGH para endurecer el umbral. |

## DefectDojo local

```bash
git clone https://github.com/DefectDojo/django-DefectDojo && cd django-DefectDojo
docker compose up -d
docker compose logs initializer | grep "Admin password:"   # usuario: admin
# http://localhost:8080 → menú de usuario → API v2 Key
```

Dos formas de cargar los reportes:

1. **Automática desde el pipeline**: expón DefectDojo con un túnel temporal
   (`cloudflared tunnel --url http://localhost:8080`) y guarda la URL y el token en los secrets
   `DEFECTDOJO_URL` y `DEFECTDOJO_TOKEN`.
2. **Manual desde tu máquina** con los artefactos del run:

```bash
gh run download <run-id> -p 'report-*' -D reports
DEFECTDOJO_URL=http://localhost:8080 DEFECTDOJO_TOKEN=<api-key> DD_BRANCH=main \
  python security/scripts/defectdojo_upload.py reports
```

El script usa `reimport-scan` con `auto_create_context` y `close_old_findings`: la primera carga crea
producto **Kiwi**, engagement **CI/CD &lt;rama&gt;** y un test por herramienta; las siguientes actualizan esos
tests y marcan como mitigado lo que ya no aparece, lo que permite comparar antes y después.

## Ejecución local de las herramientas

```bash
python security/scripts/security_summary.py docs/devsecops/baseline --markdown /tmp/summary.md
```

La línea base local (main @ `0ef43c8`) y el modelado STRIDE están en `docs/devsecops/`.

## Secretos expuestos en el historial (S-01 / HIGH-001)

Las colecciones Bruno tenían 24 JWT reales (46 ocurrencias) versionados en
`ms-orchestrator/ms-orquestrator/**` y `ms-user/api-endpoints/**`
(commits `7327962`, `f279c23`).

- **Estado del árbol de trabajo:** los tokens se reemplazaron por `{{jwt}}`, una
  *secret variable* del entorno de Bruno (`environments/kiwi.bru`, bloque
  `vars:secret`). Bruno guarda su valor fuera del repositorio; pega tu token en
  la interfaz de Bruno y no se versiona.
- **Vigencia:** los 24 tokens son HS256 y expiraron entre el 31/05/2025 y el
  18/06/2025 (`exp`), por lo que no sirven para iniciar sesión. Sin embargo,
  siguen permitiendo un ataque de fuerza bruta offline contra la clave HMAC.
- **Acción obligatoria — rotar `JWT_SECRET`** en cada entorno:
  ```bash
  # genera un secreto nuevo de 256 bits y reemplázalo en .env
  openssl rand -hex 32
  ```
  Tras la rotación, todos los tokens firmados con la clave anterior dejan de
  validar (los usuarios vuelven a iniciar sesión).
- **Historial:** Gitleaks seguirá reportando los commits antiguos mientras no se
  purgue el historial (`git filter-repo`), algo que reescribe `main` y requiere
  la aprobación del equipo. La alternativa sin reescritura es un
  `.gitleaksignore` con los *fingerprints* de esos 24 tokens, **solo después** de
  confirmar la rotación, justificado como "tokens expirados e invalidados por la
  rotación de la clave".

## Variables de entorno nuevas

| Variable | Servicio | Propósito |
|---|---|---|
| `TEACHER_INVITE_CODE` | ms-user | Código para registrarse como docente (E-02). Vacío = registro docente deshabilitado. |
| `ALLOWED_ORIGINS` | gateway, ms-quiz | Orígenes permitidos por CORS, separados por coma (I-01). Por defecto `http://localhost:5174`. |
| `MAX_PDF_SIZE_MB` / `MAX_PDF_PAGES` | ms-quiz | Límites del PDF para generar quizzes (D-01). Por defecto 5 MB y 30 páginas. |
