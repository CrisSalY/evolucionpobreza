import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
import seaborn as sns
import os
# Ruta donde están los .sav
ruta_archivos = "./basesdedatos/*.sav"
# Lista de archivos SPSS
archivos = glob.glob(ruta_archivos)
dfs = []
for archivo in archivos:
    df = pd.read_spss(archivo)
    dfs.append(df)
enemdu_consolidado = pd.concat(dfs, ignore_index=True)

vars_usar = [

    # Tiempo
    "periodo",

    # Identificadores
    "id_vivienda",
    "id_hogar",
    "id_persona",

    # Diseño muestral
    "fexp",
    "upm",
    "estrato",

    # Demografía
    "p02",        # Sexo
    "p03",        # Edad
    "p10a",       # Nivel de instruccion
    "p06",        # Estado civil
    "p15",        # Etnia
    "area",       # Área urbano/rural
    "p04" ,        # jefe de hogar
    'ciudad',

    # Educación
    "nnivins",    # Nivel de instrucción

    # Mercado laboral
    "condact", 
    "secemp",
    "grupo1",
    "rama1",

    # Ingresos oficiales INEC
    "ingrl",
    "ingpc",

    # Pobreza oficial INEC
    "pobreza",
    "epobreza"
]

enemdu_consolidado=enemdu_consolidado[vars_usar]
print('----------------------------------------')
print(enemdu_consolidado.info())
print(enemdu_consolidado.describe().T)
print('----------------------------------------')
enemdu_consolidado.to_csv('./basesdedatos/ENEMDU_2019_2026.csv',index=False,    encoding="utf-8")
print('base de datos guardada')