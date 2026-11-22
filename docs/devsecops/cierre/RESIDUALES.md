# Clasificación de hallazgos residuales

Corte vigente de código: run 45067822680. La primera validación de cierre fue 45059948900. Las cifras
son detecciones normalizadas, con duplicación posible entre filesystem e imagen.
El último resultado aplicable figura en `ci-cierre.json` y `final-ci/findings.csv`.

| Grupo | Evidencia del run | Clasificación y acción |
|---|---|---|
| Spring webmvc | Los 2 CRITICAL anteriores ya no aparecen en 45067822680 | Corregidos mediante Boot 4.0.10 / Framework 7.0.11, sin excepciones. Gate aprobado. |
| JWT históricos | 46 detecciones HIGH de Gitleaks | Pendiente. Árbol actual sin JWT reales en Bruno, clave local rotada y token anterior rechazado con 401; confirmar las otras computadoras. No ocultar con allowlist ni reescribir historia sin acuerdo del equipo. |
| PostgreSQL JDBC | Las 2 detecciones HIGH anteriores de CVE-2026-54291 ya no aparecen | Actualizado a 42.7.14 mediante Boot 4.0.10 y verificado en 45067822680. |
| PostCSS | 8 detecciones, incluidas HIGH, paquete 8.4.31 | Pendiente. Trivy indica parches 8.5.10, 8.5.12 y 8.5.18 según el aviso. Revisar dependencia transitiva de Next y validar una actualización compatible. No asumir sin probar que exige Next 16. |
| zod | No aparece en findings.csv de este run | No es un hallazgo confirmado en esta evidencia. La mención del traspaso no justifica inventar una fila activa ni afirmar mitigación sin identificar el aviso original. |
| util-linux | 132 detecciones entre paquetes y dos imágenes Python | Pendiente, no falso positivo automático. El reporte no indica versión corregida. Reducir superficie y privilegios, seguir avisos de Debian y reconstruir cuando exista parche. |
| SQLite | 28 detecciones en paquetes del sistema de imágenes Python | Pendiente. No hay versión corregida en esos reportes. Revisar alcance real y disponibilidad de actualizaciones, sin deducir no aplicabilidad por usar PostgreSQL. |
| Bandit B104 | 2 detecciones MEDIUM de bind 0.0.0.0 | Aceptación propuesta para red de contenedores. Verificar puertos y redes. Definir responsable y revisión antes de aplicarla en la instancia propia. |
| Otros Bandit LOW | 10 detecciones | Pendiente de revisión individual. No aceptar por severidad baja ni por ejecutar dentro de Docker. |
| ZAP | 16 alertas agrupadas | Pendiente de triage individual. Las cabeceras añadidas no eliminan todas las advertencias de CSP y recursos externos. |
| Semgrep CSRF | INFO en ms-classroom/src/app.js | Pendiente de análisis del mecanismo de autenticación y exposición. No adoptar csurf solo por el mensaje genérico de una regla. |

La primera ejecución también detectó un MEDIUM nuevo en `monitor_staging.py`
(`dynamic-urllib-use-detected`). Se reemplazó el cliente por HTTPConnection o
HTTPSConnection, se rechazaron otros esquemas y credenciales embebidas y se
añadió una prueba de regresión. El reporte SAST del run 45060902475, commit 5543e31, confirma que desapareció.
No se agregó ninguna exclusión de reglas.

Los propietarios y fechas de `decisiones-equipo.csv` son propuestas para la
revisión del equipo, no acuerdos ni aceptaciones ya registradas en DefectDojo.
