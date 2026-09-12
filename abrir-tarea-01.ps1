$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$pythonTarea = Join-Path $PSScriptRoot '.venv/Scripts/python.exe'
if (-not (Test-Path -LiteralPath $pythonTarea)) {
    throw 'Falta el entorno .venv. Instala las dependencias con uv sync --locked.'
}
& $pythonTarea -m jupyterlab 'tareas/tarea_01_aproximacion_funcion.ipynb'
