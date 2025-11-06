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

## Fase 2 - Integración de ambos modelos  

Esta fase corresponde a la integración funcional entre el modelo de **segmentación palpebral** (SegFormer) y el modelo de **estimación de hemoglobina** (Xception).  
El objetivo es unir ambas etapas en un solo pipeline que permita realizar la **estimación no invasiva de hemoglobina (Hb)** a partir de una única fotografía del ojo humano.  

---

### Contexto del proyecto  

Durante la **Fase 1** se desarrolló un modelo de segmentación semántica basado en **Transformers (SegFormer)**, capaz de identificar la conjuntiva palpebral.  
En esta **Fase 2** se integró dicho modelo con una red **Xception** previamente entrenada para estimar la concentración de hemoglobina (en g/dL) utilizando las regiones segmentadas.  
Este modelo base fue tomado del proyecto **“Eyes Defy Anemia”**, desarrollado por *Rodina Yasser* y disponible públicamente en [Kaggle](https://www.kaggle.com/code/rodinayasser/eyes-defy-animea/output).  
Dicho modelo fue adaptado para su integración dentro de nuestro pipeline de segmentación y estimación de hemoglobina, manteniendo su arquitectura original pero aplicándolo a la región conjuntival generada por el modelo SegFormer entrenado en la Fase 1.


Esta integración automatiza el proceso completo:  
1. Segmentación de la conjuntiva palpebral.  
2. Extracción automática de la región de interés (ROI).  
3. Predicción del valor de hemoglobina mediante el modelo Xception.  

El pipeline fue diseñado para ejecutarse preferentemente en **entornos locales**, ya que en **Google Colab** pueden presentarse conflictos de dependencias y versiones entre TensorFlow, PyTorch y Transformers.  
Por lo tanto, **no se recomienda su ejecución en Colab**, siendo más estable y reproducible en un entorno local con control de versiones.  

---

### Descripción general del pipeline  

1. **Verificación de librerías del entorno:** Se comprobó la compatibilidad entre las versiones de TensorFlow 2.15, PyTorch 2.9 y Transformers 4.57.  
2. **Carga del modelo de segmentación:** Se cargó el modelo `Palpebral_Segmentation_Augmented` entrenado en la Fase 1.  
3. **Generación de máscara:** Se implementó la función `obtener_mascara()` para generar una máscara binaria (0 = fondo, 1 = conjuntiva).  
4. **Aplicación de máscara:** La función `aplicar_mascara()` superpone la máscara sobre la imagen original para aislar la conjuntiva.  
5. **Carga del modelo Xception:** Se cargó el modelo `best_xception_model.h5`, encargado de estimar los valores de hemoglobina.  
6. **Preparación de entrada:** La función `preparar_entrada_xception()` redimensiona y normaliza la región segmentada a 224×224 px.  
7. **Integración:** La función `estimar_hemoglobina()` ejecuta todo el flujo (segmentación → extracción → predicción).  
8. **Prueba del sistema:** Se probó el pipeline con una imagen de ejemplo (`Imagen_Prueba.jpg`) mostrando resultados de máscara, ROI y valor estimado.  
9. **Validación de segmentación:** La función `validar_segmentacion()` evalúa la proporción de píxeles detectados como conjuntiva, garantizando una detección mínima antes de interpretar el resultado.  
10. **Interpretación clínica:** Se desarrolló la función `interpretar_resultado()` que traduce el valor estimado de hemoglobina en categorías clínicas (normal o grados de anemia).  
11. **Evaluación final:** Se integró todo el flujo con parámetros de prueba (sexo y edad), simulando la entrada que recibirá la futura aplicación web.  

---

### Detalles de la interpretación clínica  

La función `interpretar_resultado()` clasifica el valor estimado de hemoglobina según los umbrales definidos por la **Organización Mundial de la Salud (OMS)**.  
Solo se consideran **hombres y mujeres adultas**, ya que el conjunto de datos de entrenamiento del modelo Xception no incluye casos pediátricos ni embarazadas.  

Inicialmente se propuso un **factor de compensación (> 1)** para ajustar la subestimación del modelo frente a valores de laboratorio en población mexicana; sin embargo, en esta versión se fijó el **factor = 1**, conservando los valores originales del modelo.  
La diferencia observada se documenta como una **limitación conocida**, que será abordada en la etapa de validación clínica (Fase 4).  

La función devuelve tres salidas:  
- **estado:** clasificación clínica (ej. “Anemia moderada”)  
- **color:** código visual asociado (verde, amarillo, naranja o rojo)  
- **valor_ajustado:** valor final utilizado para la interpretación (sin compensación adicional).  

---

## Instalación  

### Requisitos  

* Python ≥ 3.10  
* Entorno **local** recomendado (Windows/Linux/MacOS).  
* GPU compatible (opcional, pero recomendada).  
* Librerías necesarias:  

  * torch  
  * torchvision  
  * tensorflow  
  * keras  
  * transformers  
  * numpy  
  * matplotlib  
  * opencv-python  
  * pycocotools  

### Instalación sugerida con Conda  

```bash
conda create -n anea_env python=3.10
conda activate anea_env
pip install torch torchvision tensorflow keras transformers numpy matplotlib opencv-python pycocotools
```

---

## Uso  

El archivo `.ipynb` puede ejecutarse en un entorno **local** para:  

* Cargar los modelos previamente entrenados.  
* Ejecutar la segmentación automática y la estimación de hemoglobina en una sola instrucción.  
* Visualizar los resultados (imagen original, máscara binaria y región segmentada).  
* Obtener la clasificación clínica y el valor estimado de hemoglobina.  

---

## Notas importantes  

* Este notebook integra ambos modelos de forma modular, permitiendo reutilizar cada componente de manera independiente.  
* Los modelos preentrenados no se incluyen en el repositorio debido a su tamaño; pueden almacenarse en la carpeta `../models/`.  
* Las pruebas se realizaron con imágenes propias de los integrantes del equipo.  
* La versión web del sistema solicitará al usuario ingresar su sexo y edad antes de realizar la predicción.  

---

## Explicación adicional  

* Modelo de segmentación: **SegFormer (Hugging Face)** 
* Modelo de estimación: **Xception (Keras/TensorFlow)**, modelo base tomado del proyecto **“Eyes Defy Anemia”**  [Kaggle](https://www.kaggle.com/code/rodinayasser/eyes-defy-animea/output)
* Formato de entrada: imágenes RGB (224×224 px)  
* Formato de salida: valor numérico (g/dL) o probabilidad de anemia  
* Lenguajes y frameworks: **Python, PyTorch, TensorFlow, Transformers**  

---

## Perspectivas del proyecto  

Esta fase representa el núcleo funcional del sistema **ANEA**. Las siguientes etapas del proyecto comprenden:  

* **Fase 3: Desarrollo de la interfaz web**, que permitirá a los usuarios subir una fotografía del ojo y obtener un resultado de hemoglobina estimada en tiempo real.  
* **Fase 4: Validación clínica con pacientes mexicanos**, comparando los valores estimados por el modelo con mediciones de laboratorio.  
  Esta etapa implicará el análisis estadístico de dispersión y varianza entre ambos métodos, abordando las diferencias observadas en la subestimación.  

---

> Proyecto en constante desarrollo. La presente fase consolida la unión de los modelos y sienta las bases para su despliegue y validación futura.
