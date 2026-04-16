import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="torch")

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

_model = None

def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def recomendar_areas(perfil_texto, df_areas, top_k=5):
    model = _get_model()

    textos_areas = df_areas["texto_area"].astype(str).tolist()

    # codificar perfil y áreas en vectores de 384 dim
    embeddings = model.encode([perfil_texto] + textos_areas, show_progress_bar=False)

    perfil_vec = embeddings[0:1]
    areas_vecs = embeddings[1:]

    scores = cosine_similarity(perfil_vec, areas_vecs)[0]

    df_areas = df_areas.copy()
    df_areas["afinidad"] = scores.clip(0, 1)

    return df_areas.sort_values("afinidad", ascending=False).head(top_k)
