from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import base64
import numpy as np
import cv2
from pathlib import Path

# Agregar python-service al path para importar utils
sys.path.insert(0, os.path.join(os.path.dirname(_file_), 'python-service'))

from utils.estimation import estimar_hemoglobina
from utils.interpretation import interpretar_resultado
from utils.segmentation import validar_segmentacion

app = Flask(_name_)
CORS(app)

@app.route("/health", methods=["GET"])
def health():
    """Endpoint de salud para verificar que el servicio está funcionando."""
    return jsonify({"status": "healthy", "service": "ANEA ML Service"}), 200

@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Endpoint principal para análisis de anemia.
    Recibe una imagen en base64 y devuelve el resultado del análisis.
    """
    try:
        data = request.get_json()
        
        if not data or 'imageBase64' not in data:
            return jsonify({"error": "No se proporcionó imagen en base64"}), 400
        
        # Decodificar imagen base64
        image_base64 = data['imageBase64']
        
        # Limpiar cualquier prefijo de data URL si existe
        if ',' in image_base64:
            image_base64 = image_base64.split(',')[1]
        
        try:
            image_bytes = base64.b64decode(image_base64)
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        except Exception as decode_error:
            print(f"Error decodificando imagen: {str(decode_error)}")
            return jsonify({
                "error": "Error al decodificar imagen base64",
                "details": str(decode_error)
            }), 400
        
        if img is None:
            print(f"Imagen decodificada es None. Tamaño de bytes: {len(image_bytes) if image_bytes else 0}")
            return jsonify({"error": "No se pudo decodificar la imagen"}), 400
        
        # Guardar temporalmente para procesamiento
        os.makedirs("data", exist_ok=True)
        temp_path = os.path.join("data", "temp_image.jpg")
        cv2.imwrite(temp_path, img)
        
        # Ejecutar pipeline de análisis
        resultado = estimar_hemoglobina(temp_path)
        
        # Validar segmentación
        if not validar_segmentacion(resultado["mask"]):
            return jsonify({
                "error": "INVALID_SEGMENTATION",
                "message": "Segmentación insuficiente. La conjuntiva no es claramente visible. Por favor, vuelve a capturar la imagen siguiendo las instrucciones."
            }), 400
        
        # Interpretar resultado (usar valores del request si están disponibles)
        sexo = data.get('sexo', 'Hombre')
        edad = data.get('edad', None)
        estado, color, valor_ajustado = interpretar_resultado(
            resultado["valor"], 
            sexo=sexo, 
            edad=edad
        )
        
        # Mapear interpretación a niveles de riesgo de la app
        risk_mapping = {
            "Normal": "muy bajo",
            "Anemia leve": "bajo",
            "Anemia moderada": "medio",
            "Anemia grave": "alto",
            "Medición no válida": "error"
        }
        
        risk_level = risk_mapping.get(estado, "medio")
        
        # Limpiar archivo temporal
        try:
            os.remove(temp_path)
        except:
            pass
        
        return jsonify({
            "hemoglobinEstimate": round(valor_ajustado, 2),
            "riskLevel": risk_level,
            "aiAnalysis": f"Análisis basado en segmentación de conjuntiva palpebral. Estado: {estado}. Hemoglobina estimada: {round(valor_ajustado, 2)} g/dL. Este análisis utiliza modelos de aprendizaje profundo entrenados específicamente para la población mexicana.",
            "rawValue": round(resultado["valor"], 2),
            "adjustedValue": round(valor_ajustado, 2),
            "estado": estado,
            "color": color
        }), 200
        
    except Exception as e:
        print(f"Error en análisis: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "error": "ANALYSIS_ERROR",
            "message": f"Error durante el análisis: {str(e)}"
        }), 500

if _name_ == "_main_":
    import subprocess
    import threading
    import time
    
    print("=" * 60)
    print("🚀 INICIANDO ANEA - Sistema de Detección de Anemia")
    print("=" * 60)
    
    # Verificar que los modelos existen (ahora en python-service/models)
    print("\n📊 Verificando modelos de IA...")
    model_h5 = Path("python-service/models/best_xception_model.h5")
    model_seg = Path("python-service/models/Palpebral_Segmentation_Augmented")
    
    if not model_h5.exists():
        print(f"⚠  ADVERTENCIA: No se encontró el modelo {model_h5}")
    else:
        print(f"✅ Modelo de hemoglobina encontrado")
    
    if not model_seg.exists():
        print(f"⚠  ADVERTENCIA: No se encontró el modelo {model_seg}")
    else:
        print(f"✅ Modelo de segmentación encontrado")
    
    # Función para ejecutar el servidor Express en paralelo
    def run_express_server():
        time.sleep(3)  # Esperar a que Flask se inicie primero
        print("\n⚡ Iniciando servidor Express + Frontend (puerto 5000)...")
        try:
            subprocess.run(["npm", "run", "dev"], check=False)
        except Exception as e:
            print(f"⚠  Error al iniciar Express: {e}")
    
    # Iniciar Express en un thread separado
    express_thread = threading.Thread(target=run_express_server, daemon=True)
    express_thread.start()
    
    # Iniciar Flask ML Service en el thread principal
    print("\n🐍 Iniciando servicio Flask ML (puerto 5001)...")
    print("✨ Ambos servicios se están iniciando...")
    print("=" * 60)
    print("\n📝 Logs del servicio:\n")
    
    app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=False)