# Ambientes y monitoreo de Kiwi

Desarrollo usa Docker Compose en la laptop. CI crea staging efímero con credenciales
aleatorias y base de datos desechable. El job release publica imágenes de main en
GHCR. Esa publicación es una fase de distribución: no demuestra un despliegue en
producción. No hay un servidor de producción identificado en el traspaso.

## Monitoreo local o staging persistente

```bash
docker compose -f compose.yml -f compose.monitoring.yml --profile monitoring up -d --build
```

Prometheus está disponible en http://localhost:9090. La consulta
`probe_success{job="kiwi-http"}` debe devolver 1 para frontend y gateway.
`probe_duration_seconds` mide el tiempo de la sonda HTTP, no la latencia de todas
las peticiones de negocio. Los HEALTHCHECK de Compose complementan estas sondas.

La alerta `KiwiEndpointDown` pasa a firing después de un minuto de fallos.
`KiwiProbeMissing` detecta fallos de scraping del exporter. Para demostrar la alerta,
detener solo frontend, observar pending/firing, arrancarlo y comprobar la recuperación.
Alertmanager y notificaciones externas quedan fuera de esta instalación.

## Promoción entre ambientes

1. Desarrollo: pruebas unitarias y revisión de cambios en una rama.
2. Staging CI: construir, escanear y ejecutar DAST autenticado sobre datos efímeros.
3. Evaluación: verificar todos los reportes y aplicar el umbral de seguridad.
4. Distribución: publicar imágenes de main en GHCR cuando las dependencias del
   release terminan correctamente. El umbral predeterminado es CRITICAL; la variable SECURITY_GATE_SEVERITY permite endurecerlo a HIGH.
5. Producción: requiere infraestructura, secretos propios, copia de seguridad,
   prueba de restauración y revisión del equipo. No ejecutar el generador de
   credenciales efímeras contra una instalación con datos que deban conservarse.

Referencia del patrón de sondas:
https://prometheus.io/docs/guides/multi-target-exporter/
