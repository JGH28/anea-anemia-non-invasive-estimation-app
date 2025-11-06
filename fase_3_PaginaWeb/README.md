# Universidad de Guadalajara

## Centro Universitario de Ciencias Exactas e Ingenierías

### Ingeniería Biomédica

### Proyecto Modular:  
### ANEA: Anemia Non-Invasive Estimation App

### Asesor: Dr. Omar Paredes

### Co-Asesor: Mtro. Moisés Sotelo Rodríguez

### Integrantes del equipo:  

* Sael Cardona Noriega  
* José de Jesús González Hernández  
* Marisol Elizabeth Huerta Lucio  

---

## Fase 3 – Desarrollo e Implementación Web de ANEA  

Esta fase corresponde al desarrollo de la **interfaz web y servicio backend** del sistema ANEA, que integra los modelos de segmentación y estimación desarrollados en las fases anteriores.  

El objetivo de esta etapa fue implementar el flujo completo de análisis de anemia mediante un servicio accesible desde navegador, permitiendo al usuario **subir una fotografía del ojo**, ejecutar el análisis con modelos locales y obtener la estimación de hemoglobina de forma automática.  

---

### Contexto del proyecto  

Tras la integración de ambos modelos (Fase 2), se diseñó una aplicación web funcional utilizando **Flask** como backend principal, alojado en **Replit** para su despliegue y pruebas iniciales.  

El servicio está estructurado para recibir una imagen codificada en **base64**, procesarla localmente con los modelos **SegFormer** y **Xception**, y devolver un resultado interpretado en formato JSON, incluyendo:  

- Valor estimado de hemoglobina (g/dL).  
- Clasificación clínica (Normal, Anemia leve, moderada o grave).  
- Nivel de riesgo y color de referencia.  

El sistema fue diseñado bajo una arquitectura modular, separando la lógica de **segmentación**, **estimación**, **interpretación** y **ruteo** en diferentes scripts dentro del servicio Python.  

---

## Estructura del proyecto  

La estructura final del backend se encuentra en la carpeta `Root_EstructuraProyecto/`, organizada de la siguiente forma:  

```
fase_3_PaginaWeb/
│
├── README.md                      # Descripción del sistema web
├── requirements.txt               # Dependencias del servicio (idénticas a Fase 2)
│
└── Root_EstructuraProyecto/
    │
    ├── app.py                     # Servidor Flask principal
    │
    ├── utils/                     # Carpeta con los módulos de IA
    │   ├── __init__.py            # Inicializador del paquete
    │   ├── segmentation.py        # Segmentación (modelo SegFormer)
    │   ├── estimation.py          # Estimación (modelo Xception)
    │   └── interpretation.py      # Clasificación clínica
    │
    ├── models/                    # Carpeta de modelos de IA
    │   ├── best_xception_model.h5                   # Estimación de hemoglobina (NO subir a GitHub)
    │   └── Palpebral_Segmentation_Augmented/        # Segmentación de conjuntiva
    │       ├── config.json
    │       ├── preprocessor_config.json
    │       └── model.safetensors                    # (NO subir a GitHub)
    │
    └── data/                      # Carpeta temporal de imágenes (autogenerada)
```

> **Nota:** los modelos pesados (`.h5` y `.safetensors`) no se incluyen en el repositorio.  
> Solo deben colocarse localmente dentro de la carpeta `models/` antes de ejecutar el servicio.  

---

## Descripción general del sistema  

### 1. Recepción de imagen (`app.py`)  
El endpoint `/analyze` recibe una imagen en formato base64 junto con los datos opcionales de **sexo** y **edad** del usuario.  

### 2. Decodificación y preprocesamiento  
La imagen se decodifica y se guarda temporalmente en la carpeta `data/`.  

### 3. Segmentación  
Se aplica el modelo **SegFormer**, que genera una máscara binaria y extrae automáticamente la región de la conjuntiva palpebral.  

### 4. Estimación  
La región segmentada se redimensiona a 224×224 píxeles y se pasa al modelo **Xception**, que estima el valor de hemoglobina (en g/dL).  

### 5. Validación  
Se evalúa si el área segmentada es suficiente mediante la función `validar_segmentacion()`. Si no lo es, se devuelve un mensaje de error indicando que la imagen no es válida.  

### 6. Interpretación  
La función `interpretar_resultado()` clasifica el valor estimado según los umbrales de la OMS, devolviendo el estado clínico y color asociado.  

### 7. Respuesta JSON  
El servicio responde con un JSON que incluye:  

- Valor estimado de hemoglobina.  
- Nivel de riesgo (muy bajo, bajo, medio, alto).  
- Interpretación textual del estado.  

---

## Instalación  

### Requisitos  

* Python ≥ 3.10  
* Entorno **local** (Replit, VSCode o Conda recomendado).  
* Las dependencias se especifican en `requirements.txt`.  

### Instalación rápida  

```bash
pip install -r requirements.txt
```

> Se recomienda **ejecutar el proyecto en entorno local**, ya que en Replit o Colab pueden presentarse conflictos de dependencias (particularmente entre PyTorch, TensorFlow y Transformers).  

---

## Ejecución  

1. Asegúrate de que las rutas de los modelos sean correctas en los scripts:  
   ```
   models/best_xception_model.h5  
   models/Palpebral_Segmentation_Augmented/
   ```  

2. Ejecuta el servidor Flask con:  

```bash
python app.py
```

3. El servidor iniciará en el puerto **5001** y escuchará solicitudes POST en la ruta:  

```
http://localhost:5001/analyze
```

4. Envía una solicitud POST con un JSON de este tipo:  

```json
{
  "imageBase64": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABA...",
  "sexo": "Hombre",
  "edad": 23
}
```

5. El servicio devolverá una respuesta JSON como esta:  

```json
{
  "hemoglobinEstimate": 13.8,
  "riskLevel": "bajo",
  "estado": "Anemia leve",
  "color": "yellow",
  "aiAnalysis": "Análisis basado en segmentación de conjuntiva palpebral..."
}
```

---

## Notas adicionales  

* El modelo de segmentación **SegFormer** fue entrenado en la Fase 1 y exportado a la carpeta `models/Palpebral_Segmentation_Augmented/`.  
* El modelo de estimación **Xception** fue tomado del proyecto [Eyes Defy Anemia](https://www.kaggle.com/code/rodinayasser/eyes-defy-animea/output) y adaptado a nuestro pipeline.  
* El pipeline de Flask combina ambos modelos para generar una respuesta interpretada en tiempo real.  
* Las imágenes cargadas por el usuario **no se almacenan de manera permanente**; se eliminan tras su procesamiento.  

---

## Perspectivas del proyecto  

Esta fase constituye la **implementación funcional del sistema ANEA**, integrando el backend con los modelos de inteligencia artificial.  

Las siguientes etapas contemplan:  
- **Optimización de rendimiento y latencia** para su uso en dispositivos móviles.  
- **Despliegue del servicio en la nube** (Render, AWS o Hugging Face Spaces).  
- **Validación clínica (Fase 4)** con pacientes mexicanos, comparando los valores estimados con resultados de laboratorio y analizando su precisión estadística.  

---

> Proyecto en desarrollo. Esta fase completa la integración práctica del sistema y sienta las bases para su despliegue clínico y validación final.

