import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================
# CONFIGURACIÓN DE ESTILO
# ==========================

st.set_page_config(
    page_title="AcademiPredict - Dashboard",
    page_icon="🎓",
    layout="wide",
)

# CSS personalizado para el estilo premium
st.markdown("""
    <style>
        .main {
            background-color: #f5f6fa;
        }
        div.block-container {
            padding-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================
# COMPONENTES UI
# ==========================

def card(title, value, variation, color="green"):
    return f"""
    <div style="
        padding: 20px;
        border-radius: 15px;
        background: white;
        box-shadow: 0 2px 5px rgba(0,0,0,0.07);
        border: 1px solid #eee;
        height: 220px;
    ">
        <h4 style="margin: 0; font-weight: 500; color: #666;">{title}</h4>
        <h2 style="margin: 5px 0 8px 0; font-size: 30px; font-weight: 700; color:#111;">
            {value}
        </h2>
        <span style="color:{'green' if color=='green' else 'red'}; font-weight:600;">
            {variation}
        </span>
    </div>
    """

# ==========================
# CALCULO DE AMBIENTE (NLP MANUAL)
# ==========================

def calcular_ambiente(observaciones):
    keywords_negativas = ["estres", "problema", "dificultad", "ansiedad", "bullying", "falta", "conflicto", "desmotivado"]
    keywords_positivas = ["participativo", "positivo", "excelente", "tranquilo", "comprometido"]

    score = 0

    for obs in observaciones:
        t = obs.lower()
        for k in keywords_negativas:
            if k in t:
                score -= 1
        for k in keywords_positivas:
            if k in t:
                score += 1

    # Normalizar entre 0 y 1
    ambiente = (score + 5) / 10
    return max(0, min(1, ambiente))

# ==========================
# CALCULO DE RIESGO RD
# ==========================

def calcular_riesgo(A, N, E, O):
    Rd = 0.25*(1-A) + 0.25*max(0, (75-N)/75) + 0.40*(1-E) + 0.10*O
    return round(Rd, 3)

# ==========================
# DATOS DE PRUEBA
# ==========================

df = pd.DataFrame({
    "estudiante": ["Juan Pérez", "María López", "Carlos Ruiz"],
    "materia": ["Lengua y Literatura", "Matematica", "Fisica"],
    "promedio": [88, 79, 65],
    "asistencia": [0.92, 0.85, 0.60],
    "engagement": [0.90, 0.72, 0.40],
    "observaciones": [
        ["Muy participativo", "Excelente actitud"],
        ["Se estresa fácilmente", "Le cuesta algunas materias"],
        ["Problemas de conducta", "Conflicto con compañeros", "Desmotivado"]
    ]
})

# Calcular ambiente y riesgo
df["ambiente"] = df["observaciones"].apply(lambda obs: calcular_ambiente(obs))
df["riesgo"] = df.apply(lambda row: calcular_riesgo(
    row["asistencia"],
    row["promedio"],
    row["engagement"],
    1 - row["ambiente"]
), axis=1)

# ==========================
# SIDEBAR
# ==========================

st.sidebar.title("📊 AcademiPredict")
st.sidebar.caption("Análisis Predictivo Institucional")

page = st.sidebar.radio(
    "Navegación",
    ["🏠 Dashboard", "👥 Estudiantes", "📄 Reportes", "🔮 Predicciones", "⚙️ Configuración"],
    label_visibility="collapsed"
)

# Redirección basada en selección
if page == "🏠 Dashboard":
    st.switch_page("app.py")
elif page == "👥 Estudiantes":
    st.switch_page("pages/Estudiantes.py")
elif page == "📄 Reportes":
    st.switch_page("pages/Reportes.py")
elif page == "🔮 Predicciones":
    st.switch_page("pages/04_🔮_Predicciones.py")
elif page == "⚙️ Configuración":
    # Puedes crear otra página o manejarlo aquí
    st.info("Página de configuración")


# st.sidebar.markdown("### 🏠 Dashboard")
# st.sidebar.markdown("### 👥 Estudiantes")
# st.sidebar.markdown("### 📄 Reportes")
# st.sidebar.markdown("### 🔮 Predicciones")
# st.sidebar.markdown("### ⚙️ Configuración")

# st.sidebar.markdown("---")
# st.sidebar.markdown("Administradora: **Dra. Ana Torres**")

# ==========================
# TITULO + FILTROS
# ==========================

st.title("Dashboard Institucional")

f1, f2 = st.columns(2)

with f1:
    periodo = st.selectbox("Periodo", ["2024-I", "2024-II"])


with f2:
    materia = st.selectbox("Materia", ["Todas"] + df["materia"].unique().tolist())

# Filtrar por materia
df_filtrado = df if materia == "Todas" else df[df["Materia"] == materia]

# ==========================
# KPIs
# ==========================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(card("Estudiantes Activos", len(df_filtrado), "+2.1%", "green"), unsafe_allow_html=True)

with col2:
    st.markdown(card("Tasa Deserción Proyectada", f"{round(df_filtrado['riesgo'].mean()*100,1)}%", "-0.5%", "red"), unsafe_allow_html=True)

with col3:
    st.markdown(card("Rendimiento Promedio", f"{round(df_filtrado['promedio'].mean(),1)}/100", "+1.2 pts", "green"), unsafe_allow_html=True)

with col4:
    st.markdown(card("Estudiantes en Riesgo", (df_filtrado['riesgo'] > 0.5).sum(), "+3.4%", "red"), unsafe_allow_html=True)

# ==========================
# GRAFICA PRINCIPAL
# ==========================

st.subheader("Rendimiento por Materias")

fig = px.bar(
    df,
    x="materia",
    y="promedio",
    color="materia",
    title="",
    height=350
)

fig.update_layout(showlegend=False)
st.plotly_chart(fig, use_container_width=True)

# ==========================
# PANEL DERECHO (ACCIONES PRIORITARIAS)
# ==========================

st.subheader("Acciones Prioritarias")

for index, row in df.sort_values(by="riesgo", ascending=False).head(3).iterrows():
    st.markdown(f"""
    <div style='padding:15px; background:#ffe6e6; border-radius:10px; margin-bottom:12px;'>
        <strong>{row['estudiante']}</strong><br>
        <span style='color:#c00;'>Riesgo Alto ({row['riesgo']})</span>
    </div>
    """, unsafe_allow_html=True)

# ==========================
# TABLA DETALLADA
# ==========================

st.subheader("Detalle de estudiantes")
st.dataframe(df)
