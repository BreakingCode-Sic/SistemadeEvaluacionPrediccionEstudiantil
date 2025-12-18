"""
Student Contextual Evaluation Form

This module provides an interactive web form for collecting comprehensive contextual data
about students, which is essential for the student evaluation and prediction system.

Purpose:
    Collects multi-dimensional student data including:
    - Personal and demographic information
    - Family context (structure, education, employment, resources)
    - Safety and environment factors
    - Health and well-being indicators
    - Behavioral patterns and study habits
    - Emotional and social context
    - Academic perceptions and goals
    - Extended contextual data (transportation, basic services, cultural access)

Integration with the System:
    This form serves as a data collection frontend for the broader Sistema de Evaluación
    y Predicción Estudiantil (Student Evaluation and Prediction System). The collected
    data is stored in 'evaluaciones_estudiantes.csv' and can be combined with:
    - Academic performance data (grades, attendance)
    - Teacher observations
    - ML models for dropout risk prediction (core/models_riesgo.py)
    - Academic area recommendation models (core/models_area.py)

Data Usage:
    The collected data is used to:
    1. Identify risk factors for academic dropout
    2. Provide personalized academic and professional recommendations
    3. Generate comprehensive student profiles for intervention planning
    4. Train and improve ML prediction models with contextual features
    5. Analyze correlations between environmental/social factors and academic outcomes

Data Storage:
    All responses are saved to 'evaluaciones_estudiantes.csv' with:
    - Timestamp for tracking
    - Raw boolean/numeric values for each indicator
    - Normalized scores (0-1 scale) for weighted factor groups
    - Full confidentiality and academic-purpose authorization

Technical Implementation:
    Built with Streamlit for web interface, uses weighted scoring system for
    multi-factor indicators, implements form validation and data normalization.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="Formulario Estudiantil - Evaluación de Contexto",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stForm {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
    }
    h1 {
        color: #1e3a5f;
    }
    h2 {
        color: #2c5282;
        border-bottom: 2px solid #4299e1;
        padding-bottom: 10px;
    }
    h3 {
        color: #3182ce;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("🎓 Formulario de Evaluación Estudiantil")
st.markdown("### Evaluación de contexto y factores de riesgo académico")
st.markdown("Por favor, completa todas las secciones del formulario. Tu información será tratada de forma confidencial.")
st.markdown("---")

# Create a form
with st.form("student_form"):
    
    # ==================== SECCIÓN 1: DATOS PERSONALES ====================
    st.header("1. 📋 Datos Personales")
    
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombre completo *", placeholder="Ingresa tu nombre completo")
        edad = st.number_input("Edad *", min_value=5, max_value=25, value=12)
    with col2:
        codigo_estudiante = st.text_input("Código de estudiante *", placeholder="Ej: EST-2025-001")
        grado = st.selectbox("Grado/Nivel *", 
            ["Seleccionar...", "1° Primaria", "2° Primaria", "3° Primaria", "4° Primaria", 
             "5° Primaria", "6° Primaria", "1° Secundaria", "2° Secundaria", 
             "3° Secundaria", "4° Secundaria", "5° Secundaria", "6° Secundaria"])
    
    st.markdown("---")
    
    # ==================== SECCIÓN 2: CONTEXTO FAMILIAR ====================
    st.header("2. 👨‍👩‍👧‍👦 Contexto Familiar")
    
    st.subheader("¿Vives con tus padres?")
    tipo_convivencia = st.radio(
        "Selecciona con quién vives principalmente",
        ["Padre", "Madre", "Ambos padres", "Ninguno", "Otro familiar/tutor"],
        index=2
    )
    vive_padre = tipo_convivencia == "Padre"
    vive_madre = tipo_convivencia == "Madre"
    vive_ambos = tipo_convivencia == "Ambos padres"
    vive_ninguno = tipo_convivencia == "Ninguno"
    vive_otro = tipo_convivencia == "Otro familiar/tutor"
    
    # Calcular puntaje de estructura familiar
    familia_pesos = {
        "Vive_Ambos": 0.40,
        "Vive_Padre": 0.15,
        "Vive_Madre": 0.15,
        "Vive_Otro": 0.20,
        "Vive_Ninguno": 0.10
    }
    familia_score = 0
    if vive_ambos:
        familia_score += familia_pesos["Vive_Ambos"]
    if vive_padre:
        familia_score += familia_pesos["Vive_Padre"]
    if vive_madre:
        familia_score += familia_pesos["Vive_Madre"]
    if vive_otro:
        familia_score += familia_pesos["Vive_Otro"]
    if vive_ninguno:
        familia_score += familia_pesos["Vive_Ninguno"]
    familia_normalizado = familia_score / sum(familia_pesos.values())
    
    hermanos = st.number_input("¿Cuántos hermanos tienes?", min_value=0, max_value=15, value=0)
    
    st.subheader("Nivel educativo de los padres/tutores")
    col_edu1, col_edu2 = st.columns(2)
    with col_edu1:
        edu_primaria = st.checkbox("Primaria")
        edu_secundaria = st.checkbox("Secundaria")
    with col_edu2:
        edu_universitario = st.checkbox("Universitario")
        edu_otro = st.checkbox("Otro nivel educativo")
    
    # Calcular puntaje de nivel educativo
    educacion_pesos = {
        "Edu_Universitario": 0.45,
        "Edu_Secundaria": 0.30,
        "Edu_Primaria": 0.15,
        "Edu_Otro": 0.10
    }
    educacion_score = 0
    if edu_universitario:
        educacion_score += educacion_pesos["Edu_Universitario"]
    if edu_secundaria:
        educacion_score += educacion_pesos["Edu_Secundaria"]
    if edu_primaria:
        educacion_score += educacion_pesos["Edu_Primaria"]
    if edu_otro:
        educacion_score += educacion_pesos["Edu_Otro"]
    educacion_normalizado = educacion_score / sum(educacion_pesos.values())
    
    st.subheader("Estado laboral de los padres/tutores")
    col_lab1, col_lab2 = st.columns(2)
    with col_lab1:
        lab_empleado = st.checkbox("Empleado")
        lab_desempleado = st.checkbox("Desempleado")
    with col_lab2:
        lab_independiente = st.checkbox("Independiente/Emprendedor")
        lab_otro = st.checkbox("Otro estado laboral")
    
    # Calcular puntaje de estabilidad laboral
    laboral_pesos = {
        "Lab_Empleado": 0.40,
        "Lab_Independiente": 0.35,
        "Lab_Otro": 0.15,
        "Lab_Desempleado": 0.10
    }
    laboral_score = 0
    if lab_empleado:
        laboral_score += laboral_pesos["Lab_Empleado"]
    if lab_independiente:
        laboral_score += laboral_pesos["Lab_Independiente"]
    if lab_otro:
        laboral_score += laboral_pesos["Lab_Otro"]
    if lab_desempleado:
        laboral_score += laboral_pesos["Lab_Desempleado"]
    laboral_normalizado = laboral_score / sum(laboral_pesos.values())
    
    st.subheader("¿Tienes acceso a recursos educativos en casa?")
    col_rec1, col_rec2 = st.columns(2)
    with col_rec1:
        rec_libros = st.checkbox("📚 Libros")
        rec_computadora = st.checkbox("💻 Computadora")
        rec_internet = st.checkbox("🌐 Internet")
    with col_rec2:
        rec_tutorias = st.checkbox("👨‍🏫 Tutorías")
        rec_otros = st.checkbox("📦 Otros recursos")
    
    # Calcular puntaje de recursos educativos
    recursos_pesos = {
        "Rec_Internet": 0.30,
        "Rec_Computadora": 0.25,
        "Rec_Libros": 0.20,
        "Rec_Tutorias": 0.15,
        "Rec_Otros": 0.10
    }
    recursos_score = 0
    if rec_internet:
        recursos_score += recursos_pesos["Rec_Internet"]
    if rec_computadora:
        recursos_score += recursos_pesos["Rec_Computadora"]
    if rec_libros:
        recursos_score += recursos_pesos["Rec_Libros"]
    if rec_tutorias:
        recursos_score += recursos_pesos["Rec_Tutorias"]
    if rec_otros:
        recursos_score += recursos_pesos["Rec_Otros"]
    recursos_normalizado = recursos_score / sum(recursos_pesos.values())
    
    if recursos_score > 0:
        st.caption(f"📊 Nivel de recursos educativos: {recursos_normalizado:.2f} (0=ninguno, 1=máximo)")
    
    st.markdown("---")
    
    # ==================== SECCIÓN 3: SEGURIDAD Y ENTORNO ====================
    st.header("3. 🏘️ Seguridad y Entorno")
    
    seguridad_barrio = st.slider(
        "¿Cómo calificas la seguridad en tu barrio?",
        min_value=1, max_value=5, value=3,
        help="1 = Muy inseguro, 5 = Muy seguro"
    )
    st.caption("1 = Muy inseguro | 2 = Inseguro | 3 = Regular | 4 = Seguro | 5 = Muy seguro")
    
    st.subheader("¿Existen problemas de violencia cerca de tu vivienda?")
    st.caption("Selecciona todos los que apliquen")
    col_vio1, col_vio2 = st.columns(2)
    with col_vio1:
        vio_robos = st.checkbox("🚨 Robos")
        vio_peleas = st.checkbox("👊 Peleas")
    with col_vio2:
        vio_drogas = st.checkbox("💊 Drogas")
        vio_acoso = st.checkbox("😰 Acoso")
    
    # Calcular puntaje de violencia con pesos
    violencia_pesos = {
        "Vio_Robos": 0.30,
        "Vio_Peleas": 0.25,
        "Vio_Drogas": 0.30,
        "Vio_Acoso": 0.15
    }
    violencia_score = 0
    if vio_robos:
        violencia_score += violencia_pesos["Vio_Robos"]
    if vio_peleas:
        violencia_score += violencia_pesos["Vio_Peleas"]
    if vio_drogas:
        violencia_score += violencia_pesos["Vio_Drogas"]
    if vio_acoso:
        violencia_score += violencia_pesos["Vio_Acoso"]
    
    # Normalizar a escala 0-1
    violencia_normalizado = violencia_score / sum(violencia_pesos.values())
    
    if violencia_score > 0:
        st.caption(f"⚠️ Nivel de exposición a violencia: {violencia_normalizado:.2f} (0=ninguno, 1=máximo)")
    
    ruido_estudio = st.slider(
        "¿Hay ruido constante que afecte tu estudio?",
        min_value=1, max_value=5, value=3,
        help="1 = Ningún ruido, 5 = Mucho ruido"
    )
    st.caption("1 = Ningún ruido | 2 = Poco ruido | 3 = Regular | 4 = Bastante ruido | 5 = Mucho ruido")
    
    st.subheader("¿Tienes acceso a espacios seguros para estudiar fuera de casa?")
    col_esp1, col_esp2 = st.columns(2)
    with col_esp1:
        esp_biblioteca = st.checkbox("📖 Biblioteca")
        esp_centro = st.checkbox("🏛️ Centro comunitario")
    with col_esp2:
        esp_otro = st.checkbox("🏫 Otro espacio seguro")
    
    # Calcular puntaje de espacios seguros
    espacios_pesos = {
        "Esp_Biblioteca": 0.45,
        "Esp_Centro": 0.35,
        "Esp_Otro": 0.20
    }
    espacios_score = 0
    if esp_biblioteca:
        espacios_score += espacios_pesos["Esp_Biblioteca"]
    if esp_centro:
        espacios_score += espacios_pesos["Esp_Centro"]
    if esp_otro:
        espacios_score += espacios_pesos["Esp_Otro"]
    espacios_normalizado = espacios_score / sum(espacios_pesos.values())
    
    st.markdown("---")
    
    # ==================== SECCIÓN 4: SALUD Y BIENESTAR ====================
    st.header("4. 🏥 Salud y Bienestar")
    
    salud_general = st.slider(
        "Estado general de salud",
        min_value=1, max_value=5, value=3,
        help="1 = Muy malo, 5 = Excelente"
    )
    st.caption("1 = Muy malo | 2 = Malo | 3 = Regular | 4 = Bueno | 5 = Excelente")
    
    st.subheader("Acceso a servicios de salud")
    col_sal1, col_sal2 = st.columns(2)
    with col_sal1:
        sal_hospital = st.checkbox("🏥 Hospital")
        sal_clinica = st.checkbox("🩺 Clínica")
    with col_sal2:
        sal_seguro = st.checkbox("📋 Seguro médico")
        sal_ninguno = st.checkbox("❌ Ningún acceso")
    
    # Calcular puntaje de acceso a salud
    salud_acceso_pesos = {
        "Sal_Seguro": 0.40,
        "Sal_Hospital": 0.35,
        "Sal_Clinica": 0.25,
        "Sal_Ninguno": 0.00
    }
    salud_acceso_score = 0
    if sal_seguro:
        salud_acceso_score += salud_acceso_pesos["Sal_Seguro"]
    if sal_hospital:
        salud_acceso_score += salud_acceso_pesos["Sal_Hospital"]
    if sal_clinica:
        salud_acceso_score += salud_acceso_pesos["Sal_Clinica"]
    if sal_ninguno:
        salud_acceso_score += salud_acceso_pesos["Sal_Ninguno"]
    salud_acceso_normalizado = salud_acceso_score / max(sum(salud_acceso_pesos.values()), 1.0)
    
    st.subheader("¿Alguna condición especial que afecte tu estudio?")
    col_cond1, col_cond2 = st.columns(2)
    with col_cond1:
        cond_visual = st.checkbox("👁️ Visual")
        cond_auditiva = st.checkbox("👂 Auditiva")
    with col_cond2:
        cond_emocional = st.checkbox("💭 Emocional")
        cond_otra = st.checkbox("🔷 Otra condición")
    
    # Calcular puntaje de condiciones especiales (mayor score = más condiciones)
    condiciones_pesos = {
        "Cond_Emocional": 0.35,
        "Cond_Visual": 0.25,
        "Cond_Auditiva": 0.25,
        "Cond_Otra": 0.15
    }
    condiciones_score = 0
    if cond_emocional:
        condiciones_score += condiciones_pesos["Cond_Emocional"]
    if cond_visual:
        condiciones_score += condiciones_pesos["Cond_Visual"]
    if cond_auditiva:
        condiciones_score += condiciones_pesos["Cond_Auditiva"]
    if cond_otra:
        condiciones_score += condiciones_pesos["Cond_Otra"]
    condiciones_normalizado = condiciones_score / sum(condiciones_pesos.values())
    
    st.markdown("---")
    
    # ==================== SECCIÓN 5: COMPORTAMIENTO Y HÁBITOS ====================
    st.header("5. 📖 Comportamiento y Hábitos")
    
    horas_estudio = st.slider(
        "Horas promedio de estudio diario",
        min_value=0, max_value=8, value=2,
        help="Horas dedicadas al estudio fuera del horario escolar"
    )
    
    st.subheader("Participación en actividades extracurriculares")
    col_act1, col_act2 = st.columns(2)
    with col_act1:
        act_deportes = st.checkbox("⚽ Deportes", key="act_deportes")
        act_arte = st.checkbox("🎨 Arte", key="act_arte")
        act_ciencia = st.checkbox("🔬 Ciencia", key="act_ciencia")
    with col_act2:
        act_voluntariado = st.checkbox("🤝 Voluntariado", key="act_voluntariado")
        act_otro = st.checkbox("📌 Otra actividad", key="act_otro")
    
    # Calcular puntaje de actividades extracurriculares
    actividades_pesos = {
        "Act_Ciencia": 0.25,
        "Act_Voluntariado": 0.25,
        "Act_Deportes": 0.20,
        "Act_Arte": 0.20,
        "Act_Otro": 0.10
    }
    actividades_score = 0
    if act_ciencia:
        actividades_score += actividades_pesos["Act_Ciencia"]
    if act_voluntariado:
        actividades_score += actividades_pesos["Act_Voluntariado"]
    if act_deportes:
        actividades_score += actividades_pesos["Act_Deportes"]
    if act_arte:
        actividades_score += actividades_pesos["Act_Arte"]
    if act_otro:
        actividades_score += actividades_pesos["Act_Otro"]
    actividades_normalizado = actividades_score / sum(actividades_pesos.values())
    
    st.subheader("Uso de dispositivos electrónicos para estudio")
    col_disp1, col_disp2 = st.columns(2)
    with col_disp1:
        disp_computadora = st.checkbox("💻 Computadora/Laptop")
        disp_tablet = st.checkbox("📱 Tablet")
    with col_disp2:
        disp_celular = st.checkbox("📲 Celular")
        disp_ninguno = st.checkbox("❌ Ningún dispositivo")
    
    # Calcular puntaje de dispositivos electrónicos
    dispositivos_pesos = {
        "Disp_Computadora": 0.45,
        "Disp_Tablet": 0.30,
        "Disp_Celular": 0.15,
        "Disp_Ninguno": 0.10
    }
    dispositivos_score = 0
    if disp_computadora:
        dispositivos_score += dispositivos_pesos["Disp_Computadora"]
    if disp_tablet:
        dispositivos_score += dispositivos_pesos["Disp_Tablet"]
    if disp_celular:
        dispositivos_score += dispositivos_pesos["Disp_Celular"]
    if disp_ninguno:
        dispositivos_score += dispositivos_pesos["Disp_Ninguno"]
    dispositivos_normalizado = dispositivos_score / sum(dispositivos_pesos.values())
    
    asistencia_escuela = st.slider(
        "Nivel de asistencia a la escuela",
        min_value=1, max_value=5, value=4,
        help="1 = Muy baja asistencia, 5 = Asistencia perfecta"
    )
    st.caption("1 = Muy baja | 2 = Baja | 3 = Regular | 4 = Buena | 5 = Excelente")
    
    st.markdown("---")
    
    # ==================== SECCIÓN 6: CONTEXTO EMOCIONAL Y SOCIAL ====================
    st.header("6. 💚 Contexto Emocional y Social")
    
    apoyo_familiar = st.slider(
        "¿Te sientes apoyado por tu familia?",
        min_value=1, max_value=5, value=3,
        help="1 = Nada apoyado, 5 = Muy apoyado"
    )
    st.caption("1 = Nada | 2 = Poco | 3 = Regular | 4 = Bastante | 5 = Mucho")
    
    integracion_companeros = st.slider(
        "¿Te sientes integrado con tus compañeros?",
        min_value=1, max_value=5, value=3,
        help="1 = Nada integrado, 5 = Muy integrado"
    )
    st.caption("1 = Nada | 2 = Poco | 3 = Regular | 4 = Bastante | 5 = Mucho")
    
    bullying = st.radio(
        "¿Has enfrentado bullying o acoso?",
        options=["No", "Sí"],
        horizontal=True
    )
    
    st.subheader("Estado de ánimo general")
    col_ani1, col_ani2 = st.columns(2)
    with col_ani1:
        ani_alegre = st.checkbox("😊 Alegre")
        ani_neutral = st.checkbox("😐 Neutral")
        ani_triste = st.checkbox("😢 Triste")
    with col_ani2:
        ani_ansioso = st.checkbox("😰 Ansioso")
        ani_otro = st.checkbox("🔷 Otro")
    
    # Calcular puntaje de estado de ánimo (mayor = mejor)
    animo_pesos = {
        "Ani_Alegre": 0.50,
        "Ani_Neutral": 0.25,
        "Ani_Otro": 0.15,
        "Ani_Ansioso": 0.05,
        "Ani_Triste": 0.05
    }
    animo_score = 0
    if ani_alegre:
        animo_score += animo_pesos["Ani_Alegre"]
    if ani_neutral:
        animo_score += animo_pesos["Ani_Neutral"]
    if ani_otro:
        animo_score += animo_pesos["Ani_Otro"]
    if ani_ansioso:
        animo_score += animo_pesos["Ani_Ansioso"]
    if ani_triste:
        animo_score += animo_pesos["Ani_Triste"]
    animo_normalizado = animo_score / sum(animo_pesos.values())
    
    motivacion_estudio = st.slider(
        "Motivación por el estudio",
        min_value=1, max_value=5, value=3,
        help="1 = Sin motivación, 5 = Muy motivado"
    )
    st.caption("1 = Nada motivado | 2 = Poco | 3 = Regular | 4 = Bastante | 5 = Muy motivado")
    
    st.markdown("---")
    
    # ==================== SECCIÓN 7: PERCEPCIÓN DEL ÁREA ACADÉMICA ====================
    st.header("7. 📚 Percepción del Área Académica")
    
    st.subheader("¿Cuáles son tus materias favoritas?")
    col_mat1, col_mat2, col_mat3 = st.columns(3)
    with col_mat1:
        mat_matematicas = st.checkbox("🔢 Matemáticas", key="mat_matematicas")
        mat_ciencias = st.checkbox("🔬 Ciencias", key="mat_ciencias")
    with col_mat2:
        mat_historia = st.checkbox("📜 Historia", key="mat_historia")
        mat_idiomas = st.checkbox("🌍 Idiomas", key="mat_idiomas")
    with col_mat3:
        mat_arte = st.checkbox("🎨 Arte", key="mat_arte")
        mat_deportes = st.checkbox("⚽ Deportes/Educación Física", key="mat_deportes")
    
    # Calcular puntaje de materias favoritas
    materias_pesos = {
        "Mat_Matematicas": 0.20,
        "Mat_Ciencias": 0.20,
        "Mat_Idiomas": 0.15,
        "Mat_Historia": 0.15,
        "Mat_Arte": 0.15,
        "Mat_Deportes": 0.15
    }
    materias_score = 0
    if mat_matematicas:
        materias_score += materias_pesos["Mat_Matematicas"]
    if mat_ciencias:
        materias_score += materias_pesos["Mat_Ciencias"]
    if mat_idiomas:
        materias_score += materias_pesos["Mat_Idiomas"]
    if mat_historia:
        materias_score += materias_pesos["Mat_Historia"]
    if mat_arte:
        materias_score += materias_pesos["Mat_Arte"]
    if mat_deportes:
        materias_score += materias_pesos["Mat_Deportes"]
    materias_normalizado = materias_score / sum(materias_pesos.values())
    
    st.subheader("¿En qué áreas crees que destacas?")
    col_area1, col_area2 = st.columns(2)
    with col_area1:
        area_logico = st.checkbox("🧮 Lógico-matemático", key="area_logico")
        area_cientifico = st.checkbox("🔭 Científico", key="area_cientifico")
        area_social = st.checkbox("🤝 Social", key="area_social")
    with col_area2:
        area_artistico = st.checkbox("🎭 Artístico", key="area_artistico")
        area_deportivo = st.checkbox("🏃 Deportivo", key="area_deportivo")
    
    # Calcular puntaje de áreas de destaque
    areas_pesos = {
        "Area_Logico": 0.25,
        "Area_Cientifico": 0.25,
        "Area_Social": 0.20,
        "Area_Artistico": 0.15,
        "Area_Deportivo": 0.15
    }
    areas_score = 0
    if area_logico:
        areas_score += areas_pesos["Area_Logico"]
    if area_cientifico:
        areas_score += areas_pesos["Area_Cientifico"]
    if area_social:
        areas_score += areas_pesos["Area_Social"]
    if area_artistico:
        areas_score += areas_pesos["Area_Artistico"]
    if area_deportivo:
        areas_score += areas_pesos["Area_Deportivo"]
    areas_normalizado = areas_score / sum(areas_pesos.values())
    
    st.subheader("¿Qué metas académicas tienes a corto plazo?")
    meta_corto_aprobar = st.checkbox("✅ Aprobar todas las materias con buenas calificaciones", key="meta_corto_aprobar")
    meta_corto_mejorar = st.checkbox("📈 Mejorar en áreas donde tengo dificultades", key="meta_corto_mejorar")
    meta_corto_participar = st.checkbox("🎯 Participar en proyectos o actividades extracurriculares", key="meta_corto_participar")
    meta_corto_habilidades = st.checkbox("💡 Desarrollar habilidades específicas (programación, matemáticas, escritura, ciencia)", key="meta_corto_habilidades")
    meta_corto_reconocimiento = st.checkbox("🏆 Obtener reconocimiento académico (certificados, concursos)", key="meta_corto_reconocimiento")
    meta_corto_habitos = st.checkbox("📚 Mejorar hábitos de estudio y organización", key="meta_corto_habitos")
    meta_corto_relaciones = st.checkbox("🤝 Fortalecer relaciones con profesores y compañeros para aprender mejor", key="meta_corto_relaciones")
    
    # Calcular puntaje de metas a corto plazo
    metas_corto_pesos = {
        "Meta_Corto_Aprobar": 0.20,
        "Meta_Corto_Mejorar": 0.20,
        "Meta_Corto_Habilidades": 0.15,
        "Meta_Corto_Habitos": 0.15,
        "Meta_Corto_Participar": 0.12,
        "Meta_Corto_Reconocimiento": 0.10,
        "Meta_Corto_Relaciones": 0.08
    }
    metas_corto_score = 0
    if meta_corto_aprobar:
        metas_corto_score += metas_corto_pesos["Meta_Corto_Aprobar"]
    if meta_corto_mejorar:
        metas_corto_score += metas_corto_pesos["Meta_Corto_Mejorar"]
    if meta_corto_habilidades:
        metas_corto_score += metas_corto_pesos["Meta_Corto_Habilidades"]
    if meta_corto_habitos:
        metas_corto_score += metas_corto_pesos["Meta_Corto_Habitos"]
    if meta_corto_participar:
        metas_corto_score += metas_corto_pesos["Meta_Corto_Participar"]
    if meta_corto_reconocimiento:
        metas_corto_score += metas_corto_pesos["Meta_Corto_Reconocimiento"]
    if meta_corto_relaciones:
        metas_corto_score += metas_corto_pesos["Meta_Corto_Relaciones"]
    metas_corto_normalizado = metas_corto_score / sum(metas_corto_pesos.values())
    
    st.subheader("¿Qué metas tienes a largo plazo?")
    meta_largo_universidad = st.checkbox("🎓 Ingresar a la universidad o continuar estudios superiores", key="meta_largo_universidad")
    meta_largo_carrera = st.checkbox("💼 Elegir una carrera profesional específica", key="meta_largo_carrera")
    meta_largo_becas = st.checkbox("🏅 Obtener becas o reconocimientos académicos", key="meta_largo_becas")
    meta_largo_competencias = st.checkbox("🛠️ Desarrollar competencias profesionales (habilidades técnicas, idiomas, liderazgo)", key="meta_largo_competencias")
    meta_largo_investigacion = st.checkbox("🔬 Contribuir a proyectos de investigación o innovación", key="meta_largo_investigacion")
    meta_largo_impacto = st.checkbox("🌍 Tener un impacto positivo en la comunidad o entorno", key="meta_largo_impacto")
    meta_largo_red = st.checkbox("🌐 Desarrollar una red de contactos profesional y académica", key="meta_largo_red")
    
    # Calcular puntaje de metas a largo plazo
    metas_largo_pesos = {
        "Meta_Largo_Universidad": 0.25,
        "Meta_Largo_Carrera": 0.20,
        "Meta_Largo_Competencias": 0.15,
        "Meta_Largo_Investigacion": 0.15,
        "Meta_Largo_Becas": 0.10,
        "Meta_Largo_Impacto": 0.10,
        "Meta_Largo_Red": 0.05
    }
    metas_largo_score = 0
    if meta_largo_universidad:
        metas_largo_score += metas_largo_pesos["Meta_Largo_Universidad"]
    if meta_largo_carrera:
        metas_largo_score += metas_largo_pesos["Meta_Largo_Carrera"]
    if meta_largo_competencias:
        metas_largo_score += metas_largo_pesos["Meta_Largo_Competencias"]
    if meta_largo_investigacion:
        metas_largo_score += metas_largo_pesos["Meta_Largo_Investigacion"]
    if meta_largo_becas:
        metas_largo_score += metas_largo_pesos["Meta_Largo_Becas"]
    if meta_largo_impacto:
        metas_largo_score += metas_largo_pesos["Meta_Largo_Impacto"]
    if meta_largo_red:
        metas_largo_score += metas_largo_pesos["Meta_Largo_Red"]
    metas_largo_normalizado = metas_largo_score / sum(metas_largo_pesos.values())
    
    st.markdown("---")
    
    # ==================== SECCIÓN 8: DATOS DE CONTEXTO AMPLIADO ====================
    st.header("8. 📊 Datos de Contexto Ampliado (Opcional)")
    st.caption("Esta sección es opcional pero ayuda a enriquecer el análisis de factores de riesgo")
    
    st.subheader("Transporte al colegio")
    col_trans1, col_trans2 = st.columns(2)
    with col_trans1:
        trans_publico = st.checkbox("🚌 Transporte público")
        trans_privado = st.checkbox("🚗 Transporte privado")
    with col_trans2:
        trans_camina = st.checkbox("🚶 Camina")
    
    # Calcular puntaje de transporte
    transporte_pesos = {
        "Trans_Privado": 0.45,
        "Trans_Publico": 0.35,
        "Trans_Camina": 0.20
    }
    transporte_score = 0
    if trans_privado:
        transporte_score += transporte_pesos["Trans_Privado"]
    if trans_publico:
        transporte_score += transporte_pesos["Trans_Publico"]
    if trans_camina:
        transporte_score += transporte_pesos["Trans_Camina"]
    transporte_normalizado = transporte_score / sum(transporte_pesos.values())
    
    st.subheader("Acceso a servicios básicos en casa")
    st.caption("Esta sección se refiere a servicios básicos del hogar (independientes de los recursos de estudio preguntados anteriormente).")
    col_serv1, col_serv2 = st.columns(2)
    with col_serv1:
        serv_agua = st.checkbox("💧 Agua potable")
        serv_luz = st.checkbox("💡 Electricidad")
        serv_internet = st.checkbox("📶 Servicio básico de internet en el hogar (uso general)")
    with col_serv2:
        serv_saneamiento = st.checkbox("🚽 Saneamiento")
        serv_ninguno = st.checkbox("❌ Ninguno de los anteriores")
    
    # Calcular puntaje de servicios básicos
    servicios_pesos = {
        "Serv_Agua": 0.30,
        "Serv_Luz": 0.30,
        "Serv_Saneamiento": 0.25,
        "Serv_Internet": 0.15,
        "Serv_Ninguno": 0.00
    }
    servicios_score = 0
    if serv_agua:
        servicios_score += servicios_pesos["Serv_Agua"]
    if serv_luz:
        servicios_score += servicios_pesos["Serv_Luz"]
    if serv_saneamiento:
        servicios_score += servicios_pesos["Serv_Saneamiento"]
    if serv_internet:
        servicios_score += servicios_pesos["Serv_Internet"]
    if serv_ninguno:
        servicios_score += servicios_pesos["Serv_Ninguno"]
    servicios_normalizado = servicios_score / max(sum(servicios_pesos.values()), 1.0)
    
    exposicion_drogas = st.radio(
        "Exposición a drogas o alcohol en entorno cercano",
        options=["No", "Sí", "No sabe"],
        horizontal=True
    )
    
    st.subheader("Acceso a actividades culturales o recreativas")
    col_cult1, col_cult2 = st.columns(2)
    with col_cult1:
        cult_biblioteca = st.checkbox("📚 Biblioteca pública", key="cult_biblioteca")
        cult_museo = st.checkbox("🏛️ Museo", key="cult_museo")
        cult_cine = st.checkbox("🎬 Cine", key="cult_cine")
    with col_cult2:
        cult_parques = st.checkbox("🌳 Parques", key="cult_parques")
        cult_otro = st.checkbox("🎭 Otro espacio cultural", key="cult_otro")
    
    # Calcular puntaje de actividades culturales
    cultura_pesos = {
        "Cult_Biblioteca": 0.30,
        "Cult_Museo": 0.25,
        "Cult_Parques": 0.20,
        "Cult_Cine": 0.15,
        "Cult_Otro": 0.10
    }
    cultura_score = 0
    if cult_biblioteca:
        cultura_score += cultura_pesos["Cult_Biblioteca"]
    if cult_museo:
        cultura_score += cultura_pesos["Cult_Museo"]
    if cult_parques:
        cultura_score += cultura_pesos["Cult_Parques"]
    if cult_cine:
        cultura_score += cultura_pesos["Cult_Cine"]
    if cult_otro:
        cultura_score += cultura_pesos["Cult_Otro"]
    cultura_normalizado = cultura_score / sum(cultura_pesos.values())
    
    st.markdown("---")
    
    # ==================== CONSENTIMIENTO Y ENVÍO ====================
    st.header("✅ Confirmación")
    
    consentimiento = st.checkbox("Confirmo que la información proporcionada es verdadera y autorizo su uso para fines académicos y de evaluación")
    
    # Submit button
    submitted = st.form_submit_button("📝 Enviar Formulario", use_container_width=True, type="primary")
    
    if submitted:
        # Validation
        if not nombre:
            st.error("❌ Por favor ingresa tu nombre completo.")
        elif not codigo_estudiante:
            st.error("❌ Por favor ingresa tu código de estudiante.")
        elif grado == "Seleccionar...":
            st.error("❌ Por favor selecciona tu grado.")
        elif not consentimiento:
            st.error("❌ Debes confirmar el consentimiento para enviar el formulario.")
        else:
            # Success!
            st.success("✅ ¡Formulario enviado exitosamente!")
            st.balloons()
            
            # Compile all data
            student_data = {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                # Datos personales
                "Nombre": nombre,
                "Edad": edad,
                "Codigo_Estudiante": codigo_estudiante,
                "Grado": grado,
                # Contexto familiar
                "Vive_Padre": 1 if vive_padre else 0,
                "Vive_Madre": 1 if vive_madre else 0,
                "Vive_Ambos": 1 if vive_ambos else 0,
                "Vive_Ninguno": 1 if vive_ninguno else 0,
                "Vive_Otro": 1 if vive_otro else 0,
                "Familia_Score": familia_score,
                "Familia_Normalizado": familia_normalizado,
                "Num_Hermanos": hermanos,
                "Edu_Primaria": 1 if edu_primaria else 0,
                "Edu_Secundaria": 1 if edu_secundaria else 0,
                "Edu_Universitario": 1 if edu_universitario else 0,
                "Edu_Otro": 1 if edu_otro else 0,
                "Educacion_Score": educacion_score,
                "Educacion_Normalizado": educacion_normalizado,
                "Lab_Empleado": 1 if lab_empleado else 0,
                "Lab_Desempleado": 1 if lab_desempleado else 0,
                "Lab_Independiente": 1 if lab_independiente else 0,
                "Lab_Otro": 1 if lab_otro else 0,
                "Laboral_Score": laboral_score,
                "Laboral_Normalizado": laboral_normalizado,
                "Rec_Libros": 1 if rec_libros else 0,
                "Rec_Computadora": 1 if rec_computadora else 0,
                "Rec_Internet": 1 if rec_internet else 0,
                "Rec_Tutorias": 1 if rec_tutorias else 0,
                "Rec_Otros": 1 if rec_otros else 0,
                "Recursos_Score": recursos_score,
                "Recursos_Normalizado": recursos_normalizado,
                # Seguridad y entorno
                "Seguridad_Barrio": seguridad_barrio,
                "Vio_Robos": 1 if vio_robos else 0,
                "Vio_Peleas": 1 if vio_peleas else 0,
                "Vio_Drogas": 1 if vio_drogas else 0,
                "Vio_Acoso": 1 if vio_acoso else 0,
                "Violencia_Score": violencia_score,
                "Violencia_Normalizado": violencia_normalizado,
                "Ruido_Estudio": ruido_estudio,
                "Esp_Biblioteca": 1 if esp_biblioteca else 0,
                "Esp_Centro": 1 if esp_centro else 0,
                "Esp_Otro": 1 if esp_otro else 0,
                "Espacios_Score": espacios_score,
                "Espacios_Normalizado": espacios_normalizado,
                # Salud y bienestar
                "Salud_General": salud_general,
                "Sal_Hospital": 1 if sal_hospital else 0,
                "Sal_Clinica": 1 if sal_clinica else 0,
                "Sal_Seguro": 1 if sal_seguro else 0,
                "Sal_Ninguno": 1 if sal_ninguno else 0,
                "Salud_Acceso_Score": salud_acceso_score,
                "Salud_Acceso_Normalizado": salud_acceso_normalizado,
                "Cond_Visual": 1 if cond_visual else 0,
                "Cond_Auditiva": 1 if cond_auditiva else 0,
                "Cond_Emocional": 1 if cond_emocional else 0,
                "Cond_Otra": 1 if cond_otra else 0,
                "Condiciones_Score": condiciones_score,
                "Condiciones_Normalizado": condiciones_normalizado,
                # Comportamiento y hábitos
                "Horas_Estudio": horas_estudio,
                "Act_Deportes": 1 if act_deportes else 0,
                "Act_Arte": 1 if act_arte else 0,
                "Act_Ciencia": 1 if act_ciencia else 0,
                "Act_Voluntariado": 1 if act_voluntariado else 0,
                "Act_Otro": 1 if act_otro else 0,
                "Actividades_Score": actividades_score,
                "Actividades_Normalizado": actividades_normalizado,
                "Disp_Computadora": 1 if disp_computadora else 0,
                "Disp_Tablet": 1 if disp_tablet else 0,
                "Disp_Celular": 1 if disp_celular else 0,
                "Disp_Ninguno": 1 if disp_ninguno else 0,
                "Dispositivos_Score": dispositivos_score,
                "Dispositivos_Normalizado": dispositivos_normalizado,
                "Asistencia_Escuela": asistencia_escuela,
                # Contexto emocional y social
                "Apoyo_Familiar": apoyo_familiar,
                "Integracion_Companeros": integracion_companeros,
                "Bullying": bullying,
                "Ani_Alegre": 1 if ani_alegre else 0,
                "Ani_Neutral": 1 if ani_neutral else 0,
                "Ani_Triste": 1 if ani_triste else 0,
                "Ani_Ansioso": 1 if ani_ansioso else 0,
                "Ani_Otro": 1 if ani_otro else 0,
                "Animo_Score": animo_score,
                "Animo_Normalizado": animo_normalizado,
                "Motivacion_Estudio": motivacion_estudio,
                # Percepción académica
                "Mat_Matematicas": 1 if mat_matematicas else 0,
                "Mat_Ciencias": 1 if mat_ciencias else 0,
                "Mat_Historia": 1 if mat_historia else 0,
                "Mat_Idiomas": 1 if mat_idiomas else 0,
                "Mat_Arte": 1 if mat_arte else 0,
                "Mat_Deportes": 1 if mat_deportes else 0,
                "Materias_Score": materias_score,
                "Materias_Normalizado": materias_normalizado,
                "Area_Logico": 1 if area_logico else 0,
                "Area_Cientifico": 1 if area_cientifico else 0,
                "Area_Social": 1 if area_social else 0,
                "Area_Artistico": 1 if area_artistico else 0,
                "Area_Deportivo": 1 if area_deportivo else 0,
                "Areas_Score": areas_score,
                "Areas_Normalizado": areas_normalizado,
                # Metas corto plazo
                "Meta_Corto_Aprobar": 1 if meta_corto_aprobar else 0,
                "Meta_Corto_Mejorar": 1 if meta_corto_mejorar else 0,
                "Meta_Corto_Participar": 1 if meta_corto_participar else 0,
                "Meta_Corto_Habilidades": 1 if meta_corto_habilidades else 0,
                "Meta_Corto_Reconocimiento": 1 if meta_corto_reconocimiento else 0,
                "Meta_Corto_Habitos": 1 if meta_corto_habitos else 0,
                "Meta_Corto_Relaciones": 1 if meta_corto_relaciones else 0,
                "Metas_Corto_Score": metas_corto_score,
                "Metas_Corto_Normalizado": metas_corto_normalizado,
                # Metas largo plazo
                "Meta_Largo_Universidad": 1 if meta_largo_universidad else 0,
                "Meta_Largo_Carrera": 1 if meta_largo_carrera else 0,
                "Meta_Largo_Becas": 1 if meta_largo_becas else 0,
                "Meta_Largo_Competencias": 1 if meta_largo_competencias else 0,
                "Meta_Largo_Investigacion": 1 if meta_largo_investigacion else 0,
                "Meta_Largo_Impacto": 1 if meta_largo_impacto else 0,
                "Meta_Largo_Red": 1 if meta_largo_red else 0,
                "Metas_Largo_Score": metas_largo_score,
                "Metas_Largo_Normalizado": metas_largo_normalizado,
                # Contexto ampliado
                "Trans_Publico": 1 if trans_publico else 0,
                "Trans_Privado": 1 if trans_privado else 0,
                "Trans_Camina": 1 if trans_camina else 0,
                "Transporte_Score": transporte_score,
                "Transporte_Normalizado": transporte_normalizado,
                "Serv_Agua": 1 if serv_agua else 0,
                "Serv_Luz": 1 if serv_luz else 0,
                "Serv_Internet": 1 if serv_internet else 0,
                "Serv_Saneamiento": 1 if serv_saneamiento else 0,
                "Serv_Ninguno": 1 if serv_ninguno else 0,
                "Servicios_Score": servicios_score,
                "Servicios_Normalizado": servicios_normalizado,
                "Exposicion_Drogas": exposicion_drogas,
                "Cult_Biblioteca": 1 if cult_biblioteca else 0,
                "Cult_Museo": 1 if cult_museo else 0,
                "Cult_Cine": 1 if cult_cine else 0,
                "Cult_Parques": 1 if cult_parques else 0,
                "Cult_Otro": 1 if cult_otro else 0,
                "Cultura_Score": cultura_score,
                "Cultura_Normalizado": cultura_normalizado,
            }
            
            # Save to CSV in datasets folder
            datasets_folder = os.path.join(os.path.dirname(__file__), "..", "datasets")
            os.makedirs(datasets_folder, exist_ok=True)
            csv_file = os.path.join(datasets_folder, "evaluaciones_estudiantes.csv")
            df_new = pd.DataFrame([student_data])
            
            if os.path.exists(csv_file):
                df_existing = pd.read_csv(csv_file)
                df_combined = pd.concat([df_existing, df_new], ignore_index=True)
                df_combined.to_csv(csv_file, index=False)
            else:
                df_new.to_csv(csv_file, index=False)
            
            st.info(f"📁 Datos guardados en {os.path.basename(csv_file)}")

# Sidebar
st.sidebar.title("ℹ️ Información")
st.sidebar.info(
    """
    **Formulario de Evaluación Estudiantil**
    
    Este formulario recopila información sobre el contexto 
    familiar, social, emocional y académico del estudiante 
    para identificar factores de riesgo y áreas de apoyo.
    
    Toda la información es confidencial.
    """
)

st.sidebar.title("📊 Estadísticas")
datasets_folder = os.path.join(os.path.dirname(__file__), "..", "datasets")
csv_file_path = os.path.join(datasets_folder, "evaluaciones_estudiantes.csv")

if os.path.exists(csv_file_path):
    try:
        df = pd.read_csv(csv_file_path)
    except pd.errors.EmptyDataError:
        df = pd.DataFrame()

    st.sidebar.metric("Total de Evaluaciones", len(df))

    if not df.empty:
        required_columns = {"Seguridad_Barrio", "Motivacion_Estudio", "Apoyo_Familiar"}
        if required_columns.issubset(df.columns):
            st.sidebar.markdown("---")
            st.sidebar.subheader("📈 Resumen Rápido")
            avg_seguridad = df["Seguridad_Barrio"].mean()
            avg_motivacion = df["Motivacion_Estudio"].mean()
            avg_apoyo = df["Apoyo_Familiar"].mean()

            st.sidebar.metric("Seguridad Promedio", f"{avg_seguridad:.1f}/5")
            st.sidebar.metric("Motivación Promedio", f"{avg_motivacion:.1f}/5")
            st.sidebar.metric("Apoyo Familiar Promedio", f"{avg_apoyo:.1f}/5")
        else:
            st.sidebar.warning(
                "No se pueden calcular estadísticas porque faltan columnas requeridas "
                "en el archivo de evaluaciones."
            )
else:
    st.sidebar.metric("Total de Evaluaciones", 0)

st.sidebar.markdown("---")
st.sidebar.markdown("**Samsung Innovation Campus Hackathon 2025** 🚀")

