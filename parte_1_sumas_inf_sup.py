"""
parte_1_sumas_inf_sup.py

Parte 1: Convergencia de sumas inferior y superior.

Este archivo:
1. Calcula la suma inferior y superior para f(x)=2sqrt(1-x^2).
2. Genera las tres tablas pedidas en la consigna.
3. Guarda las tablas en archivos CSV.
4. Grafica las sumas inferior y superior junto con pi.
5. Genera gráficas separadas para distintos rangos de N.
6. Grafica residuos y errores absolutos.
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
    residuo,
    error_absoluto,
    obtener_rangos_N,
)


# ============================================================
# 1. Cálculo de suma inferior y suma superior
# ============================================================

def suma_inferior_superior(N):
    """
    Calcula la suma inferior y la suma superior de f en [-1, 1],
    usando una partición equiespaciada de N subintervalos.

    Aclaración:
    En la consigna se habla de cantidad de puntos de la partición.
    En esta implementación tomamos N como cantidad de subintervalos.
    Por lo tanto, la partición tiene N + 1 puntos.
    """

    # Partición equiespaciada
    x = np.linspace(A, B, N + 1)

    # Extremos de cada subintervalo
    x_izq = x[:-1]
    x_der = x[1:]

    # Ancho de cada subintervalo
    delta_x = (B - A) / N

    # Valores de la función en los extremos
    f_izq = f(x_izq)
    f_der = f(x_der)

    # Para la suma inferior, tomamos el mínimo en cada subintervalo.
    # Como la función sube hasta x=0 y luego baja, el mínimo está en un extremo.
    minimos = np.minimum(f_izq, f_der)

    # Para la suma superior, tomamos el máximo en cada subintervalo.
    maximos = np.maximum(f_izq, f_der)

    # Si un subintervalo contiene al 0, el máximo real es f(0)=2.
    contiene_cero = (x_izq <= 0) & (x_der >= 0)
    maximos = np.where(contiene_cero, f(0), maximos)

    suma_inf = np.sum(minimos * delta_x)
    suma_sup = np.sum(maximos * delta_x)

    return suma_inf, suma_sup


# ============================================================
# 2. Generación de tablas
# ============================================================

def generar_tabla(lista_N):
    """
    Genera una tabla con:
    - N
    - suma inferior
    - residuo inferior
    - error absoluto inferior
    - suma superior
    - residuo superior
    - error absoluto superior
    """

    datos = []

    for N in lista_N:
        suma_inf, suma_sup = suma_inferior_superior(N)

        datos.append({
            "N": N,
            "Suma inferior": suma_inf,
            "Residuo inferior": residuo(suma_inf),
            "Error absoluto inferior": error_absoluto(suma_inf),
            "Suma superior": suma_sup,
            "Residuo superior": residuo(suma_sup),
            "Error absoluto superior": error_absoluto(suma_sup),
        })

    return pd.DataFrame(datos)


# ============================================================
# 3. Funciones para graficar
# ============================================================

def graficar_sumas(tabla, titulo, nombre_archivo):
    """
    Grafica suma inferior, suma superior y pi teórico.
    """

    plt.figure(figsize=(10, 6))

    plt.plot(
        tabla["N"],
        tabla["Suma inferior"],
        marker="o",
        label="Suma inferior",
    )

    plt.plot(
        tabla["N"],
        tabla["Suma superior"],
        marker="o",
        label="Suma superior",
    )

    plt.axhline(
        PI_TEORICO,
        linestyle="--",
        label="π teórico",
    )

    plt.xlabel("N")
    plt.ylabel("Aproximación")
    plt.title(titulo)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(f"graficas/{nombre_archivo}", dpi=300)
    plt.show()


def graficar_residuos(tabla, titulo, nombre_archivo):
    """
    Grafica los residuos de la suma inferior y superior.
    """

    plt.figure(figsize=(10, 6))

    plt.plot(
        tabla["N"],
        tabla["Residuo inferior"],
        marker="o",
        label="Residuo suma inferior",
    )

    plt.plot(
        tabla["N"],
        tabla["Residuo superior"],
        marker="o",
        label="Residuo suma superior",
    )

    plt.axhline(
        0,
        linestyle="--",
        label="Residuo cero",
    )

    plt.xlabel("N")
    plt.ylabel("Residuo")
    plt.title(titulo)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(f"graficas/{nombre_archivo}", dpi=300)
    plt.show()


def graficar_error_absoluto(tabla, titulo, nombre_archivo):
    """
    Grafica el error absoluto de la suma inferior y superior.
    """

    plt.figure(figsize=(10, 6))

    plt.plot(
        tabla["N"],
        tabla["Error absoluto inferior"],
        marker="o",
        label="Error absoluto inferior",
    )

    plt.plot(
        tabla["N"],
        tabla["Error absoluto superior"],
        marker="o",
        label="Error absoluto superior",
    )

    plt.xlabel("N")
    plt.ylabel("Error absoluto")
    plt.title(titulo)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(f"graficas/{nombre_archivo}", dpi=300)
    plt.show()


# ============================================================
# 4. Ejecución principal
# ============================================================

def main():
    """
    Ejecuta toda la Parte 1.
    """

    # Crear carpetas de salida si no existen
    os.makedirs("tablas", exist_ok=True)
    os.makedirs("graficas", exist_ok=True)

    # Mostrar números con más decimales en pantalla
    pd.options.display.float_format = "{:.10f}".format

    # Rangos pedidos en la consigna
    N_10_100, N_100_1000, N_1000_10000 = obtener_rangos_N()

    # Generar tablas
    tabla_10_100 = generar_tabla(N_10_100)
    tabla_100_1000 = generar_tabla(N_100_1000)
    tabla_1000_10000 = generar_tabla(N_1000_10000)

    # Generar una tabla con todos los valores de N, eliminando repetidos
    N_todos = sorted(set(list(N_10_100) + list(N_100_1000) + list(N_1000_10000)))
    tabla_todos = generar_tabla(N_todos)

    # Guardar tablas en CSV
    tabla_10_100.to_csv("tablas/parte_1_tabla_N_10_100.csv", index=False, float_format="%.6f")
    tabla_100_1000.to_csv("tablas/parte_1_tabla_N_100_1000.csv", index=False, float_format="%.6f")
    tabla_1000_10000.to_csv("tablas/parte_1_tabla_N_1000_10000.csv", index=False, float_format="%.6f")
    tabla_todos.to_csv("tablas/parte_1_tabla_todos_los_N.csv", index=False, float_format="%.6f")

    # Imprimir tablas en consola
    print("\nTabla 1: N de 10 a 100\n")
    print(tabla_10_100)

    print("\nTabla 2: N de 100 a 1000\n")
    print(tabla_100_1000)

    print("\nTabla 3: N de 1000 a 10000\n")
    print(tabla_1000_10000)

    # Gráfica general
    graficar_sumas(
        tabla_todos,
        "Convergencia de sumas inferior y superior",
        "parte_1_sumas_todos_los_N.png",
    )

    # Gráficas por rango, siguiendo la nota de la consigna
    graficar_sumas(
        tabla_10_100,
        "Sumas inferior y superior para N de 10 a 100",
        "parte_1_sumas_N_10_100.png",
    )

    graficar_sumas(
        tabla_100_1000,
        "Sumas inferior y superior para N de 100 a 1000",
        "parte_1_sumas_N_100_1000.png",
    )

    graficar_sumas(
        tabla_1000_10000,
        "Sumas inferior y superior para N de 1000 a 10000",
        "parte_1_sumas_N_1000_10000.png",
    )

    # Gráfica de residuos
    graficar_residuos(
        tabla_todos,
        "Residuos de las sumas inferior y superior",
        "parte_1_residuos.png",
    )

    # Gráfica de errores absolutos
    graficar_error_absoluto(
        tabla_todos,
        "Error absoluto de las sumas inferior y superior",
        "parte_1_error_absoluto.png",
    )

    # Prueba rápida con algunos valores
    print("\nPrueba rápida:\n")
    for N in [10, 100, 1000, 10000]:
        suma_inf, suma_sup = suma_inferior_superior(N)
        print(f"N = {N}")
        print(f"Suma inferior: {suma_inf:.10f}")
        print(f"Suma superior: {suma_sup:.10f}")
        print(f"π teórico:     {PI_TEORICO:.10f}")
        print(f"Diferencia superior - inferior: {suma_sup - suma_inf:.10f}")
        print()


if __name__ == "__main__":
    main()