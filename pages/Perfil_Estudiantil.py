import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Perfil Integral del Estudiante",
    page_icon="🧑‍🎓",
    layout="wide"
)

st.title("🧑‍🎓 Perfil Integral del Estudiante")
st.caption("Análisis académico, social y emocional con generación automática de texto")

# =========================
# CARGA DE DATOS
# =========================
@st.cache_data
def load_formulario():
    df_formulario = pd.read_csv("datasets/Formulario.csv")
    return df_formulario

@st.cache_data
def load_observaciones():
    df_obs = pd.read_csv("datasets/observaciones.csv")
    return df_obs

df_formulario = load_formulario()
df_observaciones = load_observaciones()

st.write("Columnas del formulario:", df_formulario.columns)

# =========================
# FUNCIONES AUXILIARES
# =========================
def interpretar_peso(valor, positivo=True):
    if pd.isna(valor):
        return "no determinado"
    if valor >= 7:
        return "alto" if positivo else "preocupante"
    elif valor >= 4:
        return "medio"
    else:
        return "bajo" if positivo else "crítico"

def generar_perfil_estudiantil(codigo_estudiante, df_formulario, df_observaciones):
    estudiante = df_formulario[df_formulario["id_estudiante"] == codigo_estudiante].iloc[0]
    observaciones = df_observaciones[df_observaciones["id_estudiante"] == codigo_estudiante]

    perfil = f"""
## 📌 PERFIL ESTUDIANTIL INTEGRAL

**Nombre:** {estudiante['nombre_estudiante']}  
**Edad:** {estudiante.get('edad', 'N/D')}  
**Grado/Nivel:** {estudiante.get('grado_secundaria', 'N/D')}

### 🏠 Entorno Familiar y Social
- Convivencia con los padres: **{interpretar_peso(estudiante.get('vive_con_padres', None))}**
- Nivel educativo de los padres: **{interpretar_peso(estudiante.get('nivel_educativo_padres', None))}**
- Apoyo familiar general: **{interpretar_peso(estudiante.get('apoyo_familiar', None))}**

### 📚 Condiciones Académicas y Estudio
- Acceso a recursos educativos: **{interpretar_peso(estudiante.get('recursos_educativos', None))}**
- Horas de estudio: **{interpretar_peso(estudiante.get('horas_estudio', None))}**
- Entorno saludable/silencioso: **{interpretar_peso(estudiante.get('entorno_saludable', None))}**
- Motivación académica: **{interpretar_peso(estudiante.get('motivacion_estudio', None))}**

### 🧑‍🤝‍🧑 Integración Social
- Integración social: **{interpretar_peso(estudiante.get('integracion_social', None))}**
- Exposición a bullying: **{interpretar_peso(estudiante.get('ausencia_bullying', None), positivo=False)}**

### 🏥 Salud y Entorno
- Estado de salud: **{interpretar_peso(estudiante.get('estado_salud', None))}**
- Acceso a servicios de salud: **{interpretar_peso(estudiante.get('acceso_servicios_salud', None))}**
- Seguridad del barrio: **{interpretar_peso(estudiante.get('seguridad_barrio', None))}**
- Riesgo drogas en entorno: **{interpretar_peso(estudiante.get('riesgo_drogas_entorno', None), positivo=False)}**
"""

    # Observaciones
    perfil += "\n### 🗒️ Observaciones Registradas\n"
    if observaciones.empty:
        perfil += "- No se registran observaciones cualitativas para este estudiante.\n"
    else:
        for _, obs in observaciones.iterrows():
            perfil += f"- Fecha: {obs.get('fecha','N/D')}, Autor: {obs.get('autor','N/D')}, Observación: {obs.get('observacion','N/D')}\n"

    # Conclusión
    perfil += f"""
### 🧩 Conclusión General
El estudiante **{estudiante['nombre_estudiante']}** presenta un perfil integral que permite identificar fortalezas y áreas de riesgo. Esta información puede ser utilizada por la institución para diseñar estrategias de acompañamiento académico, emocional y social.
"""
    return perfil

# =========================
# STREAMLIT: SELECCIÓN DE ESTUDIANTE
# =========================
st.subheader("🎓 Selecciona un estudiante")
sel = st.selectbox(
    "Estudiante",
    sorted(df_formulario["nombre_estudiante"].dropna().astype(str).unique())
)

codigo_sel = df_formulario[df_formulario["nombre_estudiante"] == sel]["id_estudiante"].iloc[0]
perfil = generar_perfil_estudiantil(codigo_sel, df_formulario, df_observaciones)

st.markdown(perfil)
