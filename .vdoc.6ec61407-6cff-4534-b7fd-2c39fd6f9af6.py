# type: ignore
# flake8: noqa
#
#
#
#
#
#
#
#
#
#
#
#
#
#| echo: false
#| warning: false
#| message: false

import pandas as pd
import altair as alt
from PIL import Image
import matplotlib.pyplot as plt 
import json
from collections import defaultdict

alt.data_transformers.disable_max_rows()
df = pd.read_csv("./basesdedatos/ENEMDU_2019-2025_CLEAN.csv")
df["periodo"] = df["periodo"].astype(int)
df["fexp"] = pd.to_numeric(df["fexp"])
```
#
#
#
#
#
#
#
#| echo: false
#| warning: false
#| message: false
pobreza_anual = (
    df
    .assign(
        pobreza_w = df["pobreza"] * df["fexp"],
        epobreza_w = df["epobreza"] * df["fexp"]
    )
    .groupby("periodo", as_index=False)
    .agg(
        pobreza=("pobreza_w", "sum"),
        pobreza_extrema=("epobreza_w", "sum"),
        total=("fexp", "sum")
    )
)
pobreza_anual["pobreza"] = pobreza_anual["pobreza"] / pobreza_anual["total"]
pobreza_anual["pobreza extrema"] = pobreza_anual["pobreza_extrema"] / pobreza_anual["total"]

pobreza_long = pobreza_anual.melt(
    id_vars="periodo",
    value_vars=["pobreza", "pobreza extrema"],
    var_name="tipo",
    value_name="tasa"
)
chart=alt.Chart(pobreza_long, title="Evolución de la pobreza en el Ecuador (2019–2025)").mark_line(point=True).encode(
    x=alt.X("periodo:O", title="Año"),
    y=alt.Y("tasa:Q", title="Tasa de pobreza", axis=alt.Axis(format=".0%")),
    color=alt.Color("tipo:N", title="Indicador"),
    tooltip=["periodo", alt.Tooltip("tasa:Q", format=".1%")]
).properties(
    width='container'
).interactive()
chart 
```
#
#
#
#
#
#
#
#
#
#
#
#
#| echo: false
#| warning: false
#| message: false   

def grafico_pobreza(df, grupo, titulo, nombre_archivo):
    tabla = (
        df
        .assign(pobreza_w=df["pobreza"] * df["fexp"])
        .groupby(grupo, as_index=False)
        .agg(
            pobreza=("pobreza_w", "sum"),
            total=("fexp", "sum")
        )
    )
    tabla["tasa"] = tabla["pobreza"] / tabla["total"]
    if nombre_archivo == "pobreza_edad":
        orden = [
            "0–14", "15–24", "25–34",
            "35–44", "45–54", "55–64",
            "65–74", "75–84", "85+"
        ]
        y_enc = alt.Y(
            f"{grupo}:N",
            sort=orden,
            title="Grupo de edad"
        )
    else:
        y_enc = alt.Y(
            f"{grupo}:N",
            sort="-x",
            title=grupo
        )

    chart = (
        alt.Chart(tabla, title=titulo)
        .mark_bar()
        .encode(
            x=alt.X(
                "tasa:Q",
                title="Tasa de pobreza",
                axis=alt.Axis(format=".0%")
            ),
            y=y_enc,
            tooltip=[
                grupo,
                alt.Tooltip("tasa:Q", format=".1%")
            ]
        )
    )

    return chart

df.rename(columns={'nnivins':'Nivel de instrucción',
'area':'Área de residencia',
'p15':'Etnia',
'p02':'Sexo'},inplace=True)    
```
#
#
#
#| echo: false
#| warning: false
#| message: false   

c=grafico_pobreza(
    df,
    grupo='Área de residencia',
    titulo="Tasa de pobreza por área de residencia",
    nombre_archivo="pobreza_area"
).properties(
    width='container'
).interactive()
c
```
#
#
#
#| echo: false
#| warning: false
#| message: false
c=grafico_pobreza(
    df[~df['Etnia'].isin(['OTRA','MENOR DE 5 AÑOS'])],
    grupo='Etnia',
    titulo="Tasa de pobreza por etnia",
    nombre_archivo="pobreza_etnia"
).properties(
    width='container'
).interactive()
c
```
#
#
#| echo: false
#| warning: false
#| message: false
c=grafico_pobreza(
    df,
    grupo='Nivel de instrucción',
    titulo="Tasa de pobreza por nivel de instrucción",
    nombre_archivo="pobreza_educacion"
).properties(
    width='container'
).interactive()
c
```
#
#
#| echo: false
#| warning: false
#| message: false
df["edad_grupo"] = pd.cut(
    df["p03"].astype(int),
    bins=[0,14, 24, 34, 44, 54, 64,74,84, 120],
    labels=[
        "0–14", "15–24", "25–34",
        "35–44", "45–54", "55–64", "65–74","75–84","85+"
    ],  
    include_lowest=True
)
orden_edades=[
        "0–14", "15–24", "25–34",
        "35–44", "45–54", "55–64", "65–74","75–84","85+"
    ]
df["edad_grupo"] = pd.Categorical(
    df["edad_grupo"],
    categories=orden_edades,
    ordered=True
)
c=grafico_pobreza(
    df,
    grupo="edad_grupo",
    titulo="Tasa de pobreza por grupo de edad",
    nombre_archivo="pobreza_edad"
).properties(
    width='container'
).interactive() 
c
```
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#| echo: false
#| warning: false
#| message: false  
  
df_pobres = df[df["pobreza"] == 1].copy() 
df_pobres = df[df["condact"] != 'SIN EMPLEO'].copy() 
df_pobres = df[df["secemp"] != 'SIN EMPLEO'].copy() 
heatmap_data = (
    df_pobres
    .groupby(["condact", "secemp"], as_index=False)
    .agg(personas_pobres=("fexp", "sum"))
)
heatmap = (
    alt.Chart(heatmap_data)
    .mark_rect()
    .encode(
        x=alt.X(
            "condact:N",
            title="Condición de actividad"
        ),
        y=alt.Y(
            "secemp:N",
            title="Sector de empleo"
        ),
        color=alt.Color(
            "personas_pobres:Q",
            title="Personas pobres",
            scale=alt.Scale(scheme="reds")
        ),
        tooltip=[
            alt.Tooltip("condact:N", title="Condición"),
            alt.Tooltip("secemp:N", title="Sector"),
            alt.Tooltip("personas_pobres:Q", title="Personas pobres", format=",.0f")
        ]
    )
    .properties( 
        title="Personas pobres por condición de actividad y sector de empleo"
    ) 
).properties(
        width='container').interactive()
heatmap
```
#
#
#| echo: false
#| warning: false
#| message: false  
 
# Crear parámetro interactivo para el año
anio_selector = alt.param(
    name="Año",
    bind=alt.binding_select(
        options=sorted(df_pobres["periodo"].unique().tolist()),
        name="Seleccione año: "
    ),
    value=sorted(df_pobres["periodo"].unique())[0]
)

# Agregar año al agrupamiento
heatmap_data = (
    df_pobres
    .groupby(["periodo", "condact", "secemp"], as_index=False)
    .agg(personas_pobres=("fexp", "sum"))
)

# Heatmap
heatmap = (
    alt.Chart(heatmap_data)
    .add_params(anio_selector)
    .transform_filter(alt.datum.periodo == anio_selector)
    .mark_rect()
    .encode(
        x=alt.X(
            "condact:N",
            title="Condición de actividad"
        ),
        y=alt.Y(
            "secemp:N",
            title="Sector de empleo"
        ),
        color=alt.Color(
            "personas_pobres:Q",
            title="Personas pobres",
            scale=alt.Scale(scheme="reds")
        ),
        tooltip=[
            alt.Tooltip("condact:N", title="Condición"),
            alt.Tooltip("secemp:N", title="Sector"),
            alt.Tooltip("personas_pobres:Q", title="Personas pobres", format=",.0f")
        ]
    )
    .properties(
        title="Personas pobres por condición de actividad y sector de empleo",
        width="container"
    )
)

heatmap
```
#
#
#
#| echo: false
#| warning: false
#| message: false  
  
df_pobres = df[df["pobreza"] == 1].copy() 
df_pobres = df[df["condact"] != 'SIN EMPLEO'].copy() 
df_pobres = df[df["secemp"] != 'SIN EMPLEO'].copy() 

heatmap_data = (
    df_pobres
    .groupby(["grupo1", "rama1"], as_index=False)
    .agg(personas_pobres=("fexp", "sum"))
)
heatmap = (
    alt.Chart(heatmap_data)
    .mark_rect()
    .encode(
        x=alt.X(
            "grupo1:N",
            title="Grupo Ocupacional"
        ),
        y=alt.Y(
            "rama1:N",
            title="Rama de actividad"
        ),
        color=alt.Color(
            "personas_pobres:Q",
            title="Personas pobres",
            scale=alt.Scale(scheme="reds")
        ),
        tooltip=[
            alt.Tooltip("grupo1:N", title="Grupo ocupacional"),
            alt.Tooltip("rama1:N", title="Rama de actividad"),
            alt.Tooltip("personas_pobres:Q", title="Personas pobres", format=",.0f")
        ]
    )
    .properties( 
        title="Personas pobres por grupo ocupacional y rama de actividad"
    ) 
).properties(
        width='container').interactive()
heatmap
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#| echo: false
#| warning: false
#| message: false   
df=df[df['ingrl']>0]
df=df[df['ingpc']>0]
base = (
    alt.Chart(df)
    .mark_circle(size=40, opacity=0.5)
    .encode(
        x=alt.X(
            "ingrl:Q",
            title="Ingreso laboral ",
            scale=alt.Scale(zero=False)
        ),
        y=alt.Y(
            "ingpc:Q",
            title="Ingreso per cápita ",
            scale=alt.Scale(zero=False)
        ),
        tooltip=[
            alt.Tooltip("ingrl:Q", title="Ingreso laboral", format=",.0f"),
            alt.Tooltip("ingpc:Q", title="Ingreso per cápita", format=",.0f")
        ]
    )
) 
scatter_pobres = (
    base
    .transform_filter(alt.datum.pobreza == 1)
    .properties(
        title="Personas pobres"
    )
)
scatter_pobres.properties(width='container').interactive()
#
#
#
#| echo: false
#| warning: false
#| message: false   
scatter_no_pobres = (
    base
    .transform_filter(alt.datum.pobreza == 0)
    .properties(
        title="Personas no pobres"
    )
)
scatter_no_pobres.properties(width='container').interactive()
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
