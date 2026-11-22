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

Código verificado: commit `41aaa61`, [run 45067822680](https://github.com/JeanPiero369/08C_DevOps_07S03_Proyecto/actions/runs/45067822680).
Resultado: 672 detecciones, **0 CRITICAL**. El gate aprueba; pruebas,
build, análisis, staging, monitoreo y DAST pasan. El release se omite fuera
de main. SonarCloud y la importación remota a DefectDojo siguen sin configurar;
la instancia propia se actualizó localmente.

La clave JWT_SECRET local fue rotada con invalidación comprobada del token
anterior. Falta la confirmación de las demás computadoras, revisar riesgos
residuales y acordar los merges. No se acredita operación productiva.
Las cifras del informe fijan el corte de código indicado; otros runs pueden
variar por cambios de imágenes y bases de vulnerabilidades.
