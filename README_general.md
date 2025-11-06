# Universidad de Guadalajara

## Centro Universitario de Ciencias Exactas e Ingenierías

### Ingeniería Biomédica

### Proyecto Modular: 
### ANEA: Anemia Non-Invasive Estimation App

### Asesor: Dr. Omar Paredes

### Co-Asesor: Mtro. Moisés Sotelo Rodríguez

### Integrantes del equipo:

* Sael Cardona Noriega - sael.cardona2597@alumnos.udg.mx
* José de Jesús González Hernández - jose.gonzalez0672@alumnos.udg.mx
* Marisol Elizabeth Huerta Lucio - marisol.huerta4198@alumnos.udg.mx
---

## Descripción general del proyecto  

**ANEA (Anemia Non-Invasive Estimation App)** es un sistema basado en **inteligencia artificial** diseñado para estimar los niveles de **hemoglobina (Hb)** de manera **no invasiva**, a partir del análisis de imágenes de la **conjuntiva palpebral**.  

El proyecto combina **modelos de segmentación semántica** y **redes convolucionales** de estimación numérica, integrados en una aplicación web funcional que procesa una fotografía del ojo y devuelve una estimación aproximada del nivel de hemoglobina.  

---

## Objetivo del proyecto  

Desarrollar una herramienta automatizada que:  
1. **Identifique la región de la conjuntiva palpebral** mediante segmentación semántica.  
2. **Estime el nivel de hemoglobina** con base en características visuales del área segmentada.  
3. Permita la **detección temprana de anemia** de forma accesible, no invasiva y rápida.  

---

## Fases del proyecto  

### **Fase 1 – Segmentación de la conjuntiva palpebral**  
- Desarrollo de un modelo basado en **Transformers (SegFormer)** para identificar la región de la conjuntiva palpebral.  
- Entrenamiento con el dataset *Eyes Defy Anemia* (India–Italia) y un conjunto adicional de **15 imágenes propias** segmentadas manualmente con [MakeSense.ai](https://www.makesense.ai/).  
- Implementación de **data augmentation** con transformaciones geométricas y fotométricas para mejorar la generalización del modelo.  
- Resultado: un modelo robusto denominado **`Palpebral_Segmentation_Augmented`**, capaz de segmentar de forma precisa la región ocular de interés.  

📁 Carpeta: [`fase_1_Segmentacion`](./fase_1_Segmentacion/)  

---

### **Fase 2 – Integración de modelos (Segmentación + Estimación)**  
- Integración del modelo **SegFormer** (segmentación) con el modelo **Xception** (estimación de hemoglobina).  
- Automatización del pipeline: segmentación → extracción de ROI → predicción de Hb → interpretación clínica.  
- El modelo Xception fue tomado del proyecto público [Eyes Defy Anemia (Rodina Yasser, Kaggle)](https://www.kaggle.com/code/rodinayasser/eyes-defy-animea/output) y adaptado al sistema ANEA.  
- Implementación de reglas clínicas basadas en los rangos de la **Organización Mundial de la Salud (OMS)** para hombres y mujeres adultas.  

📁 Carpeta: [`fase_2_Integracion`](./fase_2_Integracion/)  

---

### **Fase 3 – Desarrollo e implementación web**  
- Implementación del servicio backend en **Flask**, alojado inicialmente en **Replit**.  
- Creación de una API que recibe imágenes en formato **base64**, ejecuta la segmentación y la predicción de Hb, y devuelve una respuesta **JSON** con el valor estimado y su interpretación clínica.  
- Organización modular del código:  
  - `segmentation.py` → Segmentación palpebral con SegFormer.  
  - `estimation.py` → Estimación de hemoglobina con Xception.  
  - `interpretation.py` → Clasificación clínica del resultado.  
- Integración de ambos modelos dentro del flujo completo del sistema.  

📁 Carpeta: [`fase_3_PaginaWeb`](./fase_3_PaginaWeb/)  

---

## Tecnologías utilizadas  

| Categoría | Tecnologías |
|------------|--------------|
| **Lenguaje principal** | Python 3.10 |
| **Frameworks IA** | PyTorch, TensorFlow, Keras, Hugging Face Transformers |
| **Entrenamiento y pruebas** | Google Colab, entorno local (Conda/VSCode) |
| **Web backend** | Flask |
| **Gestión de datasets** | MakeSense.ai (etiquetado manual), Google Drive |
| **Control de versiones** | Git y GitHub |
| **Entornos adicionales** | Replit (para despliegue y pruebas web) |

---

## Estructura del repositorio  

```
ANEA_anemia-non-invasive-estimation-app/
│
├── fase_1_Segmentacion/              # Entrenamiento del modelo SegFormer
│   ├── Model_Palpebral_Segmentation.ipynb
│   ├── README.md
│   └── requirements.txt
│
├── fase_2_Integracion/               # Pipeline de integración SegFormer + Xception
│   ├── integrated_models_pipeline.ipynb
│   ├── README.md
│   └── requirements.txt
│
├── fase_3_PaginaWeb/                 # Aplicación Flask (backend)
│   ├── Root_EstructuraProyecto/
│   │   ├── app.py
│   │   ├── utils/
│   │   │   ├── segmentation.py
│   │   │   ├── estimation.py
│   │   │   └── interpretation.py
│   │   └── models/
│   │       ├── Palpebral_Segmentation_Augmented/
│   │       └── best_xception_model.h5
│   ├── README.md
│   └── requirements.txt
│
└── README.md                        # Este archivo (descripción general)
```

> **Nota:** Los archivos de modelos (`.h5` y `.safetensors`) no se incluyen por su tamaño y políticas de licencia.  
> Se deben colocar manualmente en la carpeta `models/` antes de ejecutar el sistema.  

---

## Resultados preliminares  

| Tipo de modelo | Dataset | IoU / Dice | Observación |
|----------------|----------|-------------|--------------|
| SegFormer (fine-tuned) | Eyes Defy Anemia + imágenes propias | IoU ≈ 0.46 / Dice ≈ 0.48 | Precisión aceptable en condiciones controladas |
| SegFormer (augmented) | + transformaciones geométricas | IoU ≈ 0.50 / Dice ≈ 0.53 | Mayor robustez ante cambios de iluminación y ángulo |
| Xception (integrado) | Segmentación + estimación | Error ≈ 10% respecto a laboratorio | Subestimación leve, corregible en validación clínica |

---

## Instalación general  

1. Clonar el repositorio:  
   ```bash
   git clone https://github.com/JGH28/ANEA_anemia-non-invasive-estimation-app.git
   cd ANEA_anemia-non-invasive-estimation-app
   ```

2. Crear entorno virtual (opcional pero recomendado):  
   ```bash
   conda create -n anea_env python=3.10
   conda activate anea_env
   ```

3. Instalar dependencias según la fase:  
   ```bash
   pip install -r fase_1_Segmentacion/requirements.txt
   pip install -r fase_2_Integracion/requirements.txt
   pip install -r fase_3_PaginaWeb/requirements.txt
   ```

---

## Perspectivas futuras  

- **Fase 4 (Validación clínica):**  
  Validar los modelos con pacientes mexicanos, comparando los valores estimados por ANEA con mediciones de laboratorio para calcular métricas de error (MAE, RMSE, R²) y analizar la dispersión.  

- **Despliegue:**  
  Implementar la versión final del servicio en la nube (Render, AWS o Hugging Face Spaces).  

- **Optimización móvil:**  
  Adaptar la aplicación para ejecución eficiente en dispositivos móviles o entornos de baja potencia.  

---

> **Proyecto en desarrollo.**  
> ANEA representa una propuesta de diagnóstico biomédico no invasivo, integrando inteligencia artificial, procesamiento de imágenes y diseño de software médico aplicado.
