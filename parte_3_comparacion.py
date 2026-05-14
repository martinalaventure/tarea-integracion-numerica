"""
parte_3_comparacion.py
 
Parte 3: Comparación de métodos de integración numérica
 
Este archivo:
1. Implementa los métodos de rectángulos, trapecio y punto medio
2. Genera las tres tablas pedidas en la consigna
3. Guarda las tablas en archivos CSV
4. Grafica las tres aproximaciones junto con pi teórico
5. Genera gráficas separadas para distintos rangos de N
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
 
 
# Métodos de integración numérica
 
def metodo_rectangulos(N):
    """
    Aproxima la integral de f en [A, B] usando el método de rectángulos (extremo izquierdo de cada subintervalo)
 
    Para cada subintervalo [x_i, x_{i+1}] se construye un rectángulo de base delta_x y altura f(x_i)
    """
    x = np.linspace(A, B, N + 1)
    delta_x = (B - A) / N
    return np.sum(f(x[:-1]) * delta_x)

def metodo_trapecio(N):
    """
    Aproxima la integral de f en [A, B] usando la regla del trapecio
 
    Para cada subintervalo [x_i, x_{i+1}] se construye un trapecio definido por los puntos (x_i, f(x_i)) y (x_{i+1}, f(x_{i+1}))
 
    Fórmula compuesta:
        T_N = (delta_x / 2) * (f(x_0) + 2*f(x_1) + ... + 2*f(x_{N-1}) + f(x_N))
    """
    x = np.linspace(A, B, N + 1)
    delta_x = (B - A) / N
    return delta_x * (f(x[0]) / 2 + np.sum(f(x[1:-1])) + f(x[-1]) / 2)

def metodo_punto_medio(N):
    """
    Aproxima la integral de f en [A, B] usando la regla del punto medio
 
    Para cada subintervalo [x_i, x_{i+1}] se evalúa la función en el centro del subintervalo: c_i = (x_i + x_{i+1}) / 2
    """
    x = np.linspace(A, B, N + 1)
    delta_x = (B - A) / N
    centros = (x[:-1] + x[1:]) / 2
    return np.sum(f(centros) * delta_x)
 
 
# Generar tablas
 
def generar_tabla(lista_N):
    """
    Generar una tabla con los resultados de los tres métodos para cada N
 
    Columnas:
    - N
    - Rectángulos, Residuo rectángulos
    - Trapecio, Residuo trapecio
    - Punto medio, Residuo punto medio
    """
    datos = []
 
    for N in lista_N:
        rect  = metodo_rectangulos(N)
        trap  = metodo_trapecio(N)
        medio = metodo_punto_medio(N)
 
        datos.append({
            "N":                    N,
            "Rectangulos":          rect,
            "Residuo Rectangulos":  residuo(rect),
            "Trapecio":             trap,
            "Residuo Trapecio":     residuo(trap),
            "Punto medio":          medio,
            "Residuo Punto medio":  residuo(medio),
        })
 
    return pd.DataFrame(datos)
 
# Funciones para graficar
 
def graficar_metodos(tabla, titulo, nombre_archivo):
    """
    Grafica de las tres aproximaciones y el valor teórico de pi.
    """
    plt.figure(figsize=(10, 6))
 
    plt.plot(
        tabla["N"],
        tabla["Rectangulos"],
        marker="o",
        label="Rectángulos",
    )
 
    plt.plot(
        tabla["N"],
        tabla["Trapecio"],
        marker="s",
        label="Trapecio",
    )
 
    plt.plot(
        tabla["N"],
        tabla["Punto medio"],
        marker="^",
        label="Punto medio",
    )
 
    plt.axhline(
        PI_TEORICO,
        linestyle="--",
        color="gray",
        label="π teórico",
    )
 
    plt.xlabel("N")
    plt.ylabel("Aproximación")
    plt.title(titulo)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
 
    plt.savefig(f"graficas/parte_3/{nombre_archivo}", dpi=300)
    plt.show()
 
 
def graficar_residuos(tabla, titulo, nombre_archivo):
    """
    Grafica de los residuos de los tres métodos.
    """
    plt.figure(figsize=(10, 6))
 
    plt.plot(
        tabla["N"],
        tabla["Residuo Rectangulos"],
        marker="o",
        label="Residuo rectángulos",
    )
 
    plt.plot(
        tabla["N"],
        tabla["Residuo Trapecio"],
        marker="s",
        label="Residuo trapecio",
    )
 
    plt.plot(
        tabla["N"],
        tabla["Residuo Punto medio"],
        marker="^",
        label="Residuo punto medio",
    )
 
    plt.axhline(0, linestyle="--", color="gray", label="Residuo cero")
 
    plt.xlabel("N")
    plt.ylabel("Residuo")
    plt.title(titulo)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
 
    plt.savefig(f"graficas/parte_3/{nombre_archivo}", dpi=300)
    plt.show()

# Ejecución 
 
def main():
    """
    Ejecuta toda la Parte 3.
    """
 
    # Crear carpetas de salida si no existen
    os.makedirs("tablas/parte_3", exist_ok=True)
    os.makedirs("graficas/parte_3", exist_ok=True)
 
    # Mostrar más decimales en pantalla
    pd.options.display.float_format = "{:.10f}".format
 
    # Rangos pedidos en la consigna
    N_10_100, N_100_1000, N_1000_10000 = obtener_rangos_N()
 
    # Generar tablas por rango
    tabla_10_100      = generar_tabla(N_10_100)
    tabla_100_1000    = generar_tabla(N_100_1000)
    tabla_1000_10000  = generar_tabla(N_1000_10000)
 
    # Tabla con todos los N (sin repetidos)
    N_todos = sorted(set(list(N_10_100) + list(N_100_1000) + list(N_1000_10000)))
    tabla_todos = generar_tabla(N_todos)
 
    # Guardar CSVs
    tabla_10_100.to_csv("tablas/parte_3/parte_3_tabla_N_10_100.csv", index=False, float_format="%.6f")
    tabla_100_1000.to_csv("tablas/parte_3/parte_3_tabla_N_100_1000.csv", index=False, float_format="%.6f")
    tabla_1000_10000.to_csv("tablas/parte_3/parte_3_tabla_N_1000_10000.csv", index=False, float_format="%.6f")
 
    # Imprimir tablas en consola
    print("\nTabla 1: N de 10 a 100\n")
    print(tabla_10_100.to_string())
 
    print("\nTabla 2: N de 100 a 1000\n")
    print(tabla_100_1000.to_string())
 
    print("\nTabla 3: N de 1000 a 10000\n")
    print(tabla_1000_10000.to_string())
 
    # Gráfica general (todos los N)
    graficar_metodos(
        tabla_todos,
        "Comparación de métodos de integración numérica",
        "parte_3_metodos_todos_N.png",
    )
 
    # Gráficas por rango
    graficar_metodos(
        tabla_10_100,
        "Comparación de métodos para N de 10 a 100",
        "parte_3_metodos_N_10_100.png",
    )
 
    graficar_metodos(
        tabla_100_1000,
        "Comparación de métodos para N de 100 a 1000",
        "parte_3_metodos_N_100_1000.png",
    )
 
    graficar_metodos(
        tabla_1000_10000,
        "Comparación de métodos para N de 1000 a 10000",
        "parte_3_metodos_N_1000_10000.png",
    )
 
    # Gráfica de residuos
    graficar_residuos(
        tabla_todos,
        "Residuos de los métodos de integración numérica",
        "parte_3_residuos.png",
    )
 
    # Prueba rápida con valores representativos
    print("\nPrueba rápida:\n")
    for N in [10, 100, 1000, 10000]:
        rect  = metodo_rectangulos(N)
        trap  = metodo_trapecio(N)
        medio = metodo_punto_medio(N)
        print(f"N = {N}")
        print(f"  Rectángulos: {rect:.10f}  (residuo: {residuo(rect):+.2e})")
        print(f"  Trapecio:    {trap:.10f}  (residuo: {residuo(trap):+.2e})")
        print(f"  Punto medio: {medio:.10f}  (residuo: {residuo(medio):+.2e})")
        print(f"  π teórico:   {PI_TEORICO:.10f}")
        print()
 
 
if __name__ == "__main__":
    main()