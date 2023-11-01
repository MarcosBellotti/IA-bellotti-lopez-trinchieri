from simpleai.search import (
    CspProblem,
    min_conflicts,
)
from itertools import combinations

FORMAS = {
    'L': ((0,0), (1,0), (1,1)),
    'T': ((0,0), (0,1), (0,2), (1,1)),
    'O': ((0,0), (0,1), (1,1), (1,0)),
    'I': ((0,0), (1,0), (2,0)),
    '-': ((0,0), (0,1), (0,2)),
    'Z': ((0,0), (0,1), (1,1), (1,2)),
    '.': ((0,0), ),
}

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

    def piezaNoEstaEnCasilleroSalida(variables, values):
        piso, fila, columna = values[0]
        id_pieza = variables[0]

        if piso == salida[0]:
            pieza_forma = FORMAS[next(pieza[1] for pieza in piezas if pieza[0] == id_pieza)]              
            
            for parte in pieza_forma:
                nueva_fila, nueva_col = parte[0] + fila, parte[1] + columna
                
                if (nueva_fila == salida[1] and nueva_col == salida[2]):
                    return False
        return True

    def piezaSacarDiferentePisoDeSalida(variables, values):
        return values[0][0] != salida[0]
    
    def ningunaPiezaSuperpuesta(variables, values):
        pieza1, pieza2 = values
        id_pieza1, id_pieza2 = variables

        piso1, fila1, columna1 = pieza1
        piso2, fila2, columna2 = pieza2

        if piso1 == piso2:        
            pieza1_forma = FORMAS[next(pieza[1] for pieza in piezas if pieza[0] == id_pieza1)]
            partes1 = [(parte[0] + fila1, parte[1] + columna1) for parte in pieza1_forma]

            pieza2_forma = FORMAS[next(pieza[1] for pieza in piezas if pieza[0] == id_pieza2)]
            partes2 = [(parte[0] + fila2, parte[1] + columna2) for parte in pieza2_forma]

            if any(parte in partes2 for parte in partes1):
                return False
        return True

    def ningunPisoTieneElDobleDePiezas(variables, values):    
        cont_pisos = [0] * pisos

        for value in values:
            cont_pisos[value[0]] += 1
        
        min_piezas = min(cont_pisos)
        for piso in cont_pisos:
            if piso > 2 * min_piezas:
                return False 
        return True

    def cantidadDeCasillerosOcupadosNoSuperaDosTercios(variables, values):       
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

    restricciones = []

    for variable in variables:
        restricciones.append(([variable], piezaNoEstaEnCasilleroSalida))
        if variable == pieza_sacar:
            restricciones.append(([variable], piezaSacarDiferentePisoDeSalida))

    for var1, var2 in combinations(variables, 2):
        restricciones.append(((var1,var2), ningunaPiezaSuperpuesta))
    
    restricciones.append((variables, ningunPisoTieneElDobleDePiezas))
    restricciones.append((variables, todosLosPisosOcupados))
    restricciones.append((variables, cantidadDeCasillerosOcupadosNoSuperaDosTercios))

    solucion = min_conflicts(CspProblem(variables, dominios, restricciones))
    return solucion
