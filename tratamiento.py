import pandas as pd
import os
import numpy as np

#---------------------------------------------------------------------------------

def extraer_anio(periodo):
    # Caso 1: formato tipo 201912.0
    if periodo[:4].isdigit():
        return int(periodo[:4])
    
    # Caso 2: formato tipo dic-20, dic-21, mar-26
    if "-" in periodo:
        try:
            anio_2d = int(periodo.split("-")[1])
            return 2000 + anio_2d
        except:
            return np.nan
    
    return np.nan

#---------------------------------------------------------------------------------
ipc_dic = {
    2019: 105.90,
    2020: 104.97,
    2021: 106.94,
    2022: 110.95,
    2023: 112.50,
    2024: 113.10,
    2025: 115.26
}
#---------------------------------------------------------------------------------

df=pd.read_csv('./basesdedatos/ENEMDU_2019_2026.csv', encoding="utf-8",low_memory=False)

#### limpieza de variables ####

# tipo de dato
df["periodo"] = df["periodo"].astype(str).str.lower().str.strip()
df["periodo"] = df["periodo"].apply(extraer_anio)

df["ingrl"] = pd.to_numeric(df["ingrl"], errors="coerce").fillna(0)
df["ingpc"] = pd.to_numeric(df["ingpc"], errors="coerce").fillna(0)

df["p03"]=pd.to_numeric(df["p03"], errors="coerce")
df=df[df['p03'].notna()]
df['p03']=df['p03'].astype(int)

df['p10a']=df['p10a'].fillna('Ninguno').str.strip().str.upper()
df['p06']=df['p06'].fillna('Soltero(a)').str.strip().str.upper()
df["p04"]=df['p04'].str.strip().str.upper()
# Extraer etnia del jefe/a de hogar y rellenar con esa etnia la etnia de los niños

df["p15"] = df["p15"].fillna('Menor de 5 años').str.strip().str.upper()
df['p15']=df['p15'].str.replace('MONTUVIO','MONTUBIO').str.replace('OTRO','OTRA').str.replace('OTRA, CUAL','OTRA')

df['nnivins']=df['nnivins'].fillna('Ninguno').str.strip().str.upper()
df['secemp']=df['secemp'].fillna('Sin empleo').str.strip().str.upper()
df['grupo1']=df['grupo1'].fillna('Sin empleo').str.strip().str.upper()
df['grupo1']=df['grupo1'].str.replace('CIENT?FICOS','CIENTÍFICOS').str.replace('M?QUINAS','MÁQUINAS').str.replace('P?BLICA','PÚBLICA').str.replace('T?CNICOS','TÉCNICOS')

df['rama1']=df['rama1'].fillna('Z').str.strip().str.upper()
dic_ramas={
'A': 'AGRICULTURA, GANADERIA CAZA Y SILVICULTURA Y PESCA',
'G':'COMERCIO, REPARACION VEHICULOS',
'C': 'INDUSTRIAS MANUFACTURERAS',    
'I': 'ACTS DE ALOJAMIENTO Y SERVICIOS DE COMIDA'        ,
'H': 'TRANSPORTE Y ALMACENAMIENTO',                                  
'F': 'CONSTRUCCION',                                            
'P': 'ENSEÑANZA'     ,                                              
'Q': 'ACTS, SERVICIOS SOCIALES Y DE SALUD'   ,               
'O': 'ADMINISTRACION PUBLICA, DEFENSA Y SEGURIDAD SOCIAL',
'N': 'ACTS Y SERVICIOS ADMINISTRATIVOS Y DE APOYO',
'S': 'OTRAS ACTS DE SERVICIOS',
'T': 'ACTS EN HOGARES PRIVADOS CON SERVICIO DOMESTICO',
'M':'ACTS PROFESIONALES, CIENTIFICAS Y TECNICAS',          
'K': 'ACTS FINANCIERAS Y DE SEGUROS',
'B': 'EXPLOTACION DE MINAS Y CANTERAS'     ,                       
'R': 'ARTES, ENTRETENIMIENTO Y RECREACION'                        ,
'D': 'SUMINISTROS DE ELECTRICIDAD, GAS, AIRE ACONDICIONADO'      ,    
'L':'ACTS INMOBILIARIAS',                                     
'J': 'INFORMACION Y COMUNICACION',                                   
'E': 'DISTRIBUCION DE AGUA, ALCANTARILLADO',                           
'U':  'ACTS DE ORGANIZACIONES EXTRATERRITORIALES',
'Z':'SIN EMPLEO'               
}
df['rama1']=df['rama1'].str[0].map(dic_ramas).str.strip().str.upper()
df=df[df['pobreza'].notna()]
df['area']=df['area'].str.strip().str.upper()
df['p02']=df['p02'].str.strip().str.upper()

# corregir el ingreso por IPC para que sea comparable entre años

# Asignar IPC según el año
df["ipc"] = df["periodo"].map(ipc_dic)

# Corregir (deflactar) ingresos por IPC
df["ingrl"] = df["ingrl"] / df["ipc"]
df["ingpc"] = df["ingpc"] / df["ipc"]

#codificacion de variables 
df["pobreza"]=df["pobreza"].apply(lambda x: 1 if x=='POBRE' else 0)
df["epobreza"]=df["epobreza"].apply(lambda x: 1 if x=='INDIGENTE' else 0)
print('----------------------------------------')
print(df.info())
print(df.describe().T) 
print('----------------------------------------')
df.to_csv('./basesdedatos/ENEMDU_2019-2025_CLEAN.csv',index=False,    encoding="utf-8")
print('base de datos limpiada')
print(df['p02'].value_counts())