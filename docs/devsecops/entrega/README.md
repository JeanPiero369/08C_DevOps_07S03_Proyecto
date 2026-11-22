# Entrega final de Kiwi

La rúbrica original exige los puntos a–m. El informe contiene esos apartados,
las figuras, la tabla de mitigaciones, las fuentes y el YAML completo.

- `Kiwi_Informe_Final.docx`: informe editable.
- `Kiwi_Informe_Final.pdf`: versión para lectura y entrega.
- `../stride/kiwi_stride.xlsx`: STRIDE, mitigaciones y cifras conciliadas.
- `../stride/kiwi_stride.drawio`: modelo de amenazas editable.
- `../cierre/pipeline.mmd`, `pipeline.svg` y `pipeline.png`: grafo del pipeline.
- `../cierre/VALIDACION.md`: verificaciones, alcance y decisiones pendientes.
- `../cierre/RESIDUALES.md` y `triage-propuesto.csv`: clasificación de lo que queda.

La exposición de 12 diapositivas se entrega en el visor de la conversación de
Codex y puede exportarse desde allí a PowerPoint. Sus notas incluyen fuentes y
un reparto tentativo para el ensayo que el equipo debe confirmar.

## Estado de seguridad

Código verificado: commit `5543e31`, run
[45060902475](https://github.com/JeanPiero369/08C_DevOps_07S03_Proyecto/actions/runs/45060902475).
Resultado: 663 detecciones, de ellas 2 CRITICAL de Spring. El gate bloquea por
esas dos detecciones. Pruebas, build, análisis, staging, monitoreo y DAST pasan.
La aceptación de riesgos no está automatizada ni cambia el resultado del gate.

La versión se presenta para revisión del equipo. Falta confirmar rotación de
JWT_SECRET en los entornos existentes y decidir el tratamiento de riesgos y
la integración de los PR. La infraestructura productiva no se ha validado.
