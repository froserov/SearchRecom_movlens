🎬 Buscador y Recomendador de Películas

Este proyecto implementa un buscador avanzado de películas y un sistema de recomendación por contenido, utilizando 
Elasticsearch para mejorar la eficiencia en la  búsqueda y ofrecer una experiencia más flexible.

📌  Características

✅ Búsqueda avanzada con Elasticsearch
Indexación optimizada de títulos, géneros y ratings.
Soporte para sinónimos en géneros y palabras clave.
Búsqueda con fuzziness para tolerancia a errores tipográficos.

✅ Recomendaciones personalizadas
Sistema de recomendación basado en similitud de contenido (TF-IDF + Cosine Similarity).
Ordenación por rating y filtrado por géneros.
Se muestra el top 3 de películas más similares.

✅ Optimización y eficiencia
Preprocesamiento de datos y almacenamiento optimizado en formato Parquet.
Carga rápida de datos con numpy y consultas eficientes a Elasticsearch.
Arquitectura modular con separación en búsqueda y recomendación.

🚀 Tecnologías Utilizadas

Python 🐍	Lenguaje principal del proyecto.
Streamlit 🎨	Framework para la interfaz web interactiva.
Elasticsearch 🔍	Motor de búsqueda para indexar y consultar películas.
Pandas 📊	Manejo y preprocesamiento de datos.
NumPy 🔢	Cálculo de similitud y almacenamiento eficiente.
Scikit-learn 🏆	Implementación de TF-IDF y similitud de coseno.


📂 Estructura del Proyecto

📦 SearchRecom_movlens
│
├── 📂 data
│   ├── 📂 raw
│   │   ├── ml-latest-small
│   │   │   ├── movies.csv
│   │   │   ├── ratings.csv
│   │   │   ├── tags.csv
│   │   │   ├── links.csv
│   │   │   └── README.txt
│   ├── 📂 processed
│   │   ├── movies_processed.parquet  # Datos preprocesados
│   │   ├── adjusted_sim.npy  # Matriz de similitud
│   │   ├── movies_bulk.json  # Datos para indexación en ES
│   │   └── movies.json  # Datos exportados
│
├── 📂 notebooks
│   ├── Preprocessing.ipynb  # Preprocesamiento de datos
│   ├── Search_ES.ipynb  # Implementación de Elasticsearch
│   ├── Recom.ipynb  # Sistema de recomendación por contenido
│
├── app.py  # Aplicación principal en Streamlit
├── requirements.txt  # Dependencias necesarias
├── README.md  # Documentación del proyecto



📖 Descripción de los Módulos

1️⃣ Preprocessing.ipynb
📌 Funcionalidad:
Procesamiento de los archivos movies.csv, ratings.csv y tags.csv.
Cálculo de similitud entre películas (adjusted_sim.npy).
Guardado de datos preprocesados (movies_processed.parquet).

2️⃣ Search_ES.ipynb
📌 Funcionalidad:
Indexación de películas en Elasticsearch.
Creación de un índice con sinónimos y configuración avanzada.
Función para realizar búsquedas con relevancia mejorada.

3️⃣ Recom.ipynb
📌 Funcionalidad:
Cálculo de recomendaciones con TF-IDF y similitud de coseno.
Selección de películas más similares y ordenadas por rating.
Se genera el top 3 de películas recomendadas.

4️⃣ app.py (Aplicación en Streamlit)
📌 Funcionalidad:
Interfaz interactiva para búsqueda y recomendación.
Integración con Elasticsearch para búsquedas rápidas.
Muestra los resultados con imágenes y detalles.


🔧 Instalación y Uso
1️⃣ Instalar dependencias
pip install -r requirements.txt
2️⃣ Ejecutar Elasticsearch
Asegúrate de tener Elasticsearch corriendo en local antes de usar la app.
Si tienes Docker instalado, puedes ejecutarlo con:
docker run -d -p 9200:9200 -e "discovery.type=single-node" elasticsearch:7.10.2
3️⃣ Ejecutar la aplicación
streamlit run app.py
4️⃣ Acceder a la app



