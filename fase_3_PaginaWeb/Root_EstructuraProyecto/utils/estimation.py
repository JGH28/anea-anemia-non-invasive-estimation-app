import os
from pathlib import Path
import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras
from pathlib import Path
from utils.segmentation import obtener_mascara, aplicar_mascara

# Carga del modelo Xception (solo una vez)
BASE_DIR =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_xcep_path = Path("models/best_xception_model.h5")
xception_model = keras.models.load_model(model_xcep_path, compile=False)

def preparar_entrada_xception(region_rgb: np.ndarray, H=224, W=224) -> np.ndarray:
    """Prepara la región conjuntival para el modelo Xception."""
    resized = cv2.resize(region_rgb, (W, H))
    arr = resized.astype(np.float32) / 255.0
    return np.expand_dims(arr, axis=0)

def estimar_hemoglobina(img_path: str):
    """Ejecuta el pipeline completo: segmentación y estimación."""
    bgr = cv2.imread(img_path)
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    mask = obtener_mascara(rgb)
    region = aplicar_mascara(rgb, mask)
    x_in = preparar_entrada_xception(region)
    y = xception_model.predict(x_in, verbose=0)
    valor = float(y.reshape(-1)[0])
    return {"valor": valor, "mask": mask, "region": region}
