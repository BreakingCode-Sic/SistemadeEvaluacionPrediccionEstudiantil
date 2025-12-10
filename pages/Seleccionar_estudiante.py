import streamlit as st
import pandas as pd
from Menu_functions import leer_datos, get_student_by_id

st.title("🔍 Seleccionar estudiante por ID")

df = leer_datos()
if df is None or df.empty:
    st.error("No hay datos disponibles.")
    st.stop()

ids = df["id"].tolist()
selected_id = st.selectbox("Selecciona el ID del estudiante:", ids)

if st.button("Buscar"):
    est = get_student_by_id(df, selected_id)
    st.write(est)
