## Antes vs después (findings.csv de security_summary.py)

- Antes: `docs/devsecops/baseline-ci/findings.csv` · Después: `docs/devsecops/final-ci/findings.csv`

### Por severidad

| Severidad | Antes | Después | Reducción |
|---|---:|---:|---:|
| CRITICAL | 33 | 0 | 100.0 % |
| HIGH | 382 | 156 | 59.2 % |
| MEDIUM | 485 | 286 | 41.0 % |
| LOW | 275 | 194 | 29.5 % |
| INFO | 23 | 36 | -56.5 % |
| **Total** | **1198** | **672** | **43.9 %** |
| **CRITICAL + HIGH** | **415** | **156** | **62.4 %** |

### Por herramienta

| Herramienta | CRIT antes→después | HIGH antes→después | MEDI antes→después | Total antes | Total después | Reducción |
|---|---:|---:|---:|---:|---:|---:|
| Bandit | 0→0 | 0→0 | 2→2 | 12 | 12 | 0.0 % |
| Checkov | 0→0 | 0→0 | 3→0 | 3 | 0 | 100.0 % |
| Gitleaks | 0→0 | 48→46 | 0→0 | 48 | 46 | 4.2 % |
| OWASP ZAP | 0→0 | 0→0 | 3→3 | 22 | 16 | 27.3 % |
| Semgrep | 0→0 | 46→0 | 2→0 | 49 | 1 | 98.0 % |
| Trivy | 33→0 | 288→110 | 474→281 | 1063 | 597 | 43.8 % |
| pip-audit | 0→0 | 0→0 | 1→0 | 1 | 0 | 100.0 % |

### Hallazgos CRITICAL/HIGH distintos: 179 desaparecen, 0 aparecen
