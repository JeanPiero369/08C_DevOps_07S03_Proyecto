## Antes vs después (findings.csv de security_summary.py)

- Antes: `docs/devsecops/baseline-ci/findings.csv` · Después: `docs/devsecops/final-ci/findings.csv`

### Por severidad

| Severidad | Antes | Después | Reducción |
|---|---:|---:|---:|
| CRITICAL | 33 | 2 | 93.9 % |
| HIGH | 382 | 158 | 58.6 % |
| MEDIUM | 485 | 288 | 40.6 % |
| LOW | 275 | 194 | 29.5 % |
| INFO | 23 | 22 | 4.3 % |
| **Total** | **1198** | **664** | **44.6 %** |
| **CRITICAL + HIGH** | **415** | **160** | **61.4 %** |

### Por herramienta

| Herramienta | CRIT antes→después | HIGH antes→después | MEDI antes→después | Total antes | Total después | Reducción |
|---|---:|---:|---:|---:|---:|---:|
| Bandit | 0→0 | 0→0 | 2→2 | 12 | 12 | 0.0 % |
| Checkov | 0→0 | 0→0 | 3→0 | 3 | 0 | 100.0 % |
| Gitleaks | 0→0 | 48→46 | 0→0 | 48 | 46 | 4.2 % |
| OWASP ZAP | 0→0 | 0→0 | 3→3 | 22 | 16 | 27.3 % |
| Semgrep | 0→0 | 46→0 | 2→1 | 49 | 2 | 95.9 % |
| Trivy | 33→2 | 288→112 | 474→282 | 1063 | 588 | 44.7 % |
| pip-audit | 0→0 | 0→0 | 1→0 | 1 | 0 | 100.0 % |

### Hallazgos CRITICAL/HIGH distintos: 179 desaparecen, 3 aparecen

Aparecen (revisar):

- Trivy · CVE-2026-47884 · org.springframework:spring-webmvc 6.2.19: org.springframework/spring-webmvc: Spr
- Trivy · CVE-2026-47890 · org.springframework:spring-webmvc 6.2.19: org.springframework/spring-webmvc: org
- Trivy · CVE-2026-54291 · org.postgresql:postgresql 42.7.11: org.postgresql/postgresql: com.ongres.scram/s
