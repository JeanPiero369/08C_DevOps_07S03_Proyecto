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

Los escáneres **no fallan el job**: el único punto de bloqueo es `security-gate`, que consolida todo con
`security/scripts/security_summary.py` y publica la tabla en el resumen del run.

## Configuración en GitHub (Settings → Secrets and variables → Actions)

| Nombre | Tipo | Uso |
|---|---|---|
| `DEFECTDOJO_URL` | Secret | URL pública de DefectDojo, sin `/` final (opcional) |
| `DEFECTDOJO_TOKEN` | Secret | API v2 key del usuario de DefectDojo (opcional) |
| `SONAR_TOKEN` | Secret | Token de SonarCloud (opcional) |
| `SONAR_ORGANIZATION`, `SONAR_PROJECT_KEY` | Variables | Proyecto en SonarCloud (opcional) |
| `SECURITY_GATE_SEVERITY` | Variable | Vacío = modo línea base (no bloquea). `CRITICAL` o `HIGH` = bloquea el release |

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
