import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("Ejercicio 3: Titanic con subplots 2x2")

@st.cache_data
def cargar_datos():
    df = pd.read_csv("database_titanic.csv")
    return df

df = cargar_datos()

st.write("Ejemplo de uso de subplots para partir la figura en 4 zonas")

# Limpiamos algunos datos
df_edad = df[df["Age"].notna()]
df_fare = df[df["Fare"].notna()]

# Creamos figura con 4 zonas
fig, axes = plt.subplots(2, 2, figsize=(10, 8))

# Zona 1 (arriba izquierda): histograma de edades
ax1 = axes[0, 0]
edades = df_edad["Age"]
bins_edad = np.linspace(edades.min(), edades.max(), 20)

ax1.hist(edades, bins=bins_edad)
ax1.set_title("Histograma de Edad")
ax1.set_xlabel("Edad")
ax1.set_ylabel("Frecuencia")

# Zona 2 (arriba derecha): histograma de tarifas
ax2 = axes[0, 1]
fares = df_fare["Fare"]
bins_fare = np.linspace(fares.min(), fares.max(), 20)

ax2.hist(fares, bins=bins_fare)
ax2.set_title("Histograma de Fare")
ax2.set_xlabel("Fare")
ax2.set_ylabel("Frecuencia")

# Zona 3 (abajo izquierda): supervivencia por sexo
ax3 = axes[1, 0]
tasa_sexo = df.groupby("Sex")["Survived"].mean() * 100

x3 = np.arange(len(tasa_sexo.index))
ax3.bar(x3, tasa_sexo.values)
ax3.set_xticks(x3)
ax3.set_xticklabels(tasa_sexo.index)
ax3.set_ylabel("Supervivencia (%)")
ax3.set_title("Supervivencia por Sexo")

# Zona 4 (abajo derecha): supervivencia por clase
ax4 = axes[1, 1]
tasa_clase = df.groupby("Pclass")["Survived"].mean() * 100

x4 = np.arange(len(tasa_clase.index))
ax4.bar(x4, tasa_clase.values)
ax4.set_xticks(x4)
ax4.set_xticklabels(tasa_clase.index)
ax4.set_ylabel("Supervivencia (%)")
ax4.set_title("Supervivencia por Clase")

plt.tight_layout()
st.pyplot(fig)

st.info(
    "Tip: si quieres otra distribución, por ejemplo pantalla en 1x2 o 2x1, "
    "puedes cambiar `plt.subplots(2, 2, ...)` por `(1, 2)` o `(2, 1)` "
    "y ajustar los índices `axes[fila, columna]`."
)
