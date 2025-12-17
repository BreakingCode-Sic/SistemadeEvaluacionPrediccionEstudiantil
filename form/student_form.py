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
    col_fam1, col_fam2 = st.columns(2)
    with col_fam1:
        vive_padre = st.checkbox("Padre")
        vive_madre = st.checkbox("Madre")
        vive_ambos = st.checkbox("Ambos padres")
    with col_fam2:
        vive_ninguno = st.checkbox("Ninguno")
        vive_otro = st.checkbox("Otro familiar/tutor")
    
    hermanos = st.number_input("¿Cuántos hermanos tienes?", min_value=0, max_value=15, value=0)
    
    st.subheader("Nivel educativo de los padres/tutores")
    col_edu1, col_edu2 = st.columns(2)
    with col_edu1:
        edu_primaria = st.checkbox("Primaria")
        edu_secundaria = st.checkbox("Secundaria")
    with col_edu2:
        edu_universitario = st.checkbox("Universitario")
        edu_otro = st.checkbox("Otro nivel educativo")
    
    st.subheader("Estado laboral de los padres/tutores")
    col_lab1, col_lab2 = st.columns(2)
    with col_lab1:
        lab_empleado = st.checkbox("Empleado")
        lab_desempleado = st.checkbox("Desempleado")
    with col_lab2:
        lab_independiente = st.checkbox("Independiente/Emprendedor")
        lab_otro = st.checkbox("Otro estado laboral")
    
    st.subheader("¿Tienes acceso a recursos educativos en casa?")
    col_rec1, col_rec2 = st.columns(2)
    with col_rec1:
        rec_libros = st.checkbox("📚 Libros")
        rec_computadora = st.checkbox("💻 Computadora")
        rec_internet = st.checkbox("🌐 Internet")
    with col_rec2:
        rec_tutorias = st.checkbox("👨‍🏫 Tutorías")
        rec_otros = st.checkbox("📦 Otros recursos")
    
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
    col_vio1, col_vio2 = st.columns(2)
    with col_vio1:
        vio_robos = st.checkbox("🚨 Robos")
        vio_peleas = st.checkbox("👊 Peleas")
    with col_vio2:
        vio_drogas = st.checkbox("💊 Drogas")
        vio_acoso = st.checkbox("😰 Acoso")
    
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
    
    st.subheader("¿Alguna condición especial que afecte tu estudio?")
    col_cond1, col_cond2 = st.columns(2)
    with col_cond1:
        cond_visual = st.checkbox("👁️ Visual")
        cond_auditiva = st.checkbox("👂 Auditiva")
    with col_cond2:
        cond_emocional = st.checkbox("💭 Emocional")
        cond_otra = st.checkbox("🔷 Otra condición")
    
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
    
    st.subheader("Uso de dispositivos electrónicos para estudio")
    col_disp1, col_disp2 = st.columns(2)
    with col_disp1:
        disp_computadora = st.checkbox("💻 Computadora/Laptop")
        disp_tablet = st.checkbox("📱 Tablet")
    with col_disp2:
        disp_celular = st.checkbox("📲 Celular")
        disp_ninguno = st.checkbox("❌ Ningún dispositivo")
    
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
    
    st.subheader("¿En qué áreas crees que destacas?")
    col_area1, col_area2 = st.columns(2)
    with col_area1:
        area_logico = st.checkbox("🧮 Lógico-matemático", key="area_logico")
        area_cientifico = st.checkbox("🔭 Científico", key="area_cientifico")
        area_social = st.checkbox("🤝 Social", key="area_social")
    with col_area2:
        area_artistico = st.checkbox("🎭 Artístico", key="area_artistico")
        area_deportivo = st.checkbox("🏃 Deportivo", key="area_deportivo")
    
    st.subheader("¿Qué metas académicas tienes a corto plazo?")
    meta_corto_aprobar = st.checkbox("✅ Aprobar todas las materias con buenas calificaciones", key="meta_corto_aprobar")
    meta_corto_mejorar = st.checkbox("📈 Mejorar en áreas donde tengo dificultades", key="meta_corto_mejorar")
    meta_corto_participar = st.checkbox("🎯 Participar en proyectos o actividades extracurriculares", key="meta_corto_participar")
    meta_corto_habilidades = st.checkbox("💡 Desarrollar habilidades específicas (programación, matemáticas, escritura, ciencia)", key="meta_corto_habilidades")
    meta_corto_reconocimiento = st.checkbox("🏆 Obtener reconocimiento académico (certificados, concursos)", key="meta_corto_reconocimiento")
    meta_corto_habitos = st.checkbox("📚 Mejorar hábitos de estudio y organización", key="meta_corto_habitos")
    meta_corto_relaciones = st.checkbox("🤝 Fortalecer relaciones con profesores y compañeros para aprender mejor", key="meta_corto_relaciones")
    
    st.subheader("¿Qué metas tienes a largo plazo?")
    meta_largo_universidad = st.checkbox("🎓 Ingresar a la universidad o continuar estudios superiores", key="meta_largo_universidad")
    meta_largo_carrera = st.checkbox("💼 Elegir una carrera profesional específica", key="meta_largo_carrera")
    meta_largo_becas = st.checkbox("🏅 Obtener becas o reconocimientos académicos", key="meta_largo_becas")
    meta_largo_competencias = st.checkbox("🛠️ Desarrollar competencias profesionales (habilidades técnicas, idiomas, liderazgo)", key="meta_largo_competencias")
    meta_largo_investigacion = st.checkbox("🔬 Contribuir a proyectos de investigación o innovación", key="meta_largo_investigacion")
    meta_largo_impacto = st.checkbox("🌍 Tener un impacto positivo en la comunidad o entorno", key="meta_largo_impacto")
    meta_largo_red = st.checkbox("🌐 Desarrollar una red de contactos profesional y académica", key="meta_largo_red")
    
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
    
    st.subheader("Acceso a servicios básicos en casa")
    col_serv1, col_serv2 = st.columns(2)
    with col_serv1:
        serv_agua = st.checkbox("💧 Agua potable")
        serv_luz = st.checkbox("💡 Electricidad")
        serv_internet = st.checkbox("📶 Internet")
    with col_serv2:
        serv_saneamiento = st.checkbox("🚽 Saneamiento")
        serv_ninguno = st.checkbox("❌ Ninguno de los anteriores")
    
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
                "Vive_Padre": vive_padre,
                "Vive_Madre": vive_madre,
                "Vive_Ambos": vive_ambos,
                "Vive_Ninguno": vive_ninguno,
                "Vive_Otro": vive_otro,
                "Num_Hermanos": hermanos,
                "Edu_Primaria": edu_primaria,
                "Edu_Secundaria": edu_secundaria,
                "Edu_Universitario": edu_universitario,
                "Edu_Otro": edu_otro,
                "Lab_Empleado": lab_empleado,
                "Lab_Desempleado": lab_desempleado,
                "Lab_Independiente": lab_independiente,
                "Lab_Otro": lab_otro,
                "Rec_Libros": rec_libros,
                "Rec_Computadora": rec_computadora,
                "Rec_Internet": rec_internet,
                "Rec_Tutorias": rec_tutorias,
                "Rec_Otros": rec_otros,
                # Seguridad y entorno
                "Seguridad_Barrio": seguridad_barrio,
                "Vio_Robos": vio_robos,
                "Vio_Peleas": vio_peleas,
                "Vio_Drogas": vio_drogas,
                "Vio_Acoso": vio_acoso,
                "Ruido_Estudio": ruido_estudio,
                "Esp_Biblioteca": esp_biblioteca,
                "Esp_Centro": esp_centro,
                "Esp_Otro": esp_otro,
                # Salud y bienestar
                "Salud_General": salud_general,
                "Sal_Hospital": sal_hospital,
                "Sal_Clinica": sal_clinica,
                "Sal_Seguro": sal_seguro,
                "Sal_Ninguno": sal_ninguno,
                "Cond_Visual": cond_visual,
                "Cond_Auditiva": cond_auditiva,
                "Cond_Emocional": cond_emocional,
                "Cond_Otra": cond_otra,
                # Comportamiento y hábitos
                "Horas_Estudio": horas_estudio,
                "Act_Deportes": act_deportes,
                "Act_Arte": act_arte,
                "Act_Ciencia": act_ciencia,
                "Act_Voluntariado": act_voluntariado,
                "Act_Otro": act_otro,
                "Disp_Computadora": disp_computadora,
                "Disp_Tablet": disp_tablet,
                "Disp_Celular": disp_celular,
                "Disp_Ninguno": disp_ninguno,
                "Asistencia_Escuela": asistencia_escuela,
                # Contexto emocional y social
                "Apoyo_Familiar": apoyo_familiar,
                "Integracion_Companeros": integracion_companeros,
                "Bullying": bullying,
                "Ani_Alegre": ani_alegre,
                "Ani_Neutral": ani_neutral,
                "Ani_Triste": ani_triste,
                "Ani_Ansioso": ani_ansioso,
                "Ani_Otro": ani_otro,
                "Motivacion_Estudio": motivacion_estudio,
                # Percepción académica
                "Mat_Matematicas": mat_matematicas,
                "Mat_Ciencias": mat_ciencias,
                "Mat_Historia": mat_historia,
                "Mat_Idiomas": mat_idiomas,
                "Mat_Arte": mat_arte,
                "Mat_Deportes": mat_deportes,
                "Area_Logico": area_logico,
                "Area_Cientifico": area_cientifico,
                "Area_Social": area_social,
                "Area_Artistico": area_artistico,
                "Area_Deportivo": area_deportivo,
                # Metas corto plazo
                "Meta_Corto_Aprobar": meta_corto_aprobar,
                "Meta_Corto_Mejorar": meta_corto_mejorar,
                "Meta_Corto_Participar": meta_corto_participar,
                "Meta_Corto_Habilidades": meta_corto_habilidades,
                "Meta_Corto_Reconocimiento": meta_corto_reconocimiento,
                "Meta_Corto_Habitos": meta_corto_habitos,
                "Meta_Corto_Relaciones": meta_corto_relaciones,
                # Metas largo plazo
                "Meta_Largo_Universidad": meta_largo_universidad,
                "Meta_Largo_Carrera": meta_largo_carrera,
                "Meta_Largo_Becas": meta_largo_becas,
                "Meta_Largo_Competencias": meta_largo_competencias,
                "Meta_Largo_Investigacion": meta_largo_investigacion,
                "Meta_Largo_Impacto": meta_largo_impacto,
                "Meta_Largo_Red": meta_largo_red,
                # Contexto ampliado
                "Trans_Publico": trans_publico,
                "Trans_Privado": trans_privado,
                "Trans_Camina": trans_camina,
                "Serv_Agua": serv_agua,
                "Serv_Luz": serv_luz,
                "Serv_Internet": serv_internet,
                "Serv_Saneamiento": serv_saneamiento,
                "Serv_Ninguno": serv_ninguno,
                "Exposicion_Drogas": exposicion_drogas,
                "Cult_Biblioteca": cult_biblioteca,
                "Cult_Museo": cult_museo,
                "Cult_Cine": cult_cine,
                "Cult_Parques": cult_parques,
                "Cult_Otro": cult_otro,
            }
            
            # Save to CSV
            csv_file = "evaluaciones_estudiantes.csv"
            df_new = pd.DataFrame([student_data])
            
            if os.path.exists(csv_file):
                df_existing = pd.read_csv(csv_file)
                df_combined = pd.concat([df_existing, df_new], ignore_index=True)
                df_combined.to_csv(csv_file, index=False)
            else:
                df_new.to_csv(csv_file, index=False)
            
            st.info(f"📁 Datos guardados en {csv_file}")

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
if os.path.exists("evaluaciones_estudiantes.csv"):
    df = pd.read_csv("evaluaciones_estudiantes.csv")
    st.sidebar.metric("Total de Evaluaciones", len(df))
    
    if len(df) > 0:
        st.sidebar.markdown("---")
        st.sidebar.subheader("📈 Resumen Rápido")
        avg_seguridad = df["Seguridad_Barrio"].mean()
        avg_motivacion = df["Motivacion_Estudio"].mean()
        avg_apoyo = df["Apoyo_Familiar"].mean()
        
        st.sidebar.metric("Seguridad Promedio", f"{avg_seguridad:.1f}/5")
        st.sidebar.metric("Motivación Promedio", f"{avg_motivacion:.1f}/5")
        st.sidebar.metric("Apoyo Familiar Promedio", f"{avg_apoyo:.1f}/5")
else:
    st.sidebar.metric("Total de Evaluaciones", 0)

st.sidebar.markdown("---")
st.sidebar.markdown("**Samsung Innovation Campus Hackathon 2025** 🚀")

