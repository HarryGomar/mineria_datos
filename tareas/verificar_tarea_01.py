"""Comprueba los artefactos locales de la tarea; no tiene cliente del calificador."""
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


def matriz_independiente(datos):
    """Reconstrucción explícita de la fórmula, independiente de los helpers del notebook."""
    if (datos["x6"] <= 0).any():
        raise ValueError("x6 debe ser positiva para evaluar el logaritmo.")
    return np.column_stack([
        np.ones(len(datos)), datos["x11"], datos["x2"] ** 2,
        np.sin(2 * np.pi * datos["x4"]), np.log(datos["x6"]),
        datos["x7"] ** 3, (datos["x9"] > 60).astype(float),
        datos["x1"] * datos["x11"],
    ])


def verificar():
    raiz = Path(__file__).resolve().parents[1]
    resultados = raiz / "tareas/resultados_208999"
    datos = raiz / "tareas/tarea_01_datos/v2e419aae"
    entrega = raiz / "entregas/tarea-01/v2e419aae/predicciones.csv"
    metricas = json.loads((resultados / "metricas.json").read_text(encoding="utf-8"))
    notebook = json.loads((raiz / "tareas/tarea_01_aproximacion_funcion.ipynb").read_text(encoding="utf-8"))
    celdas = [c for c in notebook["cells"] if c["cell_type"] == "code"]
    assert all(c["execution_count"] is not None for c in celdas), "Hay celdas sin ejecutar."
    assert [c["execution_count"] for c in celdas] == list(range(1, len(celdas) + 1))
    for celda in celdas:
        compile("".join(celda["source"]), "<celda>", "exec")
        assert not any(o["output_type"] == "error" for o in celda["outputs"])
        assert "ConvergenceWarning" not in json.dumps(celda["outputs"])

    train, test = (pd.read_csv(datos / f"{nombre}.csv") for nombre in ["train", "test"])
    columnas = [f"x{i}" for i in range(1, 13)]
    assert train.shape == (800, 13) and list(train) == columnas + ["y"]
    assert test.shape == (400, 12) and list(test) == columnas
    assert np.isfinite(train.to_numpy()).all() and np.isfinite(test.to_numpy()).all()
    for nombre in ["train", "test"]:
        huella = hashlib.sha256((datos / f"{nombre}.csv").read_bytes()).hexdigest()
        assert huella == metricas["sha256_datos"][nombre], "Los datos cambiaron después de ejecutar."
    assert hashlib.sha256(entrega.read_bytes()).hexdigest() == metricas["sha256_predicciones"]

    csv = pd.read_csv(entrega)
    assert csv.shape == (400, 1) and list(csv) == ["y"]
    assert np.isfinite(csv["y"]).all()
    tabla_coef = pd.read_csv(resultados / "coeficientes.csv")
    assert list(tabla_coef["termino"]) == [
        "intercepto", "x11", "x2_cuadrado", "seno_x4", "log_x6", "x7_cubo",
        "escalon_x9", "interaccion_x1_x11",
    ]
    coeficientes = tabla_coef["coeficiente"].to_numpy()
    # El archivo debe corresponder a la fórmula y al orden original de test.
    np.testing.assert_allclose(csv["y"], matriz_independiente(test) @ coeficientes,
                               rtol=1e-10, atol=1e-9)
    # Reajuste con NumPy: confirma que se usaron las 800 filas para la entrega.
    coef_numpy = np.linalg.lstsq(matriz_independiente(train), train["y"], rcond=None)[0]
    np.testing.assert_allclose(coeficientes, coef_numpy, rtol=1e-10, atol=1e-9)

    desarrollo, auditoria = train_test_split(train, test_size=0.25, random_state=42)
    for nombre, diseno in [
        ("Baseline", lambda d: np.column_stack([np.ones(len(d)), d[columnas]])),
        ("Lineal compacto", matriz_independiente),
    ]:
        coef = np.linalg.lstsq(diseno(desarrollo), desarrollo["y"], rcond=None)[0]
        pred = diseno(auditoria) @ coef
        mse = float(np.mean((auditoria["y"] - pred) ** 2))
        registro = next(r for r in metricas["auditoria"] if r["modelo"] == nombre)
        np.testing.assert_allclose(mse, registro["MSE"], rtol=1e-10, atol=1e-9)

    coef_lasso = pd.read_csv(resultados / "coeficientes_lasso.csv")
    assert len(coef_lasso) == 454
    assert np.count_nonzero(coef_lasso["coeficiente_estandarizado"]) == metricas["lasso"]["coeficientes_no_nulos"]
    cv_lasso = pd.read_csv(resultados / "lasso_cv_externo.csv")
    assert len(cv_lasso) == 20 and np.isfinite(cv_lasso.to_numpy()).all()
    np.testing.assert_allclose(cv_lasso["MSE"].mean(), metricas["cv_desarrollo"]["lasso"]["MSE_CV"])
    assert metricas["calificacion_oficial_solicitada"] is False
    assert len(pd.read_csv(resultados / "interacciones_cv.csv")) == 66
    assert len(pd.read_csv(resultados / "alternativas_cv.csv")) == 54
    bitacora = pd.read_csv(resultados / "bitacora.csv")
    assert (bitacora["decision"] == "Descartar").any()
    for nombre in [*(f"residuales_paso_{i:02d}.png" for i in range(1, 7)),
                   "residuales_compacto.png", "09_comparacion_lasso.png"]:
        assert (resultados / nombre).is_file(), f"Falta la figura {nombre}."

    print(f"OK: {len(celdas)} celdas ejecutadas sin errores ni avisos de convergencia.")
    print("OK: 400 predicciones finitas; fórmula, coeficientes y orden verificados independientemente.")
    print("OK: ajuste con 800 filas y métricas de auditoría con 600/200 reproducidos con NumPy.")
    print("OK: LassoCV, 20 pliegues externos, 66 pares, 54 alternativas y bitácora comprobados.")
    print("Todo fue local; no se solicitó una calificación.")


if __name__ == "__main__":
    verificar()
