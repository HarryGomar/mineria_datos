$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$pythonTarea = Join-Path $PSScriptRoot '.venv/Scripts/python.exe'
if (-not (Test-Path -LiteralPath $pythonTarea)) {
    throw 'Falta el entorno .venv. Consulta tareas/INICIO_208999.md.'
}
# Ejecuta modelos y validación locales; genera el CSV. No envía nada a GitHub.
& $pythonTarea -m nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=600 'tareas/tarea_01_aproximacion_funcion.ipynb'
if ($LASTEXITCODE -ne 0) { throw 'Falló la ejecución local del notebook.' }
& $pythonTarea 'tareas/verificar_tarea_01.py'
if ($LASTEXITCODE -ne 0) { throw 'Falló la verificación local de los resultados.' }
