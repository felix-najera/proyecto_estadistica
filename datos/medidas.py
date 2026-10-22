
import numpy as np
from scipy import stats


def calcular_medidas(valores):
    """
    Calcula las principales medidas descriptivas
    de una lista de datos numéricos.
    """

    datos = np.asarray(valores, dtype=float)
    datos = datos[np.isfinite(datos)]

    if len(datos) == 0:
        raise ValueError("No hay datos numéricos válidos.")

    media = np.mean(datos)
    mediana = np.median(datos)
    desviacion = np.std(datos, ddof=1) if len(datos) > 1 else 0.0
    varianza = np.var(datos, ddof=1) if len(datos) > 1 else 0.0

    moda_resultado = stats.mode(datos, keepdims=False)
    moda = moda_resultado.mode

    q1, q2, q3 = np.percentile(datos, [25, 50, 75])

    asimetria = (
        float(stats.skew(datos, bias=False))
        if len(datos) >= 3 and desviacion > 0
        else 0.0
    )

    curtosis = (
        float(stats.kurtosis(datos, bias=False))
        if len(datos) >= 4 and desviacion > 0
        else 0.0
    )

    if asimetria > 0.5:
        tipo_asimetria = "Asimétrica positiva"
    elif asimetria < -0.5:
        tipo_asimetria = "Asimétrica negativa"
    else:
        tipo_asimetria = "Aproximadamente simétrica"

    # SciPy devuelve por defecto el exceso de curtosis:
    # 0 corresponde a una distribución mesocúrtica.
    if curtosis > 0.5:
        tipo_curtosis = "Leptocúrtica"
    elif curtosis < -0.5:
        tipo_curtosis = "Platicúrtica"
    else:
        tipo_curtosis = "Mesocúrtica"

    return {
        "cantidad": len(datos),
        "media": float(media),
        "mediana": float(mediana),
        "moda": float(moda),
        "minimo": float(np.min(datos)),
        "maximo": float(np.max(datos)),
        "rango": float(np.ptp(datos)),
        "varianza_muestral": float(varianza),
        "desviacion_estandar": float(desviacion),
        "coeficiente_variacion": (
            float(desviacion / abs(media) * 100)
            if media != 0 else None
        ),
        "q1": float(q1),
        "q2": float(q2),
        "q3": float(q3),
        "rango_intercuartilico": float(q3 - q1),
        "p10": float(np.percentile(datos, 10)),
        "p25": float(np.percentile(datos, 25)),
        "p50": float(np.percentile(datos, 50)),
        "p75": float(np.percentile(datos, 75)),
        "p90": float(np.percentile(datos, 90)),
        "asimetria": asimetria,
        "tipo_asimetria": tipo_asimetria,
        "curtosis": curtosis,
        "tipo_curtosis": tipo_curtosis
    }
