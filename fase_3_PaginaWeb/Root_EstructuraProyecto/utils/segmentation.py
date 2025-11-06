import os
import numpy as np
import torch
import torch.nn.functional as F
import cv2
from transformers import AutoImageProcessor, AutoModelForSemanticSegmentation

# Carga del modelo de segmentación (solo se ejecuta una vez al importar)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(_file_)))
model_path = os.path.join(BASE_DIR, "models", "Palpebral_Segmentation_Augmented")
#model_path = "models/Palpebral_Segmentation_Augmented"  - COMENTADA POR UNA NUEVA LÍNEA
processor = AutoImageProcessor.from_pretrained(model_path)
segmentador = AutoModelForSemanticSegmentation.from_pretrained(model_path)

def obtener_mascara(img_rgb: np.ndarray) -> np.ndarray:
    """Genera una máscara binaria de la región conjuntival."""
    inputs = processor(images=img_rgb, return_tensors="pt")
    with torch.no_grad():
        logits = segmentador(**inputs).logits
    H, W = img_rgb.shape[:2]
    logits = F.interpolate(logits, size=(H, W), mode="bilinear", align_corners=False)
    mask = (logits.argmax(dim=1).squeeze().cpu().numpy() == 1).astype(np.uint8)
    return mask

def aplicar_mascara(img_rgb: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Aplica la máscara sobre la imagen original."""
    if mask.shape != img_rgb.shape[:2]:
        mask = cv2.resize(mask, (img_rgb.shape[1], img_rgb.shape[0]), interpolation=cv2.INTER_NEAREST)
    mask_uint8 = (mask * 255).astype(np.uint8)
    return cv2.bitwise_and(img_rgb, img_rgb, mask=mask_uint8)

def validar_segmentacion(mask: np.ndarray, umbral=0.0085) -> bool:
    """Verifica si la segmentación cubre área suficiente."""
    proporcion = np.mean(mask > 0)
    return proporcion >= umbral
