# Fuente del informe en LaTeX

La portada y el índice siguen la referencia académica proporcionada por el
autor. Los datos, el contenido, las tablas y las evidencias son del proyecto Kiwi.

Desde esta carpeta, compilar con Tectonic:

```sh
tectonic --untrusted main.tex
cp main.pdf ../Kiwi_Informe_Final.pdf
```

También se puede usar `latexmk -pdf main.tex` con una instalación de TeX Live.
El índice se calcula automáticamente; compilar dos veces con `pdflatex` si no
se usa Tectonic o latexmk. Las imágenes están en `assets/`.

`devsecops.yml` conserva el workflow del corte del informe; sus separadores
decorativos de comentarios usan guiones ASCII para la tipografía del anexo.
El workflow ejecutable del proyecto está en `.github/workflows/devsecops.yml`.
Las cifras corresponden al run 45067822680 documentado en el informe.
