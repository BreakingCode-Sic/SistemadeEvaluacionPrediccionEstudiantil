import re

PALABRAS_POS = [
    "participativo","atento","motivación","esfuerzo","responsable","colaborador",
    "proactivo","excelente","comprometido","constante","interés","aprendizaje",
    "participativa", "colaboradora", "responsable", "motivado", "proactivo", 
    "esfuerzo", "destacado", "excelente", "atento", "comprometido", "activo",
    "puntual", "asistencia", "constante", "iniciativa", "liderazgo", "respetuoso",
    "organizado", "autónomo", "perseverante", "curioso", "profundo", "reflexivo",
    "empático", "gratitud", "balance", "adaptable", "eficiente", "sobresaliente",
    "ejemplar", "dedicación", "entusiasta", "creativo", "analítico", "metódico",
    "disciplinado", "focalizado", "resiliente", "innovador", "colaborativo",
    "comunicativo", "propositivo", "visionario", "ordenado", "preciso", "detallista",
    "solidario", "paciente", "tolerante", "flexible", "autocrítico", "mejora",
    "evolución", "crecimiento", "superación", "exigente", "calidad", "excelencia",
    "potencial", "talento", "habilidad", "capacidad", "inteligente", "ágil",
    "rápido", "eficaz", "productivo", "constructivo", "positivo", "optimista",
    "alegre", "energético", "dinámico", "vital", "entregado", "compromiso",
    "vocación", "pasión", "interés", "dedicación", "constancia", "regularidad",
    "confiable", "confianza", "seguridad", "autoestima", "autonomía", "independiente",
    "maduro", "serio", "formal", "educado", "cortés", "amable", "gentil",
    "considerado", "atento", "detallista", "cuidadoso", "meticuloso", "perfeccionista",
    "exhaustivo", "completo", "integral", "holístico", "equilibrado", "armónico"
]

PALABRAS_NEG = [
    "desinterés", "dificultades", "timido", "timida", "falta", "conflicto", "apatía", "incumplimiento", "excusas",
    "derrotista", "inapropiado", "minimiza", "ausencias", "bajo rendimiento",
    "desmotivado", "distrae", "falta de motivación", "ausencia", "tardanza", "irrespetuoso",
    "evasión", "copia", "plagio", "desafiante", "aislamiento", "fatiga", "somnolencia",
    "negativa", "frustración", "ira", "falta materiales", "incapacidad", "disruptivo",
    "descuido", "promesas incumplidas", "resistencia",
    "problemas personales", "agresivo", "pasivo-agresivo", "abandono",
    "ausencia objetivos", "historial conflictivo", "evasivo",
    "deterioro", "postura cerrada", "estrés", "indiferencia",
    "negligencia", "irresponsable", "inconstante", "inestable", "volátil", "impulsivo",
    "agresividad", "violencia", "acoso", "bullying", "marginación", "exclusión",
    "discriminación", "intolerante", "engaño", "mentira", "fraude", "trampa",
    "chantaje", "manipulación", "arrogancia", "soberbia", "prepotencia",
    "celoso", "envidioso", "rencoroso", "vengativo", "resentimiento",
    "pesimismo", "fatalista", "ansiedad", "depresión",
    "desánimo", "desaliento", "desesperanza", "deserción", "desistimiento",
    "renuncia", "fracaso", "reprobación", "suspensión", "expulsión", "sanción",
    "amonestación", "llamado atención",
    "vulnerabilidad", "debilidad", "deficiencia",
    "carencia", "dependencia", "inseguridad", "caos",
    "desorden", "confusión", "desorientación", "perdido", "inadaptado",
    "incomprendido", "solitario", "aislado", "marginado", "excluido", "rechazado",
    "ignorado", "bloqueado", "paralizado", "estancado", "regresión", "retroceso",
    "decaimiento", "pérdida", "empeoramiento", "agravamiento", "complicación", "crisis"
]

MODIFICADORES = [
    "muy", "extremadamente", "totalmente", "completamente", "absolutamente",
    "realmente", "verdaderamente", "genuinamente", "profundamente", "intensamente",
    "levemente", "ligeramente", "moderadamente", "parcialmente", "ocasionalmente",
    "frecuentemente", "constantemente", "siempre", "nunca", "jamás", "rara vez",
    "a veces", "generalmente", "habitualmente", "usualmente", "típicamente"
]

RIESGO_EXPR = [
    "riesgo de deserción", "posible abandono", "en observación", "necesita apoyo",
    "requiere atención", "situación vulnerable", "contexto complicado", "factores de riesgo",
    "indicadores alarmantes", "señales de alerta", "comportamiento preocupante",
    "rendimiento decreciente", "motivación en caída", "interés disminuido",
    "participación reducida", "compromiso menguante", "esfuerzo decreciente",
    "asistencia irregular", "puntualidad deficiente", "organización pobre",
    "planificación ausente", "metas indefinidas", "autoeficacia baja"
]
PALABRAS_CIENCIA = [
    "experimento","cientifico","ciencia","laboratorio",
    "investigacion","quimica","biologia","fisica"
]

PALABRAS_NUMERO = [
    "logico","numerico","calculo","analisis",
    "matematico","razonamiento"
]

PALABRAS_SOCIAL = [
    "lider","equipo","comunicacion","debate",
    "argumenta","expresa","oratoria"
]
