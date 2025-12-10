import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
st.set_page_config(page_title="Riesgo de Deserción", page_icon="⚠️", layout="wide")

# --------------------------------------------------
# FUNCIONES NLP
# --------------------------------------------------

PALABRAS_POS = [
    "participativo","atento","motivación","esfuerzo","responsable","colaborador",
    "proactivo","excelente","comprometido","constante","interés","aprendizaje"
]
PALABRAS_NEG = [
    "desinterés","falta","problemas","conflicto","apatía","incumplimiento","excusas",
    "derrotista","respeto","inapropiado","minimiza","derrotista"
]

def extraer_features(texto, pos_list, neg_list):
    texto = texto.lower()
    feats = {}
    for p in pos_list:
        feats[f"pos_{p}"] = int(p in texto)
    for n in neg_list:
        feats[f"neg_{n}"] = int(n in texto)
    return feats

@st.cache_data
def cargar_modelo():
    df_train = pd.read_csv(os.path.join("datasets", "nlp_observaciones_entrenamiento.csv"))
    X = [extraer_features(txt, PALABRAS_POS, PALABRAS_NEG) for txt in df_train["texto"]]
    y = df_train["label"].values
    vec = DictVectorizer(sparse=False)
    X_vec = vec.fit_transform(X)
    clf = LogisticRegression().fit(X_vec, y)
    return clf, vec

clf, vec = cargar_modelo()

def puntaje_ambiente(texto):
    if pd.isna(texto) or not texto.strip():
        return 0.5
    feats = vec.transform([extraer_features(texto, PALABRAS_POS, PALABRAS_NEG)])
    return float(clf.predict_proba(feats)[0][1])
# --------------------------------------------------
# CARGA DATOS REALES
# --------------------------------------------------
@st.cache_data
def load_riesgo_data():
    folder = "datasets"
    est  = pd.read_csv(os.path.join(folder, "estudiantes.csv"))
    rend = pd.read_csv(os.path.join(folder, "rendimiento.csv"))
    obs  = pd.read_csv(os.path.join(folder, "observaciones.csv"))

    # nota promedio por estudiante
    periodos = ["P1","P2","P3","P4"]
    rend["nota"] = rend["CF"].fillna(rend[periodos].mean(axis=1))
    notas = rend.groupby("id_estudiante")["nota"].mean().reset_index(name="nota_promedio")

    # asistencia promedio
    asist = rend.groupby("id_estudiante")["asistencia"].mean().reset_index(name="asistencia")

    # observaciones concatenadas por estudiante
    obs_est = obs.groupby("id_estudiante")["observacion"].apply(lambda x: " | ".join(x)).reset_index(name="observaciones")

    # merge final
    riesgo = est.merge(notas, on="id_estudiante", how="left")\
                .merge(asist, on="id_estudiante", how="left")\
                .merge(obs_est, on="id_estudiante", how="left")
    
    return riesgo

df_riesgo = load_riesgo_data()

# --------------------------------------------------
# CÁLCULO DE RIESGO
# --------------------------------------------------

def calcular_riesgo_row(row):
    A = row["asistencia"] if pd.notna(row["asistencia"]) else 1.0
    N = row["nota_promedio"] if pd.notna(row["nota_promedio"]) else 75
    texto = row["observaciones"] if pd.notna(row["observaciones"]) else ""
    F = puntaje_ambiente(texto)
    riesgo_asistencia = 1 - (A / 100)
    riesgo_nota = max(0, 75 - N) / 100
    Rd = 0.25 * riesgo_asistencia + 0.25 * riesgo_nota + 0.5 * (1 - F)
    return round(Rd, 3), round(F, 3)

df_riesgo[["Rd", "F"]] = df_riesgo.apply(lambda row: pd.Series(calcular_riesgo_row(row)), axis=1)
df_riesgo = df_riesgo.sort_values("Rd", ascending=False).reset_index(drop=True)

# --------------------------------------------------
# INTERFAZ
# --------------------------------------------------
st.title("⚠️ Riesgo de Deserción Escolar (NLP + Factores Académicos)")

# KPIs
c1, c2, c3 = st.columns(3)
c1.metric("Total estudiantes", len(df_riesgo))
c2.metric("Riesgo promedio", f"{df_riesgo['Rd'].mean():.1%}")
c3.metric("Alta peligro (Rd>0.6)", (df_riesgo["Rd"] > 0.6).sum())

# Gráfico
st.subheader("Ranking de riesgo")
fig, ax = plt.subplots(figsize=(8, 4))
top = df_riesgo.head(20)
ax.barh(top["nombre_estudiante"], top["Rd"], color="crimson")
ax.set_xlabel("Riesgo de deserción (Rd)")
ax.set_title("Top 20 estudiantes con mayor riesgo")
st.pyplot(fig)

# Tabla detallada
st.subheader("Detalle por estudiante")
df_show = df_riesgo.copy()
df_show["nota_promedio"] = df_show["nota_promedio"].apply(lambda x: f"{x:.1f}")

st.dataframe(df_show[["id_estudiante", "nombre_estudiante", "nota_promedio",
                      "asistencia", "F", "Rd"]].style.format({
                          "asistencia": "{:.1%}",
                          "F": "{:.2f}",
                          "Rd": "{:.1%}"
                      }))

# Buscador
st.subheader("🔍 Consulta individual")
names = sorted(df_riesgo["nombre_estudiante"].dropna().astype(str).unique())
sel = st.selectbox("Estudiante", names)
row = df_riesgo[df_riesgo["nombre_estudiante"] == sel].iloc[0]
st.write(f"**Rd:** {row['Rd']:.1%} | **Nota:** {row['nota_promedio']:.1f} | **Asistencia:** {row['asistencia']:.1%} | **Ambiente (F):** {row['F']:.2f}")

# Observaciones del estudiante
obs_text = row["observaciones"]
if pd.notna(obs_text):
    with st.expander("📒 Ver observaciones"):
        for obs in obs_text.split(" | "):
            st.write("- " + obs)
else:
    st.info("Sin observaciones para este estudiante")

st.markdown("---")

st.caption("Modelo NLP + Fórmula Rd = 0.25·(1-A) + 0.25·(max(0,75-N)/100) + 0.5·(1-F)")