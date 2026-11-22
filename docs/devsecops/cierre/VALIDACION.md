# Cierre técnico de Kiwi

Revisión del 22 de noviembre de 2026. Base: `fix/security-mitigations`,
commit `64bf056af86f195882988c2044c7f6fdcf851d2e`. Los cambios técnicos están en
el [PR #13](https://github.com/JeanPiero369/08C_DevOps_07S03_Proyecto/pull/13).
Último CI completo: [45060902475](https://github.com/JeanPiero369/08C_DevOps_07S03_Proyecto/actions/runs/45060902475),
commit `5543e31e88fc93043c80edd36ec626e6f3159b5a`. Pruebas, análisis, build,
monitoreo y DAST correctos; gate bloqueado por dos CRITICAL Spring.
## Rúbrica original

El PDF «Proyecto - Informe final.pdf» pide los puntos **a–m**. El traspaso omitió
los requisitos de múltiples ambientes y monitoreo (j) y modelo de madurez (k).
La tabla exige al menos cinco hallazgos priorizados por severidad, no cinco de
cada severidad. El informe y la exposición deben usar esta rúbrica original.

## Evidencia ejecutada

| Comprobación | Resultado |
|---|---|
| pytest gateway | 31 pruebas correctas, incluidas 2 regresiones de PATCH /me |
| pytest ms-quiz | 6 pruebas correctas |
| JUnit ms-user con Java 17 y Tomcat 10.1.62 | 10 pruebas correctas |
| Integridad de reportes | 3 pruebas con casos de ausencia, corrupción, duplicación y ZAP sin sitio |
| Docker Compose | 5 imágenes construidas y 6 servicios Kiwi healthy |
| E2E | 16 comprobaciones correctas, ver e2e.json |
| Prometheus y reglas | promtool valida configuración y 2 reglas |
| Monitoreo | 2 sondas HTTP en 1, caída del frontend, alerta firing y recuperación |
| Excel | 90 fórmulas previas conservadas, totales recalculados y vistas revisadas |
| Gate real local | Exit 1 en GitHub con 2 CRITICAL del run de cierre |

La primera ejecución Maven con el Java predeterminado del host falló durante
la compilación de clases Lombok. Con Java 17, que es la versión del proyecto,
las 10 pruebas pasan. No se cambió el código para ocultar el fallo del entorno.

## Resultados y comparabilidad

Los reportes originales descargados reproducen exactamente 1198 detecciones
en el run 44965126475, 667 en 44972251652 y 663 en el cierre 45060902475.
La reducción agregada inicial a cierre es 44,7 %. CRITICAL: 33 a 2 (93,9 %).
Son ocurrencias de herramientas y componentes, no vulnerabilidades únicas.

La línea base oficial de ZAP no logró autenticarse. La evidencia adicional del
run 44966862163 sí está autenticada y detecta la divulgación BCrypt (10097).
Comparar esa evidencia con ZAP final permite evaluar la eliminación del hash.
No atribuir toda la diferencia agregada exclusivamente a cambios en el código:
varían cobertura, versiones de componentes y bases de vulnerabilidades.

El escaneo local de **solo ms-user** con Trivy 0.70.0 y Tomcat 10.1.62 devuelve
99 detecciones: 2 CRITICAL, 1 HIGH, 84 MEDIUM y 12 LOW. La imagen histórica de
CI tenía 79 detecciones y 6 CRITICAL. La imagen base actual y la arquitectura
local difieren del CI histórico, por lo que no constituye un nuevo total final
del proyecto. Los 4 CRITICAL de Tomcat anteriores ya no aparecen en este escaneo.

## DefectDojo propio

Instancia local en http://localhost:8080, versión de la imagen 3.4.304.
Producto Kiwi y engagement `CI/CD main`. Se importó la línea base y se reimportó
el resultado histórico posterior y el último cierre sobre los **mismos 15 tests**, conservando IDs.

- Antes: 1197 activos, 33 Critical, 381 High, 485 Medium, 276 Low, 22 Info.
- Intermedio: 667 activos, 6 Critical, 158 High, 287 Medium, 195 Low, 21 Info.
- Cierre: 663 activos, 2 Critical, 158 High, 287 Medium, 195 Low, 21 Info.
- 556 mitigados y 22 registros nuevos acumulados: 1197 + 22 − 556 = 663.
  Uno de los nuevos correspondía al script de monitoreo y ya quedó mitigado.

Las diferencias LOW/INFO frente al CSV proceden de los parsers. Esta instancia
no hereda las decisiones de triage de la laptop de Mateo. No se han aprobado
nuevas aceptaciones de riesgo. Los JSON de resumen y capturas son evidencia de
esta instancia, no capturas reconstruidas de la instancia anterior.

## Cambios preparados

- Tomcat 10.1.56 a 10.1.62, último parche 10.1.x disponible en Maven Central
  durante la revisión. No se adopta 10.1.63, anunciado como no publicado.
- PATCH de estudiante y docente reenvía el JSON al backend. Se mantienen las
  restricciones de campos de ms-user y se comprueban con E2E.
- CI ejecuta también las pruebas de quiz y Java. El release depende de los
  resultados de pruebas y escaneos, además del gate y DAST.
- ZAP sin autenticación ahora falla. Se exigen los 15 reportes JSON esperados.
- Gate CRITICAL por defecto. No se alteran cifras, severidades ni filtros para
  conseguir una ejecución verde.
- Perfil opcional de monitoreo Prometheus y Blackbox con sondas de frontend y
  gateway, alertas de fallo y pérdida de scraping, ver monitoring/README.md.
- Excel con resultados CI, DefectDojo propio, resultado local y estados parciales.
- Diagrama de 12 jobs generado desde los needs actuales del YAML. La captura
  de GitHub corresponde a los 11 jobs del run histórico, no al código nuevo.

## Triage pendiente de decisión del equipo

Los 2 avisos Spring son diferentes. CVE-2026-47884 depende de XsltView y mapeo
de vistas. CVE-2026-47890 depende de fragmentos enviados mediante SSE. No se
encontraron esas clases ni configuraciones en el código revisado. Los avisos
del fabricante los clasifican MEDIUM y LOW respectivamente; Trivy los presenta
como CRITICAL. Se conserva la clasificación del escáner en todas las métricas.
Spring documenta corrección 6.2.20 empresarial o 7.0.9 OSS. Migrar a Boot 4 no
es la única ruta comercial. La aceptación requiere revisar las condiciones,
asignar responsable y fecha de revisión, o elegir la migración correspondiente.

Tomcat también anuncia CVE-2026-133325 para clustering TLS-PSK con TLS 1.3 en
10.1.62, corregida en 10.1.63 aún no publicada. El código y Compose revisados
no configuran clustering. No se interpreta su ausencia en este Trivy como
prueba de inexistencia de avisos recientes.

El CSV `triage-propuesto.csv` clasifica todas las detecciones del último run completo
como pendientes, propuestas o verificadas localmente. No equivale a aceptar
riesgos en nombre del equipo. Permanecen deudas de rate limiting de IA,
tokens en localStorage, auditoría de negocio y autorización por pertenencia al
aula. No declarar corregida toda la amenaza E-03 solo por exigir un rol.

## Decisiones que faltan para integrar y liberar

1. Revisar los dos CRITICAL de Spring y las propuestas de `decisiones-equipo.csv`.
   Aceptarlos en DefectDojo documentaría una decisión, pero no cambia este gate:
   seguirá bloqueando mientras los reportes contengan CRITICAL. Una liberación
   en verde requiere corregirlos o acordar explícitamente una política de
   excepciones trazable. No se implementaron excepciones ni se redujo el umbral.
2. Confirmar rotación de JWT_SECRET en todos los entornos existentes del equipo.
   La nueva instalación local usa una clave aleatoria. No demuestra rotación de
   las instalaciones de otros integrantes. No se purgó historial.
3. Revisar y acordar merges: #13 en `fix/security-mitigations`, después #12 en
   `feat/devsecops-pipeline` y #11 en `main`. Los tres están sin fusionar.
4. Identificar infraestructura y responsables antes de afirmar operación en
   producción. El alcance demostrado comprende desarrollo y staging efímero.
   El job de GHCR representa distribución y permanece bloqueado por seguridad.

El conector GitHub podía leer pero rechazaba escritura con 403. Se resolvió el
acceso mediante gh autenticado. No se cambiaron settings, variables ni secretos
remotos del repositorio. Los commits posteriores de entrega contienen solo
documentación, evidencias y artefactos; el código validado se identifica arriba.

## Referencias técnicas consultadas

- https://tomcat.apache.org/security-10.html
- https://repo.maven.apache.org/maven2/org/apache/tomcat/embed/tomcat-embed-core/maven-metadata.xml
- https://spring.io/security/cve-2026-47884/
- https://spring.io/security/cve-2026-47890/
- https://prometheus.io/docs/guides/multi-target-exporter/
- https://owaspsamm.org/model/
- https://owaspsamm.org/model/verification/security-testing/
