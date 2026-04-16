import math
from core.nlp import puntaje_ambiente

def calcular_riesgo(row, modelo_nlp):
    A = row["asistencia"]
    N = row["nota_promedio"]
    F = puntaje_ambiente(row["observaciones"], modelo_nlp)
    CS = row['CS']

    try:
        has_cs = not math.isnan(float(CS))
    except (TypeError, ValueError):
        has_cs = False

    if has_cs:
        Rd = (
            0.25 * (1 - A / 100) +
            0.25 * max(0, 75 - N) / 100 +
            0.25 * (1 - F) +
            0.25 * (1 - CS)
        )
    else:
        # sin formulario: tres componentes con peso igual
        Rd = (
            (1/3) * (1 - A / 100) +
            (1/3) * max(0, 75 - N) / 100 +
            (1/3) * (1 - F)
        )

    return round(Rd, 3), round(F, 3)
