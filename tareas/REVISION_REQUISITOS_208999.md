# Revisión de requisitos · Tarea 01 · 208999

La evidencia principal está en `tarea_01_aproximacion_funcion.ipynb`, con celdas ejecutadas,
figuras y tablas. La solución identifica qué trabajo fue asistido por IA.

| Requisito | Evidencia local |
|---|---|
| Clave y variante correctas | `208999` → `v2e419aae`; verificación de esquema y datos finitos |
| Separar entrenamiento y validación | 600 filas de desarrollo y 200 de auditoría, semilla 42; índices disjuntos |
| Baseline lineal | MSE de CV y MSE/R² de auditoría; tabla de comparación |
| Distribuciones, y contra variables, correlación | Figuras 01, 02 y 03 |
| Interpretar las 12 variables | Parte 1.1, con evidencia y certeza; síntesis retrospectiva declarada |
| Escalera de residuales | 12 paneles con línea en cero después de cada término; figuras `residuales_paso_01` a `06` |
| Encontrar y medir interacciones | Comparación de 66 pares, figura del producto `x1*x11`, MSE antes/después |
| PolynomialFeatures de grado 3 | 454 columnas, sin columna constante redundante |
| Estandarizar antes de LassoCV | Pipeline; escalador ajustado sólo con el entrenamiento externo |
| Elegir penalización con CV | LassoCV con 60 valores de alpha y 5 pliegues internos |
| Comparar Lasso con el modelo guiado | Mismos 20 pliegues externos, más auditoría común de 200 filas |
| MSE, alpha y columnas no nulas de Lasso | Partes 4 y Auditoría; `coeficientes_lasso.csv` y `metricas.json` |
| Explicar la comparación y el caso de 80 observaciones | Las cuatro respuestas de la Parte 4.1 |
| Bitácora con hipótesis fallidas | Exponencial, log1p y raíz cuadrada descartadas; evidencia y MSE registrados |
| Función final e interpretación | Parte 5.1, expresión con ruido y tabla de coeficientes |
| Error concreto de la IA | Parte 5.2: exponencial inicialmente prometedora y luego descartada |
| Criterio de parada | Parte 5.3; simplicidad, CV, residuales y comparación con Lasso |
| Reajustar con todo train | OLS final con 800 filas, comprobado independientemente con NumPy |
| Archivo de entrega | 400 predicciones finitas, una columna y, en la ruta de la variante y en orden original |
| Reproducibilidad | Semillas, versiones, huellas SHA-256, ejecutor y verificador locales |

## Aspectos que no deben presentarse como ya cumplidos

- **MSE meta oficial y distancia a esa meta:** no se ha consultado el bot. La Parte 5.3
  lo declara; no inventa una referencia a partir de datos locales. `/validar` permite
  obtenerla sin gastar intentos, mediante un comentario posterior en el PR.
- **Hipótesis personales antes de explorar y comprensión del alumno:** la tabla y la
  bitácora se identifican como asistencia de IA. No puede reconstruirse retrospectivamente
  un registro personal que no ocurrió; el alumno debe revisar el razonamiento y poder explicarlo.
- **Publicación y nota oficial:** no se ha enviado el CSV, publicado un PR ni solicitado
  `/calificar`. Esta revisión sólo acredita los artefactos locales, no garantiza una nota.

## Verificación local

Desde la raíz del repositorio:

```powershell
.\ejecutar-tarea-01.ps1
```

Ejecuta el notebook desde un kernel nuevo y luego `tareas/verificar_tarea_01.py`.
Para volver a comprobar los archivos ya generados, sin volver a entrenar Lasso:

```powershell
.\.venv\Scripts\python.exe tareas/verificar_tarea_01.py
```

El verificador lee artefactos locales y reajusta OLS con NumPy para comprobar la fórmula
y las métricas; no importa ni ejecuta el script oficial de calificación.
