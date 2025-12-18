import pandas as pd
import random

# Diccionarios de sinónimos
sinonimos_peso = {
    "alto": ["alto", "muy alto", "destacado", "sobresaliente"],
    "medio": ["medio", "moderado", "intermedio"],
    "bajo": ["bajo", "limitado", "escaso"],
    "preocupante": ["preocupante", "alarmante", "grave"],
    "crítico": ["crítico", "severo", "grave"]
}

def interpretar_peso(valor, positivo=True):
    if pd.isna(valor):
        return "no determinado"
    if valor >= 7:
        return random.choice(sinonimos_peso["alto"] if positivo else sinonimos_peso["preocupante"])
    elif valor >= 4:
        return random.choice(sinonimos_peso["medio"])
    else:
        return random.choice(sinonimos_peso["bajo"] if positivo else sinonimos_peso["crítico"])

# Encabezados posibles para cada sección
encabezados = {
    "familiar": ["🏠 Entorno Familiar y Social", "👨‍👩‍👧 Familia y Apoyo", "🏡 Contexto Familiar"],
    "academico": ["📚 Condiciones Académicas y Estudio", "📖 Rendimiento y Recursos", "📝 Perfil Académico"],
    "social": ["🧑‍🤝‍🧑 Integración Social", "🌐 Relaciones y Comunidad", "🤝 Participación Social"],
    "salud": ["🏥 Salud y Bienestar", "💊 Estado de Salud", "🩺 Condiciones Físicas y Emocionales"]
}

# Plantilla base con placeholders
frases_plantilla = {
    "familiar": [
        "Convivencia con los padres: {vive}. Esto influye en su estabilidad emocional y acompañamiento académico.",
        "Nivel educativo de los padres: {edu}, afectando la orientación académica.",
        "Apoyo familiar: {apoyo}, clave para su motivación y permanencia.",
    ],
    "academico": [
        "Acceso a recursos educativos: {recursos}.",
        "Horas de estudio: {horas}, influyendo en su rendimiento.",
        "Entorno de estudio: {entorno}, favoreciendo la concentración.",
        "Motivación académica: {motivacion}, determinante para el progreso."
    ],
    "social": [
        "Integración social: {integracion}.",
        "Exposición a bullying: {bullying}.",
        "Participación en actividades extracurriculares: {integracion}.",
        "El entorno familiar influye en la interacción social: {vive}."
    ],
    "salud": [
        "Estado de salud: {salud}.",
        "Acceso a servicios de salud: {serv_salud}.",
        "Seguridad del barrio: {seguridad}.",
        "El bienestar emocional se ve afectado por la convivencia familiar: {vive}."
    ]
}

def generar_perfil_estudiantil(codigo_estudiante, df_formulario, df_observaciones):
    estudiante = df_formulario[df_formulario["id_estudiante"] == codigo_estudiante].iloc[0]
    observaciones = df_observaciones[df_observaciones["id_estudiante"] == codigo_estudiante]

    perfil = f"## 📌 PERFIL ESTUDIANTIL INTEGRAL\n\n"
    perfil += f"**Nombre:** {estudiante['nombre_estudiante']}\n\n"
    perfil += f"**Edad:** {estudiante.get('edad', 'N/D')}\n\n"
    perfil += f"**Grado/Nivel:** {estudiante.get('grado_secundaria', 'N/D')}\n\n"

    # -------------------------
    # Mezclar secciones y encabezados aleatorios
    # -------------------------
    secciones = list(frases_plantilla.keys())
    random.shuffle(secciones)

    for sec in secciones:
        # Elegir un encabezado aleatorio
        encabezado = random.choice(encabezados[sec])
        perfil += f"### {encabezado}\n"

        # Número aleatorio de frases por sección
        n_frases = random.randint(2, min(3, len(frases_plantilla[sec])))
        frases_seleccionadas = random.sample(frases_plantilla[sec], n_frases)

        for f in frases_seleccionadas:
            perfil += "- " + f.format(
                vive=interpretar_peso(estudiante.get("vive_con_padres")),
                edu=interpretar_peso(estudiante.get("nivel_educativo_padres")),
                apoyo=interpretar_peso(estudiante.get("apoyo_familiar")),
                recursos=interpretar_peso(estudiante.get("recursos_educativos")),
                horas=interpretar_peso(estudiante.get("horas_estudio")),
                entorno=interpretar_peso(estudiante.get("entorno_saludable")),
                motivacion=interpretar_peso(estudiante.get("motivacion_estudio")),
                integracion=interpretar_peso(estudiante.get("integracion_social")),
                bullying=interpretar_peso(estudiante.get("ausencia_bullying"), positivo=False),
                salud=interpretar_peso(estudiante.get("estado_salud")),
                serv_salud=interpretar_peso(estudiante.get("acceso_servicios_salud")),
                seguridad=interpretar_peso(estudiante.get("seguridad_barrio"))
            ) + "\n"
        perfil += "\n"

    # -------------------------
    # Observaciones
    # -------------------------
    perfil += "### 🗒️ Observaciones Registradas\n"
    if observaciones.empty:
        perfil += "- No se registran observaciones cualitativas.\n"
    else:
        for _, obs in observaciones.iterrows():
            perfil += f"- Fecha: {obs.get('fecha','N/D')}, Autor: {obs.get('autor','N/D')}, Observación: {obs.get('observacion','N/D')}\n"

    # -------------------------
    # Conclusión aleatoria
    # -------------------------
    conclusiones = [
        f"El estudiante {estudiante['nombre_estudiante']} presenta fortalezas y áreas de mejora. Se recomienda acompañamiento continuo.",
        f"Perfil de {estudiante['nombre_estudiante']} identifica oportunidades de desarrollo académico, social y emocional.",
        f"Se aconseja monitorear el progreso de {estudiante['nombre_estudiante']} para fortalecer su bienestar integral."
    ]
    perfil += f"\n### 🧩 Conclusión General\n"
    perfil += "- " + random.choice(conclusiones) + "\n"

    return perfil



