import streamlit as st
import pandas as pd
from Menu_functions import leer_datos, guardar_datos

st.title("➕ Agregar nuevo estudiante")

df = leer_datos()

with st.form("nuevo_estudiante"):

    nombre = st.text_input("Nombre del estudiante")
    edad = st.number_input("Edad", 15, 60)
    area = st.selectbox("Área", ["Ciencias", "Economía", "Computación", "Medicina"])
    nota = st.slider("Nota promedio", 0, 100)
    semestre = st.number_input("Semestre", 1, 12)

    submitted = st.form_submit_button("Guardar")

if submitted:
    nuevo = {
        "id": len(df) + 1,
        "nombre_estudiante": nombre,
        "edad": edad,
        "area": area,
        "nota": nota,
        "semestre": semestre
    }
    df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
    guardar_datos(df)
    st.success("Estudiante agregado correctamente.")
