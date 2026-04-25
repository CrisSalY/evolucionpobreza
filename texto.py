import os
import re
import nltk
from PyPDF2 import PdfReader

from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords
def leer_pdfs(ruta_pdfs):
    textos = []
    
    for archivo in os.listdir(ruta_pdfs):
        if archivo.lower().endswith(".pdf"):
            ruta = os.path.join(ruta_pdfs, archivo)
            lector = PdfReader(ruta)
            
            texto_pdf = ""
            for pagina in lector.pages:
                texto_pdf += pagina.extract_text() + " "
            
            textos.append(texto_pdf)
    
    return textos
ruta_pdfs = "./files"
textos_lista = leer_pdfs(ruta_pdfs)
 
corpus = " ".join(textos_lista) 
def eliminar_emoticonos(texto):
    patron_emoji = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE
    )
    return patron_emoji.sub("", texto)
corpus = corpus.lower()
corpus = eliminar_emoticonos(corpus)

tokens = word_tokenize(corpus, language="spanish")
 
tokens = [t for t in tokens if t.isalpha()]
 
stopwords_es = stopwords.words("spanish")
tokens = [t for t in tokens if t not in stopwords_es]
 
tokens = [t for t in tokens if not re.search(r'(https?|www)', t)]
tokens = [t for t in tokens if not re.search(r'(.)\1{2,}', t)]
 
pos = pos_tag(tokens) 
with open("./files/corpus_institucional_pobreza_empleo.txt", "w", encoding="utf-8") as f:
    f.write(" ".join(tokens))