from simpleai.search import (
    CspProblem,
    backtrack,
    MOST_CONSTRAINED_VARIABLE,
    HIGHEST_DEGREE_VARIABLE,
    LEAST_CONSTRAINING_VALUE,
)
from itertools import combinations

def armar_tablero(filas, columnas, pisos, salida, piezas, pieza_sacar):
    
    variables = [ pieza[0] for pieza in piezas]
    dominios = { pieza: list(combinations((range(0,pisos), range(0,filas), range(0, columnas)),3))
                for pieza in piezas} #Van a ser las combinaciones de piso, filas y columnas
    
    restricciones = []
    
    # Van todos los for para agregar las restricciones
    
    return CspProblem(variables, dominios, restricciones)

def piezaDentroTablero(variable, value):
    # Las piezas tienen que estar dentro del tablero
    pass

def piezaSuperiorIzquierda(variable, value):
    # Por cada pieza se indique la coordenada (piso, fila, columna) de su casillero superior izquierdo.
    pass

def piezaCasilleroSalida(variable, value):
    # No debe haber ninguna pieza en el casillero de salida.
    pass

def piezaSuperpuesta(variable, value):
    # Las piezas claramente no deben estar superpuestas entre si.
    pass

def doblePiezasPisos(variable, value):
    # Ningún piso tiene que tener más del doble de piezas que ningún otro piso 
    # (por ejemplo, si un piso tiene 2 piezas, otro piso puede tener 4 piezas, 
    # pero ya no puede tener 8 piezas).
    pass

def casillerosPiezasPisos(variable, value):
    # La cantidad de casilleros que ocupan las piezas de un piso, no puede ser 
    # mayor a dos tercios de los casilleros de ese piso (por ejemplo, en un piso 
    # de 3x4, es decir, 12 casilleros, la suma de los casilleros ocupados con 
    # piezas en ese piso puede ser de hasta 8 casilleros, pero ya no 9 casilleros).
    pass

def pisosOcupados(variable, value):
    # Todos los pisos tienen que tener piezas.
    pass

def piezaSacarSalida(variable, value):
    # La pieza a sacar no tiene que estar en el mismo piso que el casillero de salida.
    pass