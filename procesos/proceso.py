
from pathlib import Path

import pandas as pd


def leer_archivo(ruta):
    """
    Lee un archivo Excel o CSV y devuelve sus datos.
    """

    extension = Path(ruta).suffix.lower()

    if extension == ".xlsx":
        datos = pd.read_excel(ruta)

    elif extension == ".csv":
        try:
            datos = pd.read_csv(ruta, encoding="utf-8-sig")
        except UnicodeDecodeError:
            datos = pd.read_csv(ruta, encoding="latin-1")

    else:
        raise ValueError(
            "Formato no válido. Selecciona un archivo XLSX o CSV."
        )

    if datos.empty:
        raise ValueError("El archivo no contiene registros.")

    if len(datos.columns) == 0:
        raise ValueError("El archivo no contiene columnas.")

    # Eliminar espacios sobrantes en los encabezados.
    datos.columns = [
        str(columna).strip()
        for columna in datos.columns
    ]

    return datos
