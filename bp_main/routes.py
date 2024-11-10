from flask import Flask, request, render_template
from bp_main import bp_main
import spacy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import gensim
from gensim import corpora

# Cargar el modelo en español
nlp = spacy.load("es_core_news_md")

def generar_resumen(texto, num_oraciones=2):
    # analizador de sumy para procesar el texto en español
    parser = PlaintextParser.from_string(texto, Tokenizer("spanish"))
    summarizer = LsaSummarizer()
    resumen = summarizer(parser.document, sentences_count=num_oraciones)

    # Convertir el resumen a texto plano
    resumen_texto = " ".join([str(oracion) for oracion in resumen])
    return resumen_texto

@bp_main.route('/')
def index():
    return render_template('index.html')

@bp_main.route("/extraer_entidades", methods=["POST"])
def extraer_entidades():
    # obtener el texto del formulario
    texto = request.form.get("texto", "")

    # procesar el texto con spaCy
    doc = nlp(texto)

    # extraer entidades y almacenarlas en una lista de diccionarios
    entidades = [{"texto": entidad.text, "tipo": entidad.label_} for entidad in doc.ents]
    
    # renderizar la plantilla con las entidades extraidas
    return render_template('index.html', entidades=entidades)

@bp_main.route("/resumir", methods=["POST"])
def resumir():
    # obtener el texto del formulario
    texto = request.form.get("texto", "")

    # generar el resumen
    resumen = generar_resumen(texto)

    # renderizar la plantilla con el resumen
    return render_template('index.html', resumen=resumen)