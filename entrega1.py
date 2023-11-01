from simpleai.search import (
    SearchProblem,
    astar,
)

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
        for pieza in state:
            if pieza[0] == self.pieza_sacar:
                piezaASacar = pieza
                break

        for parte in piezaASacar[2]:
            distancia = self.distance(parte[0], parte[1])
            distancias.append(distancia)

        distancia_minima = min(distancias)
        diferencia_piso = abs(self.salida[0] - piezaASacar[1])

        return distancia_minima + diferencia_piso


def jugar(filas, columnas, pisos, salida, piezas, pieza_sacar):

    my_problem = RushHour3D(filas, columnas, pisos, salida, piezas, pieza_sacar);
    result = astar(my_problem)
    listaActions= []
    for accion, result in result.path():
        if accion is not None:
            listaActions.append(accion)
    return listaActions