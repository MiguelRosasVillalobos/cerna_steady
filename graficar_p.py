import matplotlib.pyplot as plt
import pandas as pd

# Cargar los datos de los archivos CSV
files = [
    "v1.csv",
    "v2.csv",
    "v3.csv",
    "v4.csv",
    "v5.csv",
    "v6.csv",
    "v7.csv",
    "v8.csv",
]

# Leer los archivos y almacenar los DataFrames en una lista
dataframes = [pd.read_csv(file) for file in files]

# Configurar la figura para el gráfico
plt.figure(figsize=(14, 8))

# Graficar la columna 'p' para cada archivo
for i, df in enumerate(dataframes):
    plt.plot(df["Points:2"], df["p"] / 9.81, label=f"v{i+1}")

# Configuraciones del gráfico
plt.xlabel("Distancia z (m)")
plt.ylabel("Perdidad de Carga (m)")
plt.title("Comparación de Perdida de Carga vs distancia z ")
plt.legend()
plt.grid(True)

# Mostrar el gráfico
plt.show()
