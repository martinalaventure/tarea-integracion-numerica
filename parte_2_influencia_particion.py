"""
Parte 2: Influencia de la partición.

Se reutilizan de funciones_comunes.py:
- A, B
- PI_TEORICO
- f
- residuo
- error_absoluto
- obtener_rangos_N

No se reutiliza suma_inferior_superior de la parte 1 porque esa función
usa siempre partición equiespaciada.
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
# 1 - Generar particiones
# ============================================================

def particion_equiespaciada(N):
    """
    Genera una partición equiespaciada de [-1, 1].
    """
    return np.linspace(A, B, N + 1)


def particion_aleatoria_uniforme(N):
    """
    Genera una partición aleatoria uniforme de [-1, 1].
    """
    puntos_interiores = np.random.uniform(A, B, N - 1)
    x = np.concatenate(([A], puntos_interiores, [B]))
    return np.sort(x)


def particion_coseno(N):
    """
    Genera una partición de la forma: x_i = cos(i*pi/N)

    Como naturalmente va de 1 a -1, se ordena para que quede de -1 a 1.
    """
    i = np.arange(0, N + 1)
    x = np.cos(i * np.pi / N)
    return np.sort(x)


# ============================================================
# 2 - Generar tablas comparativas
# ============================================================

def suma_con_particion(x):
    """
    Calcula la suma superior usando una partición cualquiera.
    """

    x_izq = x[:-1]
    x_der = x[1:]

    delta_x = x_der - x_izq

    f_izq = f(x_izq)
    f_der = f(x_der)

    alturas = np.maximum(f_izq, f_der)

    contiene_cero = (x_izq <= 0) & (x_der >= 0)
    alturas = np.where(contiene_cero, f(0), alturas)

    return np.sum(alturas * delta_x)


def generar_tabla(lista_N):
    """
    Genera una tabla comparando:
    - partición equiespaciada
    - partición aleatoria uniforme
    - partición coseno
    """

    datos = []

    for N in lista_N:
        x_equiespaciada = particion_equiespaciada(N)
        x_aleatoria = particion_aleatoria_uniforme(N)
        x_coseno = particion_coseno(N)

        suma_equiespaciada = suma_con_particion(x_equiespaciada)
        suma_aleatoria = suma_con_particion(x_aleatoria)
        suma_coseno = suma_con_particion(x_coseno)

        datos.append({
            "N": N,

            "Aprox equiespaciada": suma_equiespaciada,
            "Residuo equiespaciada": residuo(suma_equiespaciada),
            "Error absoluto equiespaciada": error_absoluto(suma_equiespaciada),

            "Aprox aleatoria": suma_aleatoria,
            "Residuo aleatoria": residuo(suma_aleatoria),
            "Error absoluto aleatoria": error_absoluto(suma_aleatoria),

            "Aprox coseno": suma_coseno,
            "Residuo coseno": residuo(suma_coseno),
            "Error absoluto coseno": error_absoluto(suma_coseno),
        })

    return pd.DataFrame(datos)


# ============================================================
# 3. Graficar aproximaciones
# ============================================================

def graficar_aproximaciones(tabla, titulo, nombre_archivo):
    """
    Grafica las 3 aproximaciones y el valor teórico de pi.
    """

    plt.figure(figsize=(10, 6))

    plt.plot(
        tabla["N"],
        tabla["Aprox equiespaciada"],
        marker="o",
        label="Equiespaciada",
    )

    plt.plot(
        tabla["N"],
        tabla["Aprox aleatoria"],
        marker="o",
        label="Aleatoria uniforme",
    )

    plt.plot(
        tabla["N"],
        tabla["Aprox coseno"],
        marker="o",
        label="Coseno",
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

    plt.savefig(f"graficas/parte_2/{nombre_archivo}", dpi=300)
    plt.show()


# ============================================================
# 3. Graficar residuos
# ============================================================

def graficar_residuos(tabla, titulo, nombre_archivo):
    """
    Grafica los residuos de las 3 particiones.
    """

    plt.figure(figsize=(10, 6))

    plt.plot(
        tabla["N"],
        tabla["Residuo equiespaciada"],
        marker="o",
        label="Residuo equiespaciada",
    )

    plt.plot(
        tabla["N"],
        tabla["Residuo aleatoria"],
        marker="o",
        label="Residuo aleatoria",
    )

    plt.plot(
        tabla["N"],
        tabla["Residuo coseno"],
        marker="o",
        label="Residuo coseno",
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

    plt.savefig(f"graficas/parte_2/{nombre_archivo}", dpi=300)
    plt.show()


# ============================================================
# 4. Graficar función y rectángulos
# ============================================================

def graficar_rectangulos(nombre_particion, x, nombre_archivo):
    """
    Grafica f(x) y los rectángulos de aproximación.
    """

    puntos = np.linspace(A, B, 1000)

    plt.figure(figsize=(10, 6))

    plt.plot(
        puntos,
        f(puntos),
        label="f(x) = 2√(1 - x²)",
    )

    x_izq = x[:-1]
    x_der = x[1:]

    delta_x = x_der - x_izq

    f_izq = f(x_izq)
    f_der = f(x_der)

    alturas = np.maximum(f_izq, f_der)

    contiene_cero = (x_izq <= 0) & (x_der >= 0)
    alturas = np.where(contiene_cero, f(0), alturas)
    
    plt.bar(
        x_izq,
        alturas,
        width=delta_x,
        align="edge",
        alpha=0.4,
        edgecolor="black",
        label="Rectángulos",
    )

    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title(f"Rectángulos con partición {nombre_particion}, N = 100")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(f"graficas/parte_2/{nombre_archivo}", dpi=300)
    plt.show()


# ============================================================
# 5. Programa principal
# ============================================================

def main():
    """
    Ejecuta toda la parte 2.
    """

    # Para que la partición aleatoria dé siempre igual al volver a ejecutar
    np.random.seed(1)

    os.makedirs("tablas/parte_2", exist_ok=True)
    os.makedirs("graficas/parte_2", exist_ok=True)

    pd.options.display.float_format = "{:.10f}".format

    # Reutilizado de funciones_comunes.py
    N_10_100, N_100_1000, N_1000_10000 = obtener_rangos_N()

    tabla_10_100 = generar_tabla(N_10_100)
    tabla_100_1000 = generar_tabla(N_100_1000)
    tabla_1000_10000 = generar_tabla(N_1000_10000)

    N_todos = sorted(set(
        list(N_10_100)
        + list(N_100_1000)
        + list(N_1000_10000)
    ))

    tabla_todos = generar_tabla(N_todos)

    tabla_10_100.to_csv(
        "tablas/parte_2/parte_2_tabla_N_10_100.csv",
        index=False,
        float_format="%.6f",
    )

    tabla_100_1000.to_csv(
        "tablas/parte_2/parte_2_tabla_N_100_1000.csv",
        index=False,
        float_format="%.6f",
    )

    tabla_1000_10000.to_csv(
        "tablas/parte_2/parte_2_tabla_N_1000_10000.csv",
        index=False,
        float_format="%.6f",
    )

    tabla_todos.to_csv(
        "tablas/parte_2/parte_2_tabla_todos_los_N.csv",
        index=False,
        float_format="%.6f",
    )

    print("\nTabla 1: N de 10 a 100\n")
    print(tabla_10_100)

    print("\nTabla 2: N de 100 a 1000\n")
    print(tabla_100_1000)

    print("\nTabla 3: N de 1000 a 10000\n")
    print(tabla_1000_10000)

    graficar_aproximaciones(
        tabla_todos,
        "Aproximaciones para distintas particiones",
        "parte_2_aproximaciones_todos_los_N.png",
    )

    graficar_aproximaciones(
        tabla_10_100,
        "Aproximaciones para N de 10 a 100",
        "parte_2_aproximaciones_N_10_100.png",
    )

    graficar_aproximaciones(
        tabla_100_1000,
        "Aproximaciones para N de 100 a 1000",
        "parte_2_aproximaciones_N_100_1000.png",
    )

    graficar_aproximaciones(
        tabla_1000_10000,
        "Aproximaciones para N de 1000 a 10000",
        "parte_2_aproximaciones_N_1000_10000.png",
    )

    graficar_residuos(
        tabla_todos,
        "Residuos para distintas particiones",
        "parte_2_residuos_todos_los_N.png",
    )

    # Rectángulos con N = 100
    N_rectangulos = 100

    graficar_rectangulos(
        "equiespaciada",
        particion_equiespaciada(N_rectangulos),
        "parte_2_rectangulos_equiespaciada_N_100.png",
    )

    graficar_rectangulos(
        "aleatoria uniforme",
        particion_aleatoria_uniforme(N_rectangulos),
        "parte_2_rectangulos_aleatoria_N_100.png",
    )

    graficar_rectangulos(
        "coseno",
        particion_coseno(N_rectangulos),
        "parte_2_rectangulos_coseno_N_100.png",
    )

    print("\nParte 2 ejecutada correctamente.")


if __name__ == "__main__":
    main()