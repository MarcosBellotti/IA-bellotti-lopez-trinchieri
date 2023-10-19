from itertools import combinations

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

def distance(parte, salida):
    
    return abs(parteMasCercana[0] - fila) + abs(parteMasCercana[1] - columna)

def obtenerDatosPieza(state):
    return state["piezas"]

class RushHour3D(SearchProblem):    
    # "arriba", "abajo", "izquierda", "derecha", "trepar", "caer"
    def actions(self, state):

        # ¿CÓMO ES EL STATE QUE TE LLEGA?
        
        id, piso, partes = state
        available_actions = []

        if(piso > 0):
            # ver que en el piso de abajo no haya piezas en ninguna de las posiciones
            available_actions.append("caer")

        if(piso < pisos-1): 
            # ver que en el piso de arriba no haya piezas en ninguna de las posiciones
            available_actions.append("trepar")

        if all(parte[0] > 0 for parte in partes):
            # ver que en la posicion de arriba no haya piezas en ninguna de las posiciones
            available_actions.append("arriba")

        if all(parte[0] < filas-1 for parte in partes):
            # ver que en la posicion de abajo no haya piezas en ninguna de las posiciones
            available_actions.append("abajo")

        if all(parte[1] > 0 for parte in partes):
            # ver que en la posicion izquierda no haya piezas en ninguna de las posiciones
            available_actions.append("izquierda")

        if all(parte[1] < columnas - 1 for parte in partes):
            # ver que en la posicion derecha no haya piezas en ninguna de las posiciones
            available_actions.append("derecha")

        return available_actions
    
    def result(self, state, action):
        # aca directamente veríamos que accion tenemos en available_actions y solo sumamos o restamos posiciones
        


        pass

    def cost(self, state, action, state2):
        return 1
    
    def is_goal(self, state):
        # La idea es ver que el piso sea igual a la salida, y si lo es, fijarnos si alguna parte de la pieza esta en la posicion que hace terminar el juego
        id, piso, partes = state
        if(piso == salida[0]):
            for parte in partes:
                if(parte[0] == salida[1] and parte[1] == salida[2]):
                    return id==pieza_sacar 

        return False
    
    def heuristic(self, state):
        # total calcula la distancia de la parte mas cercana a la posicion final

        # despues le sumamos la diferencia del piso en el que estamos con el que deberiamos eestar
        pass

if __name__ == '__main__':
    my_problem = RushHour3D()

    result = astar(my_problem)

    if result is None:
        print("No solution")
    else:
        for action, state in result.path():
            print("A:", action)

        print("Final depth:", len(result.path()))
        print("Final cost:", result.cost)


