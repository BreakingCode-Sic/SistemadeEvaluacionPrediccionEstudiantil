
def interpretar_peso(valor, positivo=True):
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
    PERFIL ESTUDIANTIL INTEGRAL

    Nombre del estudiante: {estudiante["nombre_estudiante"]}
    Edad: {estudiante["edad"]}
    Grado / Nivel: {estudiante["grado_secundaria"]}

    El presente perfil ha sido generado automáticamente a partir del análisis
    de indicadores sociales, académicos, familiares y de observaciones cualitativas
    realizadas por el personal educativo.
    """

    # ENTORNO FAMILIAR
    perfil += f"""
    ENTORNO FAMILIAR Y SOCIAL

    El estudiante presenta un nivel {interpretar_peso(estudiante["vive_con_padres"])}
    en cuanto a la convivencia con los padres, lo cual influye directamente en su
    estabilidad emocional y acompañamiento académico.

    El nivel educativo de los padres es considerado
    {interpretar_peso(estudiante["nivel_educativo_padres"])}, lo que puede impactar en
    la capacidad de apoyo académico dentro del hogar.

    El apoyo familiar general se clasifica como
    {interpretar_peso(estudiante["apoyo_familiar"])}, siendo un factor clave en la
    permanencia y motivación del estudiante dentro del sistema educativo.
    """

    # CONDICIONES DE ESTUDIO
    perfil += f"""
    CONDICIONES DE ESTUDIO Y ENTORNO

    El acceso a recursos educativos presenta un nivel
    {interpretar_peso(estudiante["recursos_educativos"])}, mientras que las condiciones
    de seguridad del barrio son consideradas
    {interpretar_peso(estudiante["seguridad_barrio"])}.

    El entorno libre de violencia y el silencio para el estudio se evalúan como
    {interpretar_peso(estudiante["ausencia_violencia"])} y
    {interpretar_peso(estudiante["entorno_saludable"])}, respectivamente, factores
    que inciden directamente en la concentración y el rendimiento académico.
    """

    # SALUD
    perfil += f"""
    ESTADO DE SALUD

    El estado de salud general del estudiante es evaluado como
    {interpretar_peso(estudiante["estado_salud"])}, con un nivel de acceso a servicios
    de salud clasificado como
    {interpretar_peso(estudiante["acceso_servicios_salud"])}.
    """

    # DESEMPEÑO ACADÉMICO
    perfil += f"""
    DESEMPEÑO ACADÉMICO

    El estudiante dedica un número de horas de estudio con un nivel
    {interpretar_peso(estudiante["horas_estudio"])}, y su asistencia escolar se
    considera
    {interpretar_peso(estudiante["asistencia_escolar"])}.

    El nivel de motivación académica es
    {interpretar_peso(estudiante["motivacion_estudio"])}, siendo un indicador clave para
    el progreso y la permanencia escolar.
    """

    # RIESGOS
    perfil += f"""
    FACTORES DE RIESGO

    El riesgo asociado a situaciones de bullying se considera
    {interpretar_peso(estudiante["ausencia_bullying"], positivo=False)}.
    """

    # OBSERVACIONES
    perfil += "\nOBSERVACIONES REGISTRADAS\n"

    if observaciones.empty:
        perfil += "\nNo se registran observaciones cualitativas para este estudiante.\n"
    else:
        for _, obs in observaciones.iterrows():
            perfil += f"""
            - Fecha: {obs["fecha"]}
              Autor: {obs["autor"]}
              Observación: {obs["observacion"]}
            """

    # CONCLUSIÓN
    perfil += f"""
    CONCLUSIÓN GENERAL

    A partir del análisis integral de los factores evaluados, se concluye que el
    estudiante {estudiante["nombre_estudiante"]} presenta un perfil que requiere
    seguimiento continuo. La combinación de factores sociales, académicos y
    observacionales permite a la institución tomar decisiones informadas orientadas
    a la prevención de la deserción escolar y al fortalecimiento del bienestar
    integral del estudiante.
    """

    return perfil


