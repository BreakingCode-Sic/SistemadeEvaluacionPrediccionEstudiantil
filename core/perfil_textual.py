import math


def generar_perfil_textual(row):
    partes = []

    partes.append(
        f"Estudiante de {row['edad']} años con nota promedio de {row['nota_promedio']:.1f} "
        f"y asistencia del {row['asistencia']:.1f}%."
    )

    if row["F"] >= 0.7:
        partes.append("Presenta un entorno emocional y escolar favorable.")
    elif row["F"] >= 0.4:
        partes.append("Presenta un entorno social mixto.")
    else:
        partes.append("Se identifica un entorno social vulnerable.")

    if row["score_ciencia"] > 0:
        partes.append("Muestra interés por ciencias y experimentacion.")
    if row["score_num"] > 0:
        partes.append("Posee afinidad por el razonamiento logico y numérico.")
    if row["score_social"] > 0:
        partes.append("Destaca en habilidades sociales y comunicacion.")

    if isinstance(row["observaciones"], str):
        partes.append("Observaciones relevantes: " + row["observaciones"])

    return " ".join(partes)


# ---------------------------------------------------------------------------
# Helpers de género
# ---------------------------------------------------------------------------

def _g(genero, forma):
    m = str(genero).strip().upper() == "M"
    return {
        "art":      "el"  if m else "la",
        "art_cap":  "El"  if m else "La",
        "pron":     "él"  if m else "ella",
        "pron_cap": "Él"  if m else "Ella",
        "adj":      "o"   if m else "a",   # terminación -o/-a
    }[forma]


# ---------------------------------------------------------------------------
# Generador de informe final
# ---------------------------------------------------------------------------

def generar_descripcion_final(row, ranking):
    """
    Genera un informe profesional del estudiante en tres párrafos.

    Parámetros
    ----------
    row     : pandas Series con los datos del master dataset
    ranking : DataFrame con columnas 'nombre_area' y 'afinidad' (0-1),
              ya ordenado de mayor a menor afinidad
    """

    nombre     = str(row["nombre_estudiante"])
    edad       = int(float(row["edad"]))
    nota       = float(row["nota_promedio"])
    asistencia = float(row["asistencia"])
    F          = float(row["F"]) if row["F"] == row["F"] else 0.5
    genero     = row.get("genero", "M")

    # Riesgo
    try:
        Rd = float(row["Rd"])
    except (TypeError, ValueError, KeyError):
        Rd = None

    # Contexto social
    try:
        cs_val = float(row["CS"])
        has_cs = not math.isnan(cs_val)
    except (TypeError, ValueError):
        has_cs = False
        cs_val = None

    # ── PÁRRAFO 1: perfil académico ─────────────────────────────────────────

    if nota >= 90:
        rend_txt = f"rendimiento académico sobresaliente ({nota:.1f}/100)"
    elif nota >= 80:
        rend_txt = f"rendimiento académico bueno ({nota:.1f}/100)"
    elif nota >= 70:
        rend_txt = f"rendimiento académico aceptable ({nota:.1f}/100)"
    elif nota >= 60:
        rend_txt = f"rendimiento académico bajo ({nota:.1f}/100)"
    else:
        rend_txt = f"rendimiento académico crítico ({nota:.1f}/100)"

    if asistencia >= 95:
        asist_txt = f"asistencia excelente ({asistencia:.1f}%)"
    elif asistencia >= 85:
        asist_txt = f"asistencia regular ({asistencia:.1f}%)"
    elif asistencia >= 70:
        asist_txt = f"asistencia irregular ({asistencia:.1f}%)"
    else:
        asist_txt = f"asistencia preocupante ({asistencia:.1f}%)"

    if F >= 0.7:
        entorno_txt = "un entorno emocional y escolar favorable que potencia su desarrollo"
    elif F >= 0.4:
        entorno_txt = "un entorno socioemocional mixto con áreas de oportunidad"
    else:
        entorno_txt = "un entorno socioemocional vulnerable que requiere atención prioritaria"

    if has_cs:
        if cs_val >= 0.7:
            cs_txt = (f"El contexto social reportado es favorable (CS: {cs_val:.2f}), "
                      f"indicando condiciones de apoyo adecuadas en su entorno familiar y comunitario.")
        elif cs_val >= 0.45:
            cs_txt = (f"El contexto social presenta condiciones moderadas (CS: {cs_val:.2f}), "
                      f"con algunos factores de riesgo identificados en su entorno.")
        else:
            cs_txt = (f"El contexto social indica condiciones de vulnerabilidad (CS: {cs_val:.2f}), "
                      f"con factores de riesgo significativos en su entorno familiar o comunitario.")
    else:
        cs_txt = "No se dispone de información del formulario de contexto social para este período."

    p1 = (
        f"{nombre} es {_g(genero,'art')} estudiante de {edad} años con {rend_txt} "
        f"y {asist_txt}. "
        f"Presenta {entorno_txt}. "
        f"{cs_txt}"
    )

    # ── PÁRRAFO 2: intereses y observaciones ────────────────────────────────

    obs_text = row.get("observaciones", "")
    obs_list = []
    if isinstance(obs_text, str) and obs_text.strip():
        obs_list = [o.strip() for o in obs_text.split("|") if o.strip()]

    inclinaciones = []
    if float(row.get("score_ciencia", 0) or 0) > 0:
        inclinaciones.append("ciencias y experimentación")
    if float(row.get("score_num", 0) or 0) > 0:
        inclinaciones.append("razonamiento lógico-matemático")
    if float(row.get("score_social", 0) or 0) > 0:
        inclinaciones.append("habilidades sociales y comunicación")

    if inclinaciones:
        if len(inclinaciones) == 1:
            incl_txt = f"Sus observaciones reflejan una inclinación hacia {inclinaciones[0]}."
        else:
            incl_txt = ("Sus observaciones reflejan inclinación hacia "
                        + ", ".join(inclinaciones[:-1]) + " y " + inclinaciones[-1] + ".")
    else:
        incl_txt = "Sus observaciones no registran una inclinación temática predominante."

    if obs_list:
        seleccionadas = obs_list[:2]
        obs_cita = (" Destacan aspectos como: "
                    + "; ".join(f'"{o}"' for o in seleccionadas) + ".")
    else:
        obs_cita = " No se han registrado observaciones específicas en el período actual."

    p2 = incl_txt + obs_cita

    # ── PÁRRAFO 3: riesgo y recomendación ───────────────────────────────────

    if Rd is not None:
        if Rd < 0.15:
            riesgo_txt = f"bajo riesgo de deserción ({Rd:.1%})"
            accion_txt = (f"Se sugiere mantener el acompañamiento regular "
                          f"y potenciar las fortalezas de {_g(genero,'art')} estudiante.")
        elif Rd < 0.35:
            riesgo_txt = f"riesgo de deserción moderado ({Rd:.1%})"
            accion_txt = ("Se recomienda monitoreo periódico y refuerzo "
                          "en las áreas de menor desempeño.")
        elif Rd < 0.55:
            riesgo_txt = f"riesgo de deserción elevado ({Rd:.1%})"
            accion_txt = ("Se requiere intervención activa por parte "
                          "del equipo de orientación.")
        else:
            riesgo_txt = f"riesgo de deserción crítico ({Rd:.1%})"
            accion_txt = ("Se recomienda activar el protocolo de intervención urgente "
                          "con familia y equipo psicopedagógico.")
        riesgo_sentence = f"El análisis integral indica {riesgo_txt}. {accion_txt}"
    else:
        riesgo_sentence = "No se pudo calcular el índice de riesgo por datos insuficientes."

    if ranking is not None and len(ranking) > 0:
        top1 = ranking.iloc[0]
        if len(ranking) >= 2:
            top2 = ranking.iloc[1]
            area_txt = (
                f"Con base en su perfil integral, se recomienda orientar a {nombre} hacia "
                f"**{top1['nombre_area']}** ({top1['afinidad']:.1%} de afinidad) "
                f"como primera opción, y **{top2['nombre_area']}** "
                f"({top2['afinidad']:.1%}) como alternativa complementaria."
            )
        else:
            area_txt = (
                f"Con base en su perfil integral, se recomienda orientar a {nombre} hacia "
                f"**{top1['nombre_area']}** ({top1['afinidad']:.1%} de afinidad)."
            )
    else:
        area_txt = "No se generaron recomendaciones de área por datos insuficientes."

    p3 = f"{riesgo_sentence} {area_txt}"

    return f"{p1}\n\n{p2}\n\n{p3}"
