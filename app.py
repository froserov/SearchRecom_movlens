import os
import requests
import streamlit as st
import pandas as pd
import numpy as np
from elasticsearch import Elasticsearch
from elasticsearch import helpers

# Elastic Search correrá de forma local
es = Elasticsearch("http://localhost:9200")

# Configuracion de indice
## Se incluye funcionalidad básica de sinónimos en el indice movies
index_name = "movies"
index_config = {
    "settings": {
        "analysis": {
            "analyzer": {
                "synonym_analyzer": {
                    "tokenizer": "standard",
                    "filter": ["lowercase", "synonym_filter"]
                }
            },
            "filter": {
                "synonym_filter": {
                    "type": "synonym",
                    "synonyms": [
                        "sci-fi, science fiction",
                        "thriller, suspense",
                        "animation, cartoon",
                        "drama, tragedy"
                    ]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "title": {"type": "text", "analyzer": "synonym_analyzer"},
            "genres": {"type": "text", "analyzer": "synonym_analyzer"},
            "avg_rating": {"type": "float"}
        }
    }
}

# Crear el índice si no existe
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body=index_config)

# Cargar de datos preprocesados ( para no realizar reproceso cada que consultemos en la app)
movies = pd.read_parquet("data/processed/movies_processed.parquet")
adjusted_sim = np.load("data/processed/adjusted_sim.npy")

# Cargar datos a Elasticsearch 

bulk_data = []
for movie in movies.to_dict(orient="records"):
    bulk_data.append({
        "_index": index_name,
        "_id": movie["movieId"],
        "_source": {
            "title": movie["title"],
            "genres": movie["genres"],
            "avg_rating": movie["avg_rating"]
        }
    })

helpers.bulk(es, bulk_data)

# Función para realizar búsqueda en Elasticsearch con Boosting y permitiendo errores ortográficos
@st.cache_data
def search_movies(query):
    search_body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": [
                    "title^3",  # Más peso en títulos
                    "genres^1"  # Menos peso en géneros
                ],
                "fuzziness": "AUTO"  # Permite errores tipográficos
            }
        }
    }
    res = es.search(index=index_name, body=search_body)
    return [hit["_source"]["title"] for hit in res["hits"]["hits"]]

# Crear índice de títulos
indices = pd.Series(movies.index, index=movies["title"]).drop_duplicates()

# Función para obtener recomendaciones por contenido 

@st.cache_data
def get_recommendations(title):
    if title in indices:
        idx = indices[title]
        sim_scores = list(enumerate(adjusted_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:6]
        movie_indices = [i[0] for i in sim_scores]
        recommended_movies = movies.iloc[movie_indices][["title", "tmdbId", "avg_rating", "genres"]]
        
        # Ordenar por rating en orden descendente y tomar el top 3
        recommended_movies = recommended_movies.sort_values(by="avg_rating", ascending=False).head(3)
        return recommended_movies.values.tolist()
    else:
        return []



# Interfaz de la app en Streamlit

st.set_page_config(page_title="🎬 Buscador y Recomendador de Películas", layout="wide")
st.title("🎬 Buscador y Recomendador de Películas")
st.write("Encuentra películas y obtén recomendaciones basadas en contenido y ratings.")

col1, col2 = st.columns([2, 3])

with col1:
    st.subheader("🔍 Busca una película")
    search_query = st.text_input("Escribe el nombre de una película:")
    filtered_movies = search_movies(query=search_query) if search_query else []
    selected_movie = st.selectbox("Selecciona una película:", filtered_movies) if filtered_movies else None

with col2:
    if selected_movie:
        st.subheader(f"🔹 Recomendaciones para: {selected_movie}")
        recommendations = get_recommendations(selected_movie)

        for rec_title, tmdb_id, avg_rating, genres in recommendations:
            st.markdown(f"### 🎬 {rec_title}")
            st.markdown(f"⭐ Rating: {avg_rating:.1f}")
            st.markdown(f"🎭 Géneros: {genres}")
