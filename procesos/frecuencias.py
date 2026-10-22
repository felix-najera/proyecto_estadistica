

import math
import pandas as pd


def calcular_frecuencias(valores, agrupar=False, intervalos=None):
    """
    Calcula frecuencias absolutas, relativas y acumuladas.

    agrupar=True permite construir una distribución de frecuencias
    agrupada para datos cuantitativos con muchos valores diferentes.
    """

    datos = pd.Series(valores).dropna()

    # Eliminar respuestas vacías
    datos = datos[
        datos.astype(str).str.strip() != ""
    ]

    if datos.empty:
        raise ValueError(
            "No hay datos válidos para calcular frecuencias."
        )

    # Distribución de frecuencias agrupada
    if agrupar:
        datos_numericos = pd.to_numeric(
            datos, errors="coerce"
        ).dropna()

        if datos_numericos.empty:
            raise ValueError(
                "No se puede agrupar: no hay datos numéricos válidos."
            )

        cantidad = len(datos_numericos)

        # Regla de Sturges para estimar el número de intervalos
        if intervalos is None:
            intervalos = max(
                1,
                math.ceil(1 + 3.322 * math.log10(cantidad))
            )

        if intervalos < 1:
            raise ValueError(
                "El número de intervalos debe ser mayor que cero."
            )

        # Si todos los valores son iguales, no hace falta agrupar
        if datos_numericos.nunique() == 1:
            frecuencias = datos_numericos.value_counts(
                sort=False
            ).sort_index()

            tabla = pd.DataFrame({
                "Frecuencia absoluta": frecuencias
            })
            tabla.index.name = "Valor"

        else:
            categorias = pd.cut(
                datos_numericos,
                bins=intervalos,
                include_lowest=True
            )

            frecuencias = categorias.value_counts(
                sort=False
            ).sort_index()

            tabla = pd.DataFrame({
                "Frecuencia absoluta": frecuencias
            })
            tabla.index.name = "Intervalo"

    # Distribución sin agrupar
    else:
        frecuencias = datos.value_counts(
            sort=False
        )

        # Ordenar los valores cuando sea posible
        try:
            frecuencias = frecuencias.sort_index()
        except TypeError:
            pass

        tabla = pd.DataFrame({
            "Frecuencia absoluta": frecuencias
        })
        tabla.index.name = "Valor"

    total = int(tabla["Frecuencia absoluta"].sum())

    tabla["Frecuencia acumulada"] = (
        tabla["Frecuencia absoluta"].cumsum()
    )

    tabla["Frecuencia relativa"] = (
        tabla["Frecuencia absoluta"] / total
    )

    tabla["Porcentaje"] = (
        tabla["Frecuencia relativa"] * 100
    )

    return tabla.reset_index()

