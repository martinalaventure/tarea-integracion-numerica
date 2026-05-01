"""
parte_4_montecarlo.py

Parte 4: Integración Montecarlo.

Este archivo:
1. Implementa el método Montecarlo.
2. Genera tablas con aproximaciones.
3. Guarda las tablas en CSV.
4. Grafica los resultados obtenidos para el valor de π.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from funciones_comunes import (
    A,
    B,
    PI_TEORICO,
    f,
    obtener_rangos_N,
)


# ============================================================
# 1. Método Montecarlo
# ============================================================

def montecarlo(N):
    u1 = np.random.uniform(0, 1, N)
    u2 = np.random.uniform(0, 1, N)
    # Transformamos u1 y u2 a las coordenadas x e y del rectángulo que contiene la curva de f(x).
    #Lo que nos pasa es que la variable x solo tiene sentido entre -1 y 1 la función f(x) toma valores entre 0 y 2
    x = A + (B - A) * u1
    y = 2 * u2

    dentro = y <= f(x)

    area_rect = (B - A) * 2

    return area_rect * np.sum(dentro) / N


# ============================================================
# 2. Generación de tablas
# ============================================================

def generar_tabla(lista_N):
    datos = []

    for N in lista_N:
        aprox = montecarlo(N)

        datos.append({
            "N": N,
            "Montecarlo": aprox,
        })

    return pd.DataFrame(datos)


# ============================================================
# 3. Función para graficar
# ============================================================

def graficar(tabla):
    os.makedirs("graficas/parte_4", exist_ok=True)

    plt.figure(figsize=(10, 6))

    plt.plot(
        tabla["N"],
        tabla["Montecarlo"],
        marker="o",
        label="Montecarlo",
    )

    plt.axhline(
        PI_TEORICO,
        linestyle="--",
        label="π teórico",
    )

    #plt.xscale("log") #Dejamos esta linea opcional ya qeu la consigna no lo pedía estrictamente, pero puede ayudar a visualizar mejor los resultados para N grandes.

    plt.xlabel("N")
    plt.ylabel("Valor de π")
    plt.title("Aproximación de π mediante Montecarlo")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig("graficas/parte_4/parte_4_montecarlo.png", dpi=300)
    plt.show()


# ============================================================
# 4. Ejecución principal
# ============================================================

def main():
    os.makedirs("tablas", exist_ok=True)

    pd.options.display.float_format = "{:.10f}".format

    N_10_100, N_100_1000, N_1000_10000 = obtener_rangos_N()

    tabla_10_100 = generar_tabla(N_10_100)
    tabla_100_1000 = generar_tabla(N_100_1000)
    tabla_1000_10000 = generar_tabla(N_1000_10000)

    N_todos = sorted(set(list(N_10_100) + list(N_100_1000) + list(N_1000_10000)))
    tabla_todos = generar_tabla(N_todos)

    # Guardar tablas
    tabla_10_100.to_csv("tablas/parte_4/parte_4_tabla_N_10_100.csv", index=False, float_format="%.6f")
    tabla_100_1000.to_csv("tablas/parte_4/parte_4_tabla_N_100_1000.csv", index=False, float_format="%.6f")
    tabla_1000_10000.to_csv("tablas/parte_4/parte_4_tabla_N_1000_10000.csv", index=False, float_format="%.6f")
    tabla_todos.to_csv("tablas/parte_4/parte_4_tabla_todos_los_N.csv", index=False, float_format="%.6f")

    # gráficar resultados
    graficar(tabla_todos)


if __name__ == "__main__":
    main()