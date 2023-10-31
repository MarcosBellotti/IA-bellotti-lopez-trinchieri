from simpleai.search import (
    CspProblem,
    backtrack,
    MOST_CONSTRAINED_VARIABLE,
    HIGHEST_DEGREE_VARIABLE,
    LEAST_CONSTRAINING_VALUE,
)
from itertools import combinations

FORMAS = {
    'L': ((0,0), (1,0), (1,1)),
    'T': ((0,0), (0,1), (0,2), (1,1)),
    'O': ((0,0), (0,1), (1,1), (1,0)),
    'I': ((0,0), (1,0), (2,0)),
    '-': ((0,0), (0,1), (0,2)),
    'Z': ((0,0), (0,1), (1,1), (1,2)),
    '.': ((0,0)),
}

def armar_tablero(filas, columnas, pisos, salida, piezas, pieza_sacar):
    
    variables = [ pieza[0] for pieza in piezas]
    dominios = { pieza: list(combinations((range(0,pisos), range(0,filas), range(0, columnas)),3))
                for pieza in piezas} #Van a ser las combinaciones de piso, filas y columnas
    
    restricciones = []
    
    # Funciones
    
    def piezaDentroTablero(variable, value):
    # Las piezas tienen que estar dentro del tablero, y que toda la forma este dentro del tablero
    
        piso, fila, columna = value
        id_pieza = variable
        forma = [pieza[1] for pieza in piezas if pieza[0] == id_pieza]
        
        pieza_forma = FORMAS[forma]
        
        for parte in pieza_forma:
            
            nueva_x, nueva_y = parte[0] + fila, parte[1] + columna
            
            if not (0 < nueva_x < fila and 0 < nueva_y < columna):
                return False
        
        return True
    
    def piezaCasilleroSalida(variable, value):
    # No debe haber ninguna pieza en el casillero de salida.
        piso, fila, columna = value
        id_pieza = variable
        forma = [pieza[1] for pieza in piezas if pieza[0] == id_pieza]
        
        pieza_forma = FORMAS[forma]
        
        for parte in pieza_forma:
            
            nueva_x, nueva_y = parte[0] + fila, parte[1] + columna
            
            if (piso == salida[0] and nueva_x == salida[1] and nueva_y == salida[2]):
                return False

        return True
    
    def doblePiezasPisos(variables, values):
    # Ningún piso tiene que tener más del doble de piezas que ningún otro piso 
    # (por ejemplo, si un piso tiene 2 piezas, otro piso puede tener 4 piezas, 
    # pero ya no puede tener 8 piezas).
    
        cont_pisos = [0] * pisos #Inicializamos el contador en 0
    
        for i in range(0,pisos):
            for value in values:
                if value[0] == i:
                    cont_pisos[i] += 1
        
        for piso in cont_pisos - 1:
            for piso2 in cont_pisos:
                if not piso <= piso2 * 2:
                    return False
        return True
    
    # Van todos los for para agregar las restricciones
    
    for variable in variables:
        restricciones.append((variable, piezaDentroTablero))
        restricciones.append((variable, piezaCasilleroSalida))
        
    restricciones.append((variables, doblePiezasPisos))
        
    
    return CspProblem(variables, dominios, restricciones)


def piezaSuperpuesta(variable, value):
    # Las piezas claramente no deben estar superpuestas entre si.
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