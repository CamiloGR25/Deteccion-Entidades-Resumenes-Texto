from flask import Flask, request, render_template
from bp_main import bp_main
import nltk
import gensim
from gensim import corpora
import spacy

# Cargar el modelo en español
nlp = spacy.load("es_core_news_md")



@bp_main.route('/')
def index():
    return render_template('index.html')

@bp_main.route("/extraer_entidades", methods=["POST"])
def extraer_entidades():
    # Obtener el texto del formulario
    texto = request.form.get("texto", "")

    # Procesar el texto con spaCy
    doc = nlp(texto)

    # Extraer entidades y almacenarlas en una lista de diccionarios
    entidades = [{"texto": entidad.text, "tipo": entidad.label_} for entidad in doc.ents]
    
    # Renderizar la plantilla con las entidades extraídas
    return render_template('index.html', entidades=entidades)