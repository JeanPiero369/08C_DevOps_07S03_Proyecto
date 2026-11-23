## Resumen de seguridad

| Herramienta | CRITICAL | HIGH | MEDIUM | LOW | INFO | Total |
|---|---:|---:|---:|---:|---:|---:|
| Trivy | 2 | 1 | 84 | 12 | 0 | 99 |
| **Total** | **2** | **1** | **84** | **12** | **0** | **99** |

### Hallazgos CRITICAL / HIGH

| Severidad | Herramienta | Regla | Hallazgo | Ubicación |
|---|---|---|---|---|
| CRITICAL | Trivy | CVE-2026-47884 | org.springframework:spring-webmvc 6.2.19: org.springframework/spring-webmvc: Spring Framework: Remote Code Execution via improper path limitation in XsltView | Java |
| CRITICAL | Trivy | CVE-2026-47890 | org.springframework:spring-webmvc 6.2.19: org.springframework/spring-webmvc: org.springframework/spring-webflux: Spring Framework: Stream corruption in Server-S | Java |
| HIGH | Trivy | CVE-2026-54291 | org.postgresql:postgresql 42.7.11: org.postgresql/postgresql: com.ongres.scram/scram-client: pgjdbc: Man-in-the-middle protection bypass via SCRAM-SHA-256-PLUS  | Java |
