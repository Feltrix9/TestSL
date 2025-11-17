import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =====================================================
# CONFIGURACIÓN INICIAL
# Más adelante esto NO cambia, solo la parte del layout.
# =====================================================
st.set_page_config(
    page_title="Ejercicio base Titanic",
    layout="wide"
)

st.title("Ejercicio base con Titanic")
st.write("Este ejercicio NO usa columns, containers ni sidebar (los añadirás después)")

@st.cache_data
def cargar_datos():
    return pd.read_csv("database_titanic.csv")

df = cargar_datos()

# =====================================================
# PASO 1 (FUTURO): MOVER FILTROS A LA SIDEBAR
# Ahora los filtros están en el cuerpo principal.
# Más adelante:
#   - Envolver TODO este bloque con:  with st.sidebar:
#   - Cambiar el texto a algo como "Filtros (sidebar)"
# =====================================================
st.subheader("Filtros")

# Filtro de edad
if df["Age"].notna().any():
    edad_min = int(df["Age"].min(skipna=True))
    edad_max = int(df["Age"].max(skipna=True))
else:
    edad_min = 0
    edad_max = 80

rango_edad = st.slider(
    "Rango de edad",
    min_value=edad_min,
    max_value=edad_max,
    value=(max(edad_min, 10), min(edad_max, 50))
)

# Filtro de tarifa
fare_min = float(df["Fare"].min())
fare_max = float(df["Fare"].max())

max_fare = st.slider(
    "Fare máximo",
    min_value=fare_min,
    max_value=fare_max,
    value=float(np.percentile(df["Fare"], 75))
)

# =====================================================
# PASO 2 (FUTURO): PRIMER CONTAINER PARA "RESUMEN"
# Ahora solo mostramos "Aplicando filtros" y el conteo.
# Más adelante:
#   - Envolver este bloque con:  with st.container():
#   - Aquí puedes agregar métricas con st.metric en columnas.
# =====================================================
st.subheader("Aplicando filtros")

df_filtrado = df.copy()
df_filtrado = df_filtrado[
    df_filtrado["Age"].between(rango_edad[0], rango_edad[1]) &
    (df_filtrado["Fare"] <= max_fare)
]

st.metric("Pasajeros filtrados", len(df_filtrado))

if "Survived" in df_filtrado.columns and len(df_filtrado) > 0:
    tasa = df_filtrado["Survived"].mean() * 100
    st.metric("Supervivencia", f"{tasa:.1f} %")
else:
    st.metric("Supervivencia", "N A")

if len(df_filtrado) > 0:
    st.metric("Fare promedio", f"{df_filtrado['Fare'].mean():.2f}")
else:
    st.metric("Fare promedio", "N A")

# =====================================================
# PASO 3 (FUTURO): SEGUNDO CONTAINER PARA LOS GRÁFICOS
# Ahora los gráficos están uno debajo del otro.
# Más adelante:
#   - Crear:  with st.container():  antes del primer gráfico
#   - Dentro del container usar:  col1, col2 = st.columns(2)
#   - Poner el gráfico 1 en col1 y el gráfico 2 en col2
# =====================================================

# ========= Gráfico 1: histograma de edad =========
st.subheader("Gráfico 1: Histograma de edades")

if not df_filtrado.empty and df_filtrado["Age"].notna().any():
    fig1, ax1 = plt.subplots()
    edades = df_filtrado["Age"].dropna()
    bins_edad = np.linspace(edades.min(), edades.max(), 12)

    ax1.hist(edades, bins=bins_edad)
    ax1.set_xlabel("Edad")
    ax1.set_ylabel("Frecuencia")
    ax1.set_title("Edades filtradas")

    st.pyplot(fig1)
else:
    st.warning("No hay datos de edad válidos con estos filtros")

# ========= Gráfico 2: barras por clase =========
st.subheader("Gráfico 2: Pasajeros por clase (Pclass)")

if "Pclass" in df_filtrado.columns and not df_filtrado.empty:
    conteo_clase = df_filtrado["Pclass"].value_counts().sort_index()

    fig2, ax2 = plt.subplots()
    x = np.arange(len(conteo_clase.index))
    ax2.bar(x, conteo_clase.values)
    ax2.set_xticks(x)
    ax2.set_xticklabels(conteo_clase.index)
    ax2.set_xlabel("Clase")
    ax2.set_ylabel("Cantidad de pasajeros")
    ax2.set_title("Pasajeros por clase con filtros aplicados")

    st.pyplot(fig2)
else:
    st.warning("No hay información de Pclass con estos filtros")

# =====================================================
# PASO 4 (FUTURO): USAR EXPANDER PARA LA TABLA
# Ahora la tabla se muestra SIEMPRE.
# Más adelante:
#   - Reemplazar este bloque por:
#
#       with st.expander("Ver tabla filtrada"):
#           st.dataframe(...)
#
#   - Opcional: envolver también en un container.
# =====================================================
st.subheader("Tabla filtrada")

st.dataframe(df_filtrado[["PassengerId", "Name", "Sex", "Age", "Pclass", "Fare", "Survived"]])
