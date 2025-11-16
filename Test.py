import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("Ejercicio 2: Tabla y slider en la barra lateral")

st.write("Ejemplo de tabla filtrada usando un slider en la sidebar")

# Crear datos de ejemplo con pandas y numpy
np.random.seed(42)
n_filas = 200

df = pd.DataFrame({
    "id": np.arange(1, n_filas + 1),
    "edad": np.random.randint(18, 65, size=n_filas),
    "puntaje": np.random.normal(loc=50, scale=10, size=n_filas).round(1)
})

# Controles en la sidebar
with st.sidebar:
    st.header("Filtros")

    edad_min, edad_max = int(df["edad"].min()), int(df["edad"].max())
    rango_edad = st.slider(
        "Rango de edad",
        min_value=edad_min,
        max_value=edad_max,
        value=(25, 40)
    )

    puntaje_min = float(df["puntaje"].min())
    puntaje_max = float(df["puntaje"].max())
    umbral_puntaje = st.slider(
        "Puntaje mínimo",
        min_value=puntaje_min,
        max_value=puntaje_max,
        value=50.0
    )

# Filtrar datos según sliders
filtro = (
    (df["edad"] >= rango_edad[0]) &
    (df["edad"] <= rango_edad[1]) &
    (df["puntaje"] >= umbral_puntaje)
)
df_filtrado = df[filtro]

st.subheader("Tabla filtrada")

st.write(
    f"Mostrando filas donde la edad está entre "
    f"{rango_edad[0]} y {rango_edad[1]} "
    f"y el puntaje es mayor o igual a {umbral_puntaje}"
)

st.dataframe(df_filtrado)

st.subheader("Distribución de puntajes filtrados")

if not df_filtrado.empty:
    fig, ax = plt.subplots()
    ax.hist(df_filtrado["puntaje"], bins=15)
    ax.set_xlabel("Puntaje")
    ax.set_ylabel("Frecuencia")
    ax.set_title("Histograma de puntajes filtrados")
    st.pyplot(fig)
else:
    st.warning("No hay datos que coincidan con los filtros actuales")
