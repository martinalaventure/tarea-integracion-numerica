"""
funciones_comunes.py

Funciones y constantes comunes para la tarea de integración numérica.
"""

import numpy as np


# Intervalo de integración
A = -1
B = 1

# Valor teórico de comparación
PI_TEORICO = np.pi


def f(x):
    """
    Función a integrar:

        f(x) = 2 * sqrt(1 - x^2)

    Representa la semicircunferencia superior de radio 1 multiplicada por 2.
    La integral en [-1, 1] vale pi.
    """
    return 2 * np.sqrt(np.maximum(0, 1 - x**2))


def residuo(aproximacion):
    """
    Calcula el residuo entre una aproximación numérica y el valor teórico pi.

    Residuo = aproximación - pi
    """
    return aproximacion - PI_TEORICO


def error_absoluto(aproximacion):
    """
    Calcula el error absoluto entre una aproximación numérica y pi.
    """
    return abs(aproximacion - PI_TEORICO)


def obtener_rangos_N():
    """
    Devuelve los tres rangos de N pedidos en la consigna.

    En este proyecto tomamos N como cantidad de subintervalos.
    Por lo tanto, cada partición tiene N + 1 puntos.
    """
    N_10_100 = range(10, 101, 10)
    N_100_1000 = range(100, 1001, 100)
    N_1000_10000 = range(1000, 10001, 1000)

    return N_10_100, N_100_1000, N_1000_10000