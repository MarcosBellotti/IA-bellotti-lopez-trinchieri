from simpleai.search import (
    CspProblem,
    backtrack,
    min_conflicts,
    MOST_CONSTRAINED_VARIABLE,
    HIGHEST_DEGREE_VARIABLE,
    LEAST_CONSTRAINING_VALUE,
)
from itertools import combinations, product

FORMAS = {
    'L': ((0,0), (1,0), (1,1)),
    'T': ((0,0), (0,1), (0,2), (1,1)),
    'O': ((0,0), (0,1), (1,1), (1,0)),
    'I': ((0,0), (1,0), (2,0)),
    '-': ((0,0), (0,1), (0,2)),
    'Z': ((0,0), (0,1), (1,1), (1,2)),
    '.': ((0,0), ),
}

def calcular_coordenadas_maximas(forma_pieza, filas, columnas):
    coordenadas_maximas = set()
    for parte in forma_pieza:
        x_max = filas - parte[0]
        y_max = columnas - parte[1]
        coordenadas_maximas.add((x_max, y_max))
    return coordenadas_maximas


def armar_tablero(filas, columnas, pisos, salida, piezas, pieza_sacar):
    
    variables = [ pieza[0] for pieza in piezas]
    dominios = {variable: [] for variable in variables}

    # generar el dominio solo las posiciones que dejan a la pieza dentro del tablero
    for variable in variables:
        for piso in range(pisos):
            for fila in range(filas):
                for columna in range(columnas):
                    forma_pieza = FORMAS[next(p[1] for p in piezas if p[0] == variable)]

                    max_fila = max(part[0] for part in forma_pieza)
                    max_col =  max(part[1] for part in forma_pieza)
                    
                    if fila + max_fila < filas and columna + max_col < columnas:
                        dominios[variable].append((piso, fila, columna))

    # coordenadas_maximas_por_pieza = {}
    # for pieza in piezas:
    #     id_pieza = pieza[0]
    #     forma_pieza = FORMAS[pieza[1]]
    #     coordenadas_maximas = calcular_coordenadas_maximas(forma_pieza, filas, columnas)
    #     coordenadas_maximas_por_pieza[id_pieza] = coordenadas_maximas

    # for variable in variables:
    #     for piso, fila, columna in product(range(pisos), range(filas), range(columnas)):
    #         if all((fila, columna) < coordenada_maxima for coordenada_maxima in coordenadas_maximas_por_pieza[variable]):
    #             dominios[variable].append((piso, fila, columna))
    
    # dominios = {variable: list(product(range(pisos), range(filas), range(columnas)))
    #         for variable in variables} #Van a ser las combinaciones de piso, filas y columnas
    
    # # Funciones
    
    # def piezaDentroDelTablero(variables, values):
    # # Las piezas tienen que estar dentro del tablero, y que toda la forma este dentro del tablero
    #     piso, fila, columna = values[0]
    #     id_pieza = variables[0]

    #     forma = tuple([pieza[1] for pieza in piezas if pieza[0] == id_pieza])

    #     pieza_forma = FORMAS[forma[0]]  

    #     for parte in pieza_forma:
            
    #         nueva_x, nueva_y = parte[0] + fila, parte[1] + columna

    #         if not (0 < nueva_x < fila and 0 < nueva_y < columna):
    #             return False
    #     return True

    def piezaNoEstaEnCasilleroSalida(variables, values):
    # No debe haber ninguna pieza en el casillero de salida.
        piso, fila, columna = values[0]
        id_pieza = variables[0]

        if piso == salida[0]:
            pieza_forma = FORMAS[next(pieza[1] for pieza in piezas if pieza[0] == id_pieza)]              

            for parte in pieza_forma:
                nueva_x, nueva_y = parte[0] + fila, parte[1] + columna
                
                if (nueva_x == salida[1] and nueva_y == salida[2]):
                    return False
        return True

    def piezaSacarDiferentePisoDeSalida(variables, values):
        # La pieza a sacar no tiene que estar en el mismo piso que el casillero de salida.
        return values[0][0] != salida[0]
    
    def ningunaPiezaSuperpuesta(variables, values):
    # Las piezas claramente no deben estar superpuestas entre si.
        pieza1, pieza2 = values
        id_pieza1, id_pieza2 = variables

        piso1, fila1, columna1 = pieza1
        piso2, fila2, columna2 = pieza2

        if piso1 == piso2:        
            forma1 = tuple([pieza[1] for pieza in piezas if pieza[0] == id_pieza1])
            pieza1_forma = FORMAS[forma1[0]]
            partes1 = []
            for parte in pieza1_forma:       
                partes1.append((parte[0] + fila1, parte[1] + columna1))

            forma2 = tuple([pieza[1] for pieza in piezas if pieza[0] == id_pieza2])
            pieza2_forma = FORMAS[forma2[0]]
            partes2 = []
            for parte in pieza2_forma:               
                partes2.append((parte[0] + fila2, parte[1] + columna2))

            if any(parte in partes2 for parte in partes1):
                return False
        return True

    def ningunPisoTieneElDobleDePiezas(variables, values):
    # Ningún piso tiene que tener más del doble de piezas que ningún otro piso 
    # (por ejemplo, si un piso tiene 2 piezas, otro piso puede tener 4 piezas, 
    # pero ya no puede tener 8 piezas).            
        cont_pisos = [0] * pisos #Inicializamos el contador en 0
        # for i in range(pisos):
        #     for value in values:
        #         if value[0] == i:
        #             cont_pisos[i] += 1

        # for piso in cont_pisos - 1:
        #     for piso2 in cont_pisos:
        #         if not piso <= piso2 * 2:
        #             return False
        # return True

        for value in values:
            cont_pisos[value[0]] += 1
        
        min_piezas = min(cont_pisos)
        for piso in cont_pisos:
            if piso > 2 * min_piezas:
                return False 
        return True

    def cantidadDeCasillerosOcupadosNoSuperaDosTercios(variables, values):
        # La cantidad de casilleros que ocupan las piezas de un piso, no puede ser 
        # mayor a dos tercios de los casilleros de ese piso (por ejemplo, en un piso 
        # de 3x4, es decir, 12 casilleros, la suma de los casilleros ocupados con 
        # piezas en ese piso puede ser de hasta 8 casilleros, pero ya no 9 casilleros).
        
        cantidadCasilleros = filas*columnas

        for piso in range(pisos):
            cantidadOcupada = 0
            for i, v in enumerate(values):
                valor = values[i]
                if valor[0] == piso:
                    forma = tuple([pieza[1] for pieza in piezas if pieza[0] == variables[i]])
                    cantidadOcupada += len(FORMAS[forma[0]])
                    if cantidadOcupada > cantidadCasilleros*2/3:
                        return False

        return True

    def todosLosPisosOcupados(variables, values):
        # Todos los pisos tienen que tener piezas.
        cont_pisos = [0]*pisos
        for value in values:
            cont_pisos[value[0]] += 1
        return 0 not in cont_pisos

    # Van todos los for para agregar las restricciones
    
    restricciones = []
    # UNAREA
    for variable in variables:
        # restricciones.append(([variable], piezaDentroDelTablero))
        restricciones.append(([variable], piezaNoEstaEnCasilleroSalida))
        if variable == pieza_sacar:
            restricciones.append(([variable], piezaSacarDiferentePisoDeSalida))

    for var1, var2 in combinations(variables, 2):
        restricciones.append(((var1,var2), ningunaPiezaSuperpuesta))
    
    restricciones.append((variables, ningunPisoTieneElDobleDePiezas))
    restricciones.append((variables, todosLosPisosOcupados))
    restricciones.append((variables, cantidadDeCasillerosOcupadosNoSuperaDosTercios))

    solucion = min_conflicts(CspProblem(variables, dominios, restricciones))
    print("La solucion es: ", solucion)
    return solucion


armar_tablero(
    filas=5,
    columnas=5,
    pisos=2,
    salida=(0, 3, 1),  # piso 0, fila 3, columna 1 
    piezas=[
        # una lista de piezas presentes en el tablero, cada una con un id 
        # y una forma (expresada como un caracter, debajo se explican las formas
        # disponibles)
        ("pieza_verde", "L"),
        ("pieza_roja", "O"),
        ("pieza_azul", "T"),
        ("pieza_amarilla", "T"),
    ],
    pieza_sacar="pieza_roja",
)