import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import pearsonr
import matplotlib.pyplot as plt

# Configurar Matplotlib para usar texto en formato SVG
plt.rcParams["svg.fonttype"] = "none"

# Listas de nombres de archivos
archivos_vel_csv = [f"v{i}_vel.csv" for i in range(1, 11)]
archivos_p_csv = [f"v{i}.csv" for i in range(1, 11)]

# Inicializar listas para almacenar las velocidades máximas y los valores máximos de p
velocidades_maximas = []
p_maximos = []

# Leer cada archivo de velocidades y extraer la velocidad máxima de la columna 'U:2'
for archivo in archivos_vel_csv:
    df = pd.read_csv(archivo)
    if "U:2" in df.columns:
        velocidad_maxima = df["U:2"].max()
        velocidades_maximas.append(velocidad_maxima)
    else:
        raise ValueError(f"El archivo {archivo} no contiene una columna llamada 'U:2'.")

# Leer cada archivo de p y extraer el valor máximo de la columna 'p'
for archivo in archivos_p_csv:
    df = pd.read_csv(archivo)
    if "p" in df.columns:
        p_maximo = df["p"].max()
        p_maximos.append(p_maximo)
    else:
        raise ValueError(f"El archivo {archivo} no contiene una columna llamada 'p'.")

# Crear los vectores V e I con los valores máximos obtenidos y agregar el punto (0,0)
V = np.array([0] + velocidades_maximas)
I = np.array([0] + p_maximos) / (9.81 * 0.01)


# Definimos la función parabólica con término lineal y cuadrático
def parabola(x, a, b):
    return a * x + b * x**2


# Ajuste de los datos a la parábola
popt, pcov = curve_fit(parabola, V, I)
a, b = popt

# Coeficiente de correlación de Pearson
r, _ = pearsonr(I, parabola(V, a, b))

# Imprimir los coeficientes de ajuste y el coeficiente de correlación
print(f"Coeficiente a: {a}")
print(f"Coeficiente b: {b}")
print(f"Coeficiente de correlación de Pearson: {r}")

# Discretización fina para la curva ajustada
V_fine = np.linspace(min(V), max(V), 1000)
I_fine = parabola(V_fine, a, b)

# Convertir tamaño de cm a pulgadas
width_inch = 7.5 / 2.54
height_inch = 6.0 / 2.54

# Crear el gráfico de línea para los datos ordenados
plt.figure(figsize=(width_inch, height_inch))

plt.scatter(V, I, label="Datos", color="blue", marker="o")
plt.plot(
    V_fine,
    I_fine,
    label=f"Ajuste: $I = {a:.2f}V + {b:.2f}V^2$",
    color="red",
    linestyle="-",
    linewidth=2,
)
plt.xlabel("V (m/s)", fontsize=12)
plt.ylabel("I (m/m)", fontsize=12)
plt.title("Ajuste Parabólico de Datos", fontsize=12)
plt.tick_params(axis="both", which="major", labelsize=12)
plt.text(
    0.1,
    0.9,
    f"$r^2 = {r:.7f}$",
    transform=plt.gca().transAxes,
    fontsize=12,
    verticalalignment="top",
)

# Añadir una cuadrícula más suave
plt.grid(True, which="both", linestyle="--", linewidth=0.5)

# Añadir leyenda
plt.legend(loc="best", fontsize=12)

# Ajustar el diseño para evitar recortes
plt.tight_layout()

# Guardar la figura en formato SVG
plt.savefig("Ajuste.svg", format="svg")

# Mostrar el gráfico
plt.show()
