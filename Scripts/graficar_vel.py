import matplotlib.pyplot as plt
import pandas as pd

# Cargar los datos de los archivos CSV
files = [
    "v1_vel.csv",
    "v2_vel.csv",
    "v3_vel.csv",
    "v4_vel.csv",
    "v5_vel.csv",
    "v6_vel.csv",
    "v7_vel.csv",
    "v8_vel.csv",
]

# Leer los archivos y almacenar los DataFrames en una lista
dataframes = [pd.read_csv(file) for file in files]

# Configurar la figura para el gráfico
plt.figure(figsize=(14, 8))

# Graficar la columna 'p' para cada archivo
for i, df in enumerate(dataframes):
    plt.plot(df["Points:1"], df["U:2"], label=f"v{i+1}")

# Configuraciones del gráfico
plt.xlabel("Distancia y (m)")
plt.ylabel("Velocidad (m/s)")
plt.title("Comparación de Velocidad  vs Distancia en y")
plt.legend()
plt.grid(True)

# Mostrar el gráfico
plt.show()
