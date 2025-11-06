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
## Fase 1 - Segmentación Automática de la Conjuntiva Palpebral para la Estimación No-Invasiva de Anemia

 Esta fase se enfoca exclusivamente en la tarea de segmentación semántica de la región ocular de interés.

---

### Elección de Transformers y Hugging Face

Para esta tarea se optó por utilizar un modelo preentrenado de segmentación disponible en la plataforma [Hugging Face](https://huggingface.co/) debido a sus ventajas en cuanto a:

* Facilidad de integración en entornos Python/Colab.
* Rendimiento superior al de modelos tradicionales como U-Net, especialmente con pocas épocas de entrenamiento.
* Arquitectura basada en transformers, que han demostrado gran eficacia en tareas de visión por computadora.

Se utilizó en particular el modelo [nvidia/segformer-b0-finetuned-ade-512-512](https://huggingface.co/nvidia/segformer-b0-finetuned-ade-512-512), originalmente entrenado para segmentar 150 clases, pero se adaptó para nuestro caso reduciéndolo a solo 2 clases: **conjuntiva palpebral** y **fondo**.

---

### ¿Qué es un modelo de segmentación semántica?

La segmentación semántica es una tarea de visión por computadora en la que se clasifica cada píxel de una imagen de acuerdo a la clase a la que pertenece. En este proyecto, nos interesa clasificar los píxeles que pertenecen a la conjuntiva palpebral vs. los que no, generando máscaras binarias.

---

## Estructura de la Fase 1 del Proyecto

1. **Recolección de Datos:** Se utilizó el dataset público "Eyes Defy Anemia" con imágenes de ojos y sus respectivas máscaras de segmentación.
2. **Preprocesamiento:** Agrupación de todas las imágenes y sus máscaras en carpetas separadas, conversión a escala de grises y redimensionamiento a 512x512.
3. **Entrenamiento Inicial:** Se entrenó el modelo SegFormer desde un checkpoint preentrenado.
4. **Evaluación:** Se observaron resultados prometedores, pero se identificó un posible bajo rendimiento al probar con imágenes externas (no incluidas en el entrenamiento).
5. **Recolección de Imágenes Nuevas:** Se capturaron 15 nuevas imágenes propias (equipo, amigos y familiares) que fueron etiquetadas manualmente en MakeSense.ai.
6. **Fine-Tuning:** Se reutilizó el modelo previamente entrenado y se le realizó un reentrenamiento incluyendo las nuevas imágenes.
7. **Validación Visual:** Se iteró con imágenes nuevas externas y se observó una mejora considerable en la segmentación.
8. **Guardado del Modelo Final:** Se almacenó el modelo ajustado en Google Drive para futuras integraciones.

---

## Instalación

### Requisitos

* Python >= 3.8
* Google Colab (recomendado)
* GPU (ideal, pero también corre en CPU)
* Librerías:

  * transformers
  * datasets
  * torch
  * torchvision
  * numpy
  * matplotlib
  * PIL
  * pycocotools

### Instalación sugerida con Conda (opcional)

```bash
conda create -n segformer_env python=3.10
conda activate segformer_env
pip install transformers datasets torch torchvision matplotlib pillow pycocotools
```

---

## Uso

Puedes ejecutar el archivo `.ipynb` en Google Colab para:

* Entrenar desde cero o continuar desde un checkpoint.
* Probar con nuevas imágenes cargadas desde tu Google Drive.
* Guardar el modelo en Drive para integrarlo en otras plataformas.

---

## Notas importantes

* El archivo `.ipynb` contiene markdowns explicativos por celda.
* No se incluyen las imágenes originales del dataset ni las imágenes nuevas tomadas por el equipo debido a restricciones de uso.
* Si deseas replicar el trabajo, deberás capturar tus propias imágenes y generar sus respectivas máscaras con herramientas como [MakeSense.ai](https://www.makesense.ai/).

---

## Explicación Adicional

* Dataset base: **"Eyes Defy Anemia"** (imágenes de ojos con segmentaciones de conjuntiva palpebral).
* Herramienta de etiquetado: **[MakeSense.ai](https://www.makesense.ai/)**
* Modelo usado: **[nvidia/segformer-b0-finetuned-ade-512-512](https://huggingface.co/nvidia/segformer-b0-finetuned-ade-512-512)**
* Frameworks: **Transformers (Hugging Face)** y **PyTorch**.

---

## Perspectivas del Proyecto

Debido a limitaciones de tiempo y recursos computacionales, esta fase se centró exclusivamente en la segmentación palpebral. Las siguientes fases se trabajarán en paralelo:

* **Fase 2: Integración de modelos**, donde el modelo de segmentación se enlazará con el modelo de estimación de hemoglobina (best_xcpetion_model.h5) para obtener valores de hemoglobina a partir de la región segmentada.

* **Fase 3: Desarrollo de la aplicación web**, que permitirá subir fotografías y obtener un análisis automático desde cualquier dispositivo.

* **Fase 4: Validación con pacientes mexicanos**, contemplando niveles reales de hemoglobina bajo condiciones clínicas controladas. Esta etapa no se ejecutó por limitaciones de confidencialidad y tiempo, pero constituye la siguiente meta del proyecto.


---

> Proyecto en constante evolución. Seguiremos iterando, mejorando y documentando conforme avanzan las fases.
