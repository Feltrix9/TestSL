import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="App Titanic con 3 ejercicios",
    layout="wide"
)

st.title("App Titanic con 3 ejercicios en 1")


@st.cache_data
def cargar_datos():
    df = pd.read_csv("database_titanic.csv")
    return df


df = cargar_datos()

st.markdown("Usando el archivo **database_titanic.csv** como fuente de datos")


# ==========================
# Ejercicio 1
# ==========================
def ejercicio_1(df):
    st.header("Ejercicio 1: Botón, gráfico, pandas, numpy y layout con columnas")

    st.write("Configuramos un gráfico de tasa de supervivencia según distintas variables")

    with st.container():
        st.subheader("Parámetros del gráfico")

        col1, col2 = st.columns(2)

        with col1:
            # proteger por si Age tiene nulos
            edad_min = int(df["Age"].min(skipna=True)) if df["Age"].notna().any() else 0
            edad_max = int(df["Age"].max(skipna=True)) if df["Age"].notna().any() else 80

            max_edad = st.slider(
                "Máxima edad a considerar",
                min_value=edad_min,
                max_value=edad_max,
                value=min(40, edad_max),
                step=1
            )

        with col2:
            variable_grupo = st.selectbox(
                "Variable para agrupar la tasa de supervivencia",
                ("Sex", "Pclass", "Embarked")
            )

    with st.container():
        st.subheader("Resultado")

        if st.button("Generar gráfico del ejercicio 1"):
            df_filtrado = df[df["Age"] <= max_edad].copy()

            tasa = df_filtrado.groupby(variable_grupo)["Survived"].mean() * 100
            tasa = tasa.dropna()

            st.write("Tabla de tasas de supervivencia (%)")
            st.dataframe(tasa.round(2).reset_index())

            fig, ax = plt.subplots()

            x = tasa.index.astype(str)
            y = tasa.values

            posiciones = np.arange(len(x))

            ax.bar(posiciones, y)
            ax.set_xticks(posiciones)
            ax.set_xticklabels(x)
            ax.set_ylabel("Supervivencia (%)")
            ax.set_title(f"Tasa de supervivencia por {variable_grupo} (edad ≤ {max_edad})")

            st.pyplot(fig)
        else:
            st.info("Ajusta los parámetros y pulsa el botón para generar el gráfico")


# ==========================
# Ejercicio 2
# ==========================
def ejercicio_2(df):
    st.header("Ejercicio 2: Tabla filtrada con sliders en la sidebar")

    st.write("La tabla principal se filtra con los controles que están en la barra lateral")

    with st.sidebar:
        st.subheader("Filtros ejercicio 2")

        edad_min = int(df["Age"].min(skipna=True)) if df["Age"].notna().any() else 0
        edad_max = int(df["Age"].max(skipna=True)) if df["Age"].notna().any() else 80

        rango_edad = st.slider(
            "Rango de edad",
            min_value=edad_min,
            max_value=edad_max,
            value=(max(edad_min, 20), min(edad_max, 50)),
            key="rango_edad_ej2"
        )

        fare_min = float(df["Fare"].min())
        fare_max = float(df["Fare"].max())

        max_fare = st.slider(
            "Tarifa máxima (Fare)",
            min_value=fare_min,
            max_value=fare_max,
            value=float(np.percentile(df["Fare"], 75)),
            key="max_fare_ej2"
        )

        sexo_opciones = ["Todos"] + sorted(df["Sex"].dropna().unique().tolist())
        sexo_sel = st.selectbox("Sexo", sexo_opciones, key="sexo_ej2")

    df_filtrado = df.copy()
    df_filtrado = df_filtrado[
        df_filtrado["Age"].between(rango_edad[0], rango_edad[1]) &
        (df_filtrado["Fare"] <= max_fare)
    ]

    if sexo_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Sex"] == sexo_sel]

    st.subheader("Tabla filtrada de pasajeros")

    st.write(
        f"Pasajeros con edad entre {rango_edad[0]} y {rango_edad[1]}, "
        f"Fare ≤ {max_fare:.2f}"
        + ("" if sexo_sel == "Todos" else f", sexo = {sexo_sel}")
    )

    columnas_tabla = ["PassengerId", "Name", "Sex", "Age", "Pclass", "Fare", "Survived"]
    columnas_tabla = [c for c in columnas_tabla if c in df_filtrado.columns]

    st.dataframe(df_filtrado[columnas_tabla])

    st.subheader("Distribución de edades filtradas")

    if not df_filtrado.empty and df_filtrado["Age"].notna().any():
        fig, ax = plt.subplots()

        edades = df_filtrado["Age"].dropna()
        bins = np.linspace(edades.min(), edades.max(), 15)

        ax.hist(edades, bins=bins)
        ax.set_xlabel("Edad")
        ax.set_ylabel("Frecuencia")
        ax.set_title("Histograma de edades filtradas")

        st.pyplot(fig)
    else:
        st.warning("No hay pasajeros que cumplan los filtros actuales o no hay edades válidas")


# ==========================
# Ejercicio 3
# ==========================
def ejercicio_3(df):
    st.header("Ejercicio 3: Subplots con la pantalla partida en 4 zonas")

    st.write("Ejemplo de cómo organizar varios gráficos en una figura 2x2")

    df_edad = df[df["Age"].notna()]
    df_fare = df[df["Fare"].notna()]

    fig, axes = plt.subplots(2, 2, figsize=(10, 8))

    # Zona 1
    ax1 = axes[0, 0]
    if not df_edad.empty:
        edades = df_edad["Age"]
        bins_edad = np.linspace(edades.min(), edades.max(), 20)

        ax1.hist(edades, bins=bins_edad)
        ax1.set_title("Histograma de Edad")
        ax1.set_xlabel("Edad")
        ax1.set_ylabel("Frecuencia")
    else:
        ax1.text(0.5, 0.5, "Sin datos de edad", ha="center", va="center")
        ax1.set_axis_off()

    # Zona 2
    ax2 = axes[0, 1]
    if not df_fare.empty:
        fares = df_fare["Fare"]
        bins_fare = np.linspace(fares.min(), fares.max(), 20)

        ax2.hist(fares, bins=bins_fare)
        ax2.set_title("Histograma de Fare")
        ax2.set_xlabel("Fare")
        ax2.set_ylabel("Frecuencia")
    else:
        ax2.text(0.5, 0.5, "Sin datos de Fare", ha="center", va="center")
        ax2.set_axis_off()

    # Zona 3
    ax3 = axes[1, 0]
    if "Sex" in df.columns:
        tasa_sexo = df.groupby("Sex")["Survived"].mean() * 100

        x3 = np.arange(len(tasa_sexo.index))
        ax3.bar(x3, tasa_sexo.values)
        ax3.set_xticks(x3)
        ax3.set_xticklabels(tasa_sexo.index)
        ax3.set_ylabel("Supervivencia (%)")
        ax3.set_title("Supervivencia por Sexo")
    else:
        ax3.text(0.5, 0.5, "Sin columna Sex", ha="center", va="center")
        ax3.set_axis_off()

    # Zona 4
    ax4 = axes[1, 1]
    if "Pclass" in df.columns:
        tasa_clase = df.groupby("Pclass")["Survived"].mean() * 100

        x4 = np.arange(len(tasa_clase.index))
        ax4.bar(x4, tasa_clase.values)
        ax4.set_xticks(x4)
        ax4.set_xticklabels(tasa_clase.index)
        ax4.set_ylabel("Supervivencia (%)")
        ax4.set_title("Supervivencia por Clase")
    else:
        ax4.text(0.5, 0.5, "Sin columna Pclass", ha="center", va="center")
        ax4.set_axis_off()

    plt.tight_layout()
    st.pyplot(fig)

    st.info(
        "Puedes cambiar la distribución usando plt.subplots(1, 2), (2, 1), etc "
        "y jugar con qué va en cada zona axes[fila, columna]"
    )


# ==========================
# Menú principal
# ==========================
opcion = st.sidebar.radio(
    "Selecciona el ejercicio",
    (
        "Ejercicio 1: Botón y gráfico",
        "Ejercicio 2: Tabla y sidebar",
        "Ejercicio 3: Subplots 2x2"
    )
)

if opcion.startswith("Ejercicio 1"):
    ejercicio_1(df)
elif opcion.startswith("Ejercicio 2"):
    ejercicio_2(df)
else:
    ejercicio_3(df)
