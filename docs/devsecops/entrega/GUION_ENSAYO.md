# Guion de ensayo — Kiwi DevSecOps (12 diapositivas, ~12 min + preguntas)

Reparto sugerido según rol: **Mateo** (frontend/coordinación), **Jean Piero** (DevOps), **Aarón** (backend).

| # | Diapositiva | Expone | Tiempo | Idea clave que debe quedar |
|---|---|---|---|---|
| 1 | Portada | Mateo | 0:20 | Equipo, curso, qué es Kiwi en una frase. |
| 2 | Problema y alcance | Mateo | 1:00 | Plataforma educativa con microservicios (Next.js, gateway FastAPI, Spring Boot, Gemini). Más superficie = más riesgo. |
| 3 | STRIDE | Mateo | 1:00 | 14 amenazas, 6 fronteras de confianza, riesgo = P × I. |
| 4 | 5 amenazas priorizadas | Mateo | 1:15 | E-01 Next.js y E-02 rol docente (20/25), T-01 IDOR (16/25): qué control se aplicó a cada una. |
| 5 | Pipeline CI/CD | Jean Piero | 1:30 | Gate falla con CRITICAL por defecto; sin sesión ZAP o reportes incompletos también falla. Staging efímero. |
| 6 | Herramientas | Jean Piero | 1:00 | SAST, DAST autenticado, secretos, SCA/imágenes, IaC: cada una con su evidencia. |
| 7 | Mitigaciones | Aarón | 1:30 | Código de invitación docente, identidad desde /auth/claims, sin hash en perfiles, límites de PDF, Spring actualizado. |
| 8 | DefectDojo | Jean Piero | 0:45 | Reimportación: 561 mitigados, 36 nuevos, 672 activos. |
| 9 | Antes vs después | Aarón | 1:00 | 1198 → 672 (−43,9 %); CRITICAL 33 → 0; CRITICAL+HIGH −62,4 %. Mencionar la limitación de comparación. |
| 10 | Ambientes y monitoreo | Jean Piero | 0:45 | Local, staging en CI, imágenes en GHCR; sondas con alerta y recuperación probadas. |
| 11 | OWASP SAMM | Aarón | 0:45 | Qué práctica tiene evidencia y cuál es su límite. |
| 12 | Lecciones y cierre | Mateo | 1:00 | ZAP autenticado encontró el hash; "verde" no garantiza cobertura; residuales triados (B101 falso positivo, B104 aceptado, JWT rotados). |

## Preguntas probables (tener respuesta lista)
- **¿Por qué el gate es CRITICAL y no HIGH?** Configurable con `SECURITY_GATE_SEVERITY`; con HIGH el pipeline bloquearía por residuales ya triados. Se demuestra el bloqueo con evidencia (`cierre/github-gate-cierre.png`, `gate-ci.log`).
- **¿Los 672 activos no son demasiados?** La mayoría son LOW/MEDIUM de dependencias e imágenes base; 0 CRITICAL y decisiones documentadas en `cierre/decisiones-equipo.csv`.
- **¿Qué pasó con los JWT en el historial?** Se rotó `JWT_SECRET`; los tokens antiguos devuelven 401. Siguen en el historial pero sin validez.
- **¿Qué falta para producción?** Desplegar las imágenes de GHCR en un entorno real y revisión periódica del modelo de amenazas.

## Checklist del ensayo
- [ ] Una pasada completa cronometrada (meta ≤ 12 min).
- [ ] Transiciones entre expositores sin pausas.
- [ ] Tener abierto un run verde de Actions y DefectDojo por si piden demo.
