from simpleai.search import (
    SearchProblem,
    breadth_first,
    uniform_cost,
    depth_first,
    limited_depth_first,
    iterative_limited_depth_first,
    greedy,
    astar,
)
from simpleai.search.viewers import BaseViewer, WebViewer


class RushHour3D(SearchProblem):  
    
    def __init__(self, filas, columnas, pisos, salida, piezas, pieza_sacar):
        self.filas=filas
        self.columnas= columnas
        self.pisos= pisos
        self.salida = salida
        self.state = tuple((pieza["id"], pieza["piso"], tuple(pieza["partes"])) for pieza in piezas)
        self.pieza_sacar = pieza_sacar

        super().__init__(self.state)

    # Pasamos la posicion modificada
    def puedoMovermeEn2D(self, id, partes, piso, state):

        for pieza in state:
            if pieza[1] == piso and id != pieza[0]:
                for parte_de_otra_pieza in pieza[2]:
                        if parte_de_otra_pieza in partes:
                            return False
        return True


    def actions(self, state):
        available_actions = []

        for pieza in state:
            id = pieza[0]
            piso = pieza[1]
            partes = pieza[2]

            # CAER
            if piso > 0:
                if self.puedoMovermeEn2D(id, partes, piso-1, state):  
                    available_actions.append((id, "caer"))

            # TREPAR         
            if piso < self.pisos-1:
                if self.puedoMovermeEn2D(id, partes, piso+1, state):  
                    available_actions.append((id, "trepar"))


            # ARRIBA
            if all(parte[0] > 0 for parte in partes):
                nuevasPartes = [(fil-1, col) for fil, col in partes]

                if self.puedoMovermeEn2D(id, nuevasPartes, piso, state):  
                    available_actions.append((id, "arriba"))

            # ABAJO
            if all(parte[0] < self.filas-1 for parte in partes):
                nuevasPartes = [(fil+1, col) for fil, col in partes]
                    
                if self.puedoMovermeEn2D(id, nuevasPartes, piso, state):                
                    available_actions.append((id, "abajo"))

            # IZQUIERDA
            if all(parte[1] > 0 for parte in partes):
                nuevasPartes = [(fil, col - 1) for fil, col in partes]
                    
                if self.puedoMovermeEn2D(id, nuevasPartes, piso, state):               
                    available_actions.append((id, "izquierda"))

            # DERECHA
            if all(parte[1] < self.columnas - 1 for parte in partes):
                nuevasPartes = [(fil, col + 1) for fil, col in partes]
                    
                if self.puedoMovermeEn2D(id, nuevasPartes, piso, state):               
                    available_actions.append((id, "derecha"))

        return available_actions
    
    def result(self, state, action):

        MOVIMIENTOS = {"arriba": (-1,0),
                       "abajo": (+1,0),
                       "izquierda": (0,-1),
                       "derecha": (0,+1)}
        
        # aca directamente veríamos que accion tenemos en available_actions y solo sumamos o restamos posiciones     
        id, accion = action
        state = list(state)
        nuestraPieza = None

        # obtengo la pieza que tiene mi id
        for pieza in state:
            if pieza[0] == id:
                nuestraPieza = pieza
                break
        
        state.remove(nuestraPieza)
        nuestraPieza=list(nuestraPieza)

        if accion == "trepar":
            nuestraPieza[1]= nuestraPieza[1]+1
            
        else:
            if accion == "caer":
                nuestraPieza[1]=nuestraPieza[1]-1

            else:
                nFil, nCol = MOVIMIENTOS[accion]
                nuevasPartes = []

                for parteVieja in nuestraPieza[2]:
                    fil, col = parteVieja
                    nuevaParte= (fil + nFil, col+nCol)
                    nuevasPartes.append(nuevaParte)

                nuestraPieza[2] = tuple(nuevasPartes) 

        nuestraPieza = tuple(nuestraPieza)
        state.append(nuestraPieza)
        return tuple(state)
    

    def cost(self, state, action, state2):
        return 1
    

    def is_goal(self, state):
        # La idea es ver que el piso sea igual a la salida, y si lo es, 
        # fijarnos si alguna parte de la pieza esta en la posicion que hace terminar el juego
        for pieza in state:
            id = pieza[0]
            piso = pieza[1]
            partes = pieza[2]

            if id == self.pieza_sacar:
                if(piso == self.salida[0]):
                    for parte in partes:
                        if(parte[0] == self.salida[1] and parte[1] == self.salida[2]):
                            return True
        return False
    
    def distance(self, x, y):
        return abs(x - self.salida[1]) + abs(y - self.salida[2])

    def heuristic(self, state):
        distancias=[]
        # total calcula la distancia de la parte mas cercana a la posicion final
        # obtengo la pieza que tiene mi id
        for pieza in state:
            if pieza[0] == self.pieza_sacar:
                piezaASacar = pieza
                break

        for parte in piezaASacar[2]:
            distancia = self.distance(parte[0], parte[1])
            distancias.append(distancia)

        # Calcula la distancia mínima entre todas las distancias recopiladas.
        distancia_minima = min(distancias)

        # Calcula la diferencia entre el piso actual y el piso deseado.
        diferencia_piso = abs(self.salida[0] - piezaASacar[1])

        # Suma la distancia mínima y la diferencia de piso a la heurística total.
        heuristica_total = distancia_minima + diferencia_piso

        return heuristica_total


def jugar(filas, columnas, pisos, salida, piezas, pieza_sacar):

    my_problem = RushHour3D(filas, columnas, pisos, salida, piezas, pieza_sacar);
    result = astar(my_problem)
    listaActions= []
    for accion, result in result.path():
        if accion is not None:
            listaActions.append(accion)
    return listaActions
    

# if __name__ == '__main__':
#     my_problem = RushHour3D(filas=2, columnas=3,
#     pisos=2,
#     salida=(0, 0, 0),  
#     piezas=[
#         # {"id": "E", "piso": 2, "partes": [(0, 3), (1, 2), (1, 3), (2, 2)]},
#         # {"id": "A", "piso": 2, "partes": [(1, 0), (2, 0), (2, 1)]},
#         # {"id": "C", "piso": 1, "partes": [(0, 1), (1, 1), (2, 1)]},
#         # {"id": "D", "piso": 1, "partes": [(2, 2), (2, 3)]},
#         # {"id": "B", "piso": 0, "partes": [(1, 0), (0, 0), (0, 1), (1, 1)]},
#         # {"id": "F", "piso": 0, "partes": [(0, 2), (0, 3)]},

#         # Ejemplo 7,6,10
#         {"id": "A", "piso": 1, "partes": [(1, 1), (1, 2)]},
#         {"id": "C", "piso": 0, "partes": [(0, 1)]},
#         {"id": "D", "piso": 0, "partes": [(0, 0), (0, 1)]},
#         {"id": "B", "piso": 1, "partes": [(0, 0), (0, 1)]},

#     ],
#     pieza_sacar="A",)

#     result = astar(my_problem)

#     if result is None:
#         print("No solution")
#     else:
#         for action, resultado in result.path():
#             print("A:", action)
#             # print("R:", resulta)

#         print("Final depth:", len(result.path()))
#         print("Final cost:", result.cost)


