# Revisión de Tarea 01, clave 208999

Revisión del 12 de septiembre de 2026. Se contrastó la entrega recibida en `2d0ef75`
con el enunciado del profesor en `213958e9aaeea54988478056defd3d07b4db3da1`.

El modelo es fuerte frente a las referencias locales: MSE de auditoría **19.3227**,
frente a **99.6679** del baseline y **58.0620** de Lasso. Los cálculos se reproducen.
La tarea todavía no cumple todos los requisitos. Faltan evidencia personal exigida
por el enunciado, la meta oficial y la entrega mediante PR.

| Requisito | Estado | Evidencia o acción necesaria |
|---|---|---|
| Clave, variante, dimensiones y faltantes | Verificado | `208999` → `v2e419aae`; train 800×13, test 400×12; datos finitos y huellas verificadas |
| Separar ajuste y validación | Verificado con límite | 600 filas de desarrollo y 200 de auditoría, índices disjuntos, semilla 42; auditoría ya consultada |
| Baseline, MSE y R² | Verificado | `auditoria.csv`, `metricas.json` y reconstrucción independiente con NumPy |
| Distribuciones, y contra cada variable, correlación | Verificado | Figuras 01, 02 y 03; 12 variables en las rejillas |
| Sospechas escritas antes de seguir | Pendiente personal | La tabla de la Parte 1.1 es retrospectiva. No demuestra que se escribió antes de ver los resultados |
| Escalera de residuales, un término cada vez | Verificado como reproducción | Seis pasos, 12 paneles y referencia en cero; `escalera_cv.csv` y figura 10 |
| Detectar y medir interacciones | Verificado | 66 pares comparados; `x1*x11` baja MSE CV de 47.0168 a 20.0671; figura 06 antes/después |
| PolynomialFeatures grado 3, escala y LassoCV | Verificado | 454 columnas sin constante redundante, 60 alphas, 5 pliegues internos y 20 externos |
| MSE y columnas no nulas de Lasso | Verificado | CV 57.3492, auditoría 58.0620, 34 columnas, alpha 0.525217 |
| Cuatro respuestas de Parte 4.1 | Texto presente | Diccionario polinomial, límites y caso de 80 observaciones; el alumno debe poder defenderlas |
| Bitácora con hipótesis fallidas | Evidencia técnica presente | 16 filas de familias de hipótesis y CSV completos; exponencial, log1p, raíz y otras alternativas descartadas |
| Función final y ruido | Verificado | Parte 5.1 y `coeficientes.csv`; siete columnas más intercepto |
| Momento concreto en que se equivocó la IA | Pendiente personal | Comparación exponencial/cuadrado reproducible; falta la experiencia y reflexión propia del alumno |
| Criterio de parada y distancia a la meta | Parcial | Hay criterio local. Falta el MSE meta que devuelve `/validar` |
| Reajustar todo train y generar 400 predicciones | Verificado | OLS reconstruido con NumPy sobre 800 filas; predicciones en el orden original |
| Notebook ejecutado y entorno reproducible | Verificado localmente | 15 celdas desde kernel nuevo, sin errores ni avisos de convergencia de Lasso; kernel dentro de `.venv` |
| PR al curso, `/validar`, `/calificar` | Pendiente oficial | No hay PR del alumno ni comentarios enviados durante la revisión; no se acredita una nota oficial |
| IA sólo como tutor | No acreditado | Hay código y análisis de datos generados con IA, más allá del uso descrito en el enunciado. Atribuirlo a IA no resuelve esa diferencia |

## Qué dicen los resultados

| Modelo | MSE CV desarrollo | DE entre pliegues | MSE auditoría reutilizada | RMSE auditoría | R² auditoría |
|---|---:|---:|---:|---:|---:|
| Baseline | 104.6655 | 15.0910 | 99.6679 | 9.9834 | 0.3938 |
| Compacto | 19.5950 | 2.5838 | 19.3227 | 4.3958 | 0.8825 |
| Polinomio grado 3 + LassoCV | 57.3492 | 6.7840 | 58.0620 | 7.6198 | 0.6469 |

La reducción local de MSE frente al baseline es 80.61%. Esto respalda conservar
el compacto. No demuestra una nota de 10 ni que el error restante sea ruido puro.

Retirar cualquiera de las siete columnas aumenta el MSE CV. La retirada menos
costosa, `x11`, lo lleva a 27.51; retirar `x7³` lo lleva a 61.76. Son contribuciones
predictivas condicionales en esta fórmula, no efectos causales. La rejilla respalda
el seno de frecuencia 1 frente a las 13 alternativas comprobadas, sin demostrar
una frecuencia exacta entre todos los valores posibles.

Agregar `x6` cruda baja MSE CV sólo de 19.5950 a 19.5742. Se conserva la fórmula
más sencilla. La DE de pliegues no es un error estándar independiente; comparar
barras solapadas no es una prueba de significancia.

La CV guiada reutiliza filas que sirvieron para seleccionar transformaciones.
El pipeline de Lasso se evalúa fuera de cada ajuste externo, aunque su CV interna
recibe la matriz ya escalada del entrenamiento externo, como en el pipeline
sugerido por el curso. Un protocolo más estricto ajustaría el escalador dentro de
cada pliegue interno al seleccionar alpha. Las filas de evaluación externa y de
auditoría no llegan al escalador.

La auditoría es la misma partición consultada en la solución recibida. Las nuevas
comprobaciones no crean una validación independiente de una búsqueda nueva.
El intervalo bootstrap del MSE, aproximadamente [15.48, 23.75], condiciona en el
modelo y la muestra existentes; no incluye incertidumbre de selección.

## Calidad de las figuras

Los 17 PNG originales eran legibles y correspondían a cálculos reales, pero les
faltaba contexto para interpretarlos por separado. La revisión produce 20 figuras.

| Problema observado | Corrección |
|---|---|
| Sin título de etapa ni tamaño de muestra | Título, modelo/etapa y muestra en cada figura |
| Curva naranja sin explicación | Leyenda de medias agrupadas y un error estándar descriptivo |
| 12 grupos ocultaban parte de la oscilación de x4 | 24 grupos para x4 en desarrollo, declarados en el pie |
| Escalas cambiaban entre pasos | Escala fija en baseline y seis pasos; detalle final rotulado aparte |
| Distinto orden de variables entre figuras | Rejilla de 3×4 uniforme |
| Correlaciones a un decimal y ceros negativos | Dos decimales, sin -0.00; explicación del límite de la correlación marginal |
| Interacción sólo mostraba el problema | Antes/después del producto, con la misma escala |
| Barras de MSE sin valores ni dispersión | Valores y DE, rotulada como descriptiva |
| Exponencial difícil de comparar visualmente | MSE en títulos, medias por grupos y tabla reproducible en dos contextos |
| Progreso y contribuciones dispersos | Figuras 10 y 11, escalera y retirada de términos |
| Diagnóstico final limitado | Predicho/observado con ejes iguales, residuales, histograma y Q-Q |
| x6 comprimida por la cola derecha | Detalle adicional en escala logarítmica en figura 12 |

El Q-Q muestra algunas observaciones extremas. Eso no justifica borrar filas.
La ausencia de una forma grande en los residuales no prueba ruido puro.
Las curvas agrupadas son diagnósticos, no modelos nuevos ni bandas de predicción.

El verificador decodifica los PNG y comprueba dimensiones y SHA-256 contra
`figuras_manifest.json`. Eso detecta daños o cambios posteriores al manifiesto.
La inspección visual es distinta: un hash no prueba que los ejes o las conclusiones
sean correctos. La revisión visual detectó y corrigió además el solapamiento de
títulos y subtítulos en las figuras panorámicas de la primera regeneración.

## Lo que falta para cumplir la tarea

1. Revisar el límite de uso de IA del enunciado y acordar con el profesor cómo
   acreditar el razonamiento propio. La revisión automática no certifica ese punto.
2. Explicar personalmente las sospechas, los residuales, la interacción y el fallo
   de la IA. No presentar la tabla retrospectiva como notas previas al análisis.
   Si esas notas nunca existieron, decirlo; esa cronología no se puede reconstruir.
3. Revisar la entrega y abrir el PR de `HarryGomar/mineria_datos:tarea-01-208999`
   hacia `nasaul/mineria_datos:main`.
4. Solicitar `/validar` en ese PR, guardar el MSE meta oficial y completar la
   Parte 5.3. Compararlo con un MSE local tiene incertidumbre y no revela el error
   real de las 400 filas ocultas.
5. Cuando el alumno decida presentar un intento, solicitar `/calificar`. Hay tres
   intentos y cuenta el último, según el [README del curso](tarea_01_README.md).

El README fija el cierre el **20 de septiembre de 2026, 23:59, hora de CDMX**.
Esta revisión no envió mensajes al profesor ni consumió intentos.

## Reproducir y revisar

Sigue [INICIO_208999.md](INICIO_208999.md). Un checkout nuevo fallaba con
`NoSuchKernel: mineria-datos`: sólo tenía el kernel `python3`. Los ejecutores ahora
registran el kernel dentro de `.venv`, con el Python de este checkout.

El verificador comprueba ejecución secuencial, huella del código, datos y
predicciones; reconstruye OLS con NumPy y cruza métricas con los CSV. La comparación
con las predicciones recibidas admite sólo tolerancia de coma flotante. La revisión
no cambió la fórmula ni ajustó parámetros a partir de la auditoría.

La evidencia está en `escalera_cv.csv`, `comparacion_pliegues.csv`,
`exponencial_cv.csv`, `ablacion_cv.csv`, `frecuencia_x4_cv.csv`, `alternativas_cv.csv`,
`interacciones_cv.csv`, `sensibilidad_cv.csv`, `lasso_cv_externo.csv` y `bitacora.csv`.
`metricas.json` deja la meta oficial en `null` y declara la reutilización de auditoría.

La rama de tarea recibió el nombre `tarea-01-208999`. El commit del alumno estaba
sobre `213958e`, que era el `main` del profesor al revisar. El `main` del fork es
otra línea con trabajo previo y se conserva en `05db756`; no se reescribió ni se
trató como una rama sobrante.
