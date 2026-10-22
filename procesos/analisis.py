import pandas as pd


def analizar_encuesta(datos):
    resultados = []

    for nombre in datos.columns:
        columna = datos[nombre]

        # Contar respuestas vacias
        vacios = int(columna.isna().sum())

        # Quitar respuestas vacias para analizar los datos
        respuestas = columna.dropna()
        respuestas = respuestas[respuestas.astype(str).str.strip() != ""]

        # Contar respuestas validas y valores diferentes
        cantidad = len(respuestas)
        diferentes = respuestas.nunique()

        if cantidad == 0:
            tipo = "Sin datos"

        elif pd.api.types.is_numeric_dtype(respuestas):
            tipo = "Cuantitativa"

            # Las escalas pequeñas necesitan revision
            if diferentes <= 10 and respuestas.min() >= 0 and respuestas.max() <= 10:
                tipo = "Revisar tipo"

        else:
            # Comprobar si todas las respuestas son numeros
            numeros = pd.to_numeric(respuestas, errors="coerce")

            if numeros.notna().all():
                tipo = "Revisar tipo"
            else:
                tipo = "Cualitativa"

        resultados.append({
            "Pregunta": nombre,
            "Tipo sugerido": tipo,
            "Respuestas validas": cantidad,
            "Datos vacios": vacios,
            "Valores diferentes": diferentes
        })

    return pd.DataFrame(resultados)