
import matplotlib.pyplot as plt
import pandas as pd


def generar_grafico(valores, nombre_variable):
    """
    Genera un gráfico básico según el tipo de datos.
    Devuelve la figura para mostrarla en la interfaz.
    """

    datos = pd.Series(valores).dropna()

    if datos.empty:
        raise ValueError("No hay datos válidos para graficar.")

    figura, eje = plt.subplots(figsize=(8, 5))

    if pd.api.types.is_numeric_dtype(datos):
        if datos.nunique() <= 10:
            frecuencias = datos.value_counts().sort_index()
            eje.bar(
                frecuencias.index.astype(str),
                frecuencias.values
            )
            eje.set_xlabel(nombre_variable)
            eje.set_ylabel("Frecuencia")
        else:
            eje.hist(datos, bins="auto", edgecolor="black")
            eje.set_xlabel(nombre_variable)
            eje.set_ylabel("Frecuencia")

    else:
        frecuencias = datos.astype(str).value_counts()
        eje.bar(
            frecuencias.index,
            frecuencias.values
        )
        eje.set_xlabel(nombre_variable)
        eje.set_ylabel("Frecuencia")
        eje.tick_params(axis="x", rotation=35)

    eje.set_title(f"Distribución de {nombre_variable}")
    figura.tight_layout()

    return figura
