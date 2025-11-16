
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("Ejercicio 1: Gráfico interactivo con particiones")

st.write("Este ejemplo usa pandas, numpy y matplotlib con layout por columnas")

# Contenedor principal
with st.container():
    st.subheader("Configuración del gráfico")

    # Particiones con columnas
    col1, col2 = st.columns(2)

    with col1:
        n_puntos = st.slider(
            "Número de puntos",
            min_value=10,
            max_value=300,
            value=100,
            step=10
        )

    with col2:
        n_series = st.slider(
            "Número de series",
            min_value=1,
            max_value=5,
            value=3,
            step=1
        )

# Segundo contenedor para botón y resultado
with st.container():
    st.subheader("Generación de datos y gráfico")

    if st.button("Generar nuevo gráfico"):
        # Generar DataFrame con numpy y pandas
        index = np.arange(n_puntos)
        data = {
            f"serie_{i+1}": np.random.randn(n_puntos).cumsum()
            for i in range(n_series)
        }
        df = pd.DataFrame(data, index=index)

        st.write("Vista previa de los datos")
        st.dataframe(df.head())

        # Crear gráfico con matplotlib
        fig, ax = plt.subplots()
        df.plot(ax=ax)
        ax.set_xlabel("Índice")
        ax.set_ylabel("Valor")
        ax.set_title("Series aleatorias acumuladas")

        st.pyplot(fig)
    else:
        st.info("Mueve los sliders y presiona el botón para ver el gráfico")
