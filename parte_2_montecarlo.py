"""
parte_2_montecarlo.py

Parte 2: Método de Montecarlo para la integración.

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