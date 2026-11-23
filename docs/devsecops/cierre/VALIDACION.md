# Cierre técnico de Kiwi

Revisión del 22 de noviembre de 2026. Código verificado: `41aaa6190b044a079add02ff058e5e2bda3dfd6c`,
[CI 45067822680](https://github.com/JeanPiero369/08C_DevOps_07S03_Proyecto/actions/runs/45067822680), conclusión **success**. El gate CRITICAL verifica los 15
reportes y aprueba sin CRITICAL. Release se omite porque la rama no es main.
Cambios y entrega en el [PR #13](https://github.com/JeanPiero369/08C_DevOps_07S03_Proyecto/pull/13).

## Rúbrica y alcance

El PDF original exige a–m, incluidos ambientes y monitoreo (j), modelo de
madurez (k), lecciones (l) y recomendaciones (m). Se entregan Word, PDF,
Excel STRIDE, presentación de 12 diapositivas y evidencias. La tabla contiene
siete hallazgos priorizados; el Excel conserva las 20 filas del equipo.
El despliegue demostrado es desarrollo local y staging efímero en CI.

## Actualización de usuarios

- Spring Boot 3.5.16 → 4.0.10, Java 17.
- Spring Framework 7.0.11, Tomcat 11.0.27, PostgreSQL JDBC 42.7.14 y Jackson
  databind 3.1.8 administrados por el BOM de Boot.
- Se adaptan matchers, DaoAuthenticationProvider y RoleHierarchy para Spring
  Security 7. Jackson 3 conserva los valores JSON de Jackson 2 mediante la
  opción oficial de compatibilidad.
- CVE-2026-47884 y CVE-2026-47890 ya no aparecen. Tampoco el aviso JDBC
  CVE-2026-54291 de 42.7.11. No se aceptaron riesgos para conseguir el verde,
  no se excluyeron reglas ni se redujo el umbral.

## Validación ejecutada

| Comprobación | Resultado |
|---|---|
| pytest gateway | 31 correctas |
| pytest quiz | 6 correctas |
| JUnit seguridad | 10 correctas |
| Integración BootMigrationTest | 3 correctas con HTTP real y PostgreSQL aislado |
| Validadores de reportes y URLs | 3 correctas |
| Total automatizado | 53 pruebas, sin fallos ni omisiones en las suites seleccionadas |
| E2E local tras actualizar | 16 comprobaciones correctas |
| Docker Compose | 5 imágenes construidas y 6 servicios Kiwi healthy |
| DAST de CI | API autenticada y frontend analizados |
| Monitoreo | 2 sondas sanas; caída, alerta firing y recuperación comprobadas |
| Rotación local | Token anterior 401; nuevo login y perfil 200 |

BootMigrationTest comprueba login, serialización sin password, rechazo de token
alterado, invitación docente, rol decidido por servidor y PATCH sin cambiar
rol, monedas ni contraseña. Usa una base temporal; no modifica la base local.
El CI ejecuta Maven en Java 17 con acceso al Docker del runner para Testcontainers.
Los logs de suites están resumidos en `pruebas-ci.json`.

## Resultados y comparabilidad

El corte de código 45067822680 registra **672 detecciones**: 0 CRITICAL, 156 HIGH, 286 MEDIUM, 194 LOW, 36 INFO.
Línea base oficial: 1198 en 44965126475. Reducción observada: 43.9 %.
CRITICAL: 33 → 0. Son ocurrencias de herramientas, no vulnerabilidades únicas.

La evolución anterior se conserva en los históricos: 667 en 44972251652,
663 en 45060902475 y 677 en 45062675759. Este último agregó 14 registros
UNKNOWN de libseccomp normalizados como INFO. Las bases de vulnerabilidades,
imágenes, versiones y cobertura pueden cambiar entre ejecuciones.
La línea base oficial ZAP no autenticó; el run adicional 44966862163 sí lo hizo
y encontró el hash BCrypt. El DAST actual autenticado no presenta esa alerta.

El escaneo local de solo usuarios da 95 detecciones (0 CRITICAL, 0 HIGH,
83 MEDIUM, 12 LOW); no se suma a las cifras globales del CI. Ver
`ms-user-spring4-local.json`. El resultado local anterior de 99 se conserva
como evidencia histórica de Tomcat 10.1.62, no como inventario actual.

## DefectDojo propio

Instancia local http://localhost:8080, versión 3.4.304. Producto Kiwi,
engagement CI/CD main. Se reimporta el corte 45067822680 sobre los mismos 15 tests,
sin crear nuevos tests ni modificar aceptaciones del equipo.

- Línea base importada: 1197 activos.
- Corte actual: 672 activos, distribución {'High': 156, 'Medium': 286, 'Low': 195, 'Info': 35}.
- 561 mitigados y 36 registros nuevos acumulados.
- Conciliación: 1197 + 36 − 561 = 672.

Las diferencias LOW/INFO entre CSV y DefectDojo proceden de los parsers. Esta
instancia no hereda el triage de la computadora de Mateo. Los estados propuestos
en decisiones-equipo.csv no son aprobaciones ni aceptaciones registradas.

## Rotación y pendientes del equipo

El usuario confirmó que Kiwi se ejecuta solo en computadoras del equipo.
Se rotó JWT_SECRET en esta computadora y se comprobó la invalidación de la
sesión anterior; ver `rotacion-jwt-local.json`. No se muestra ni comparte la
clave. Cada otro integrante debe seguir `security/README.md` y confirmar
su resultado. La prueba local no acredita las otras instalaciones.

Permanecen hallazgos HIGH y de otras severidades: revisar `RESIDUALES.md` y
`triage-propuesto.csv`. No se purgó historial ni se agregaron allowlists.
Siguen pendientes autorización por pertenencia al aula, rate limiting de IA,
tokens en localStorage, auditoría y validación de todos los flujos de negocio.
Gemini y SMTP no se probaron con credenciales reales. No se midieron carga,
capacidad concurrente ni resultados pedagógicos.

Orden propuesto de integración tras revisión: #13 en fix/security-mitigations,
después #12 en feat/devsecops-pipeline y #11 en main. No se han fusionado.
GHCR distribuye imágenes; no acredita una instalación productiva.
SonarCloud y la importación automática a DefectDojo siguen sin credenciales
remotas configuradas; el job opcional se omite y la importación se ejecuta
localmente. No se cambiaron settings, secretos ni variables del repositorio.

## Referencias

- https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-4.0-Migration-Guide
- https://spring.io/security/cve-2026-47884/
- https://spring.io/security/cve-2026-47890/
- https://docs.spring.io/spring-boot/4.0/system-requirements.html
- https://tomcat.apache.org/security-11.html
- https://prometheus.io/docs/guides/multi-target-exporter/
- https://owaspsamm.org/model/
