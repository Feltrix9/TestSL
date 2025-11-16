import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("Ejercicio 1: Titanic con botón y gráfico")

@st.cache_data
def cargar_datos():
    df = pd.read_csv("database_titanic.csv")
    return df

df = cargar_datos()

st.write("Usamos el dataset de pasajeros del Titanic")

# Contenedor para controles
with st.container():
    st.subheader("Configuración del gráfico")

    col1, col2 = st.columns(2)

    with col1:
        max_edad = st.slider(
            "Máxima edad a considerar",
            min_value=int(df["Age"].min(skipna=True)),
            max_value=int(df["Age"].max(skipna=True)),
            value=40,
            step=1
        )

    with col2:
        variable_grupo = st.selectbox(
            "Variable para agrupar la tasa de supervivencia",
            ("Sex", "Pclass", "Embarked")
        )

# Segundo contenedor para botón y resultado
with st.container():
    st.subheader("Gráfico de tasa de supervivencia")

    if st.button("Generar gráfico"):
        # Filtramos por edad
        df_filtrado = df[df["Age"] <= max_edad].copy()

        # Agrupamos y calculamos tasa de supervivencia
        tasa = df_filtrado.groupby(variable_grupo)["Survived"].mean() * 100
        tasa = tasa.dropna()

        st.write("Tabla de tasas de supervivencia (%)")
        st.dataframe(tasa.round(2).reset_index())

        # Creamos el gráfico con matplotlib
        fig, ax = plt.subplots()

        x = tasa.index.astype(str)
        y = tasa.values

        # Solo para usar numpy de forma visible
        posiciones = np.arange(len(x))

        ax.bar(posiciones, y)
        ax.set_xticks(posiciones)
        ax.set_xticklabels(x, rotation=0)
        ax.set_ylabel("Supervivencia (%)")
        ax.set_title(f"Tasa de supervivencia por {variable_grupo} (edad ≤ {max_edad})")

        st.pyplot(fig)
    else:
        st.info("Configura los parámetros y pulsa el botón para ver el gráfico")
