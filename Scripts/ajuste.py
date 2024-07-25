import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import pearsonr
import matplotlib.pyplot as plt


# Definimos la función parabólica con término lineal y cuadrático
def parabola(x, a, b):
    return a * x + b * x**2


# Vectores de ejemplo (reemplaza con tus datos)
V = np.array([0, 0.1018, 0.1431, 0.1734, 0.1940, 0.2051, 0.2247, 0.2457, 0.2557])
I = np.array([0, 0.0082, 0.0154, 0.022, 0.0271, 0.03, 0.0358, 0.0426, 0.0460]) / 0.01
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

# Graficar los datos y el ajuste con estilo mejorado
plt.figure(figsize=(10, 6))
plt.scatter(V, I, label="Datos", color="blue", marker="o")
plt.plot(
    V_fine,
    I_fine,
    label=f"Ajuste: $I = {a:.2f}V + {b:.2f}V^2$",
    color="red",
    linestyle="-",
    linewidth=2,
)
plt.xlabel("V (m/s)", fontsize=14)
plt.ylabel("I (m/m)", fontsize=14)
plt.title("Ajuste Parabólico de Datos", fontsize=16)
plt.legend(fontsize=12)
plt.grid(True, linestyle="--", alpha=0.7)
plt.tick_params(axis="both", which="major", labelsize=12)
plt.text(
    0.1,
    0.9,
    f"$r^2 = {r:.5f}$",
    transform=plt.gca().transAxes,
    fontsize=14,
    verticalalignment="top",
)
plt.tight_layout()

# Guardar el gráfico como un archivo PNG de alta resolución
# plt.savefig("ajuste_parabolico.png", dpi=300)

# Mostrar el gráfico
plt.show()
