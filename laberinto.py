import random

#tamaño del mapa

tamaño = 8

#simbolos esto (esto es para no andar escribiendo "." todo el tiempo)

vacio = "⬛"
pared = "⬜"
raton = "🐭"
gato = "🐱"
queso = "🧀"

#movimientos

movimientos = {
    "w":(-1, 0),
    "s":(1, 0),
    "a":(0, -1),
    "d":(0, 1)
}

#creo el tablero vacio

def crear_tablero():
 return [[vacio for _ in range(tamaño)] for _ in range(tamaño)]

def dibujar_tablero(tablero):
    print()
    for fila in tablero:
        print(" ".join(fila))
    print()

# paredes aleatorias
def generar_paredes_aleatorias(num_paredes=10):
     paredes = set()

     while len(paredes) < num_paredes:
        x = random.randint(0, tamaño - 1)
        y = random.randint(0, tamaño - 1)
        # evitar colocar sobre raton, gato o queso
        if (x, y) not in [(6,0), (0,6), (6,6)]:
            paredes.add((x,y))
     return paredes


def colocar_elementos(tablero, aleatorio=True):
    raton_pos = (6, 0)
    gato_pos = (0, 6)
    queso_pos = (6, 6)

    paredes = generar_paredes_aleatorias() if aleatorio else {
        (1,1), (1,2), (1,3),
        (3,1), (3,2), (3,3),
        (4,1), (5,1)
    }

    for x, y in paredes:
        tablero[x][y] = pared

    tablero[raton_pos[0]][raton_pos[1]] = raton
    tablero[gato_pos[0]][gato_pos[1]] = gato
    tablero[queso_pos[0]][queso_pos[1]] = queso

    return raton_pos, gato_pos, queso_pos, paredes

# movimientos posibles

def dentro_del_mapa(pos, paredes):
    x, y = pos
    if x < 0 or x >= tamaño or y < 0 or y >= tamaño or pos in paredes:
        return False
    return True

#mover al jugador

def mover_jugador(tablero, pos, simbolo, paredes, queso_pos):
    tecla = input("> ").lower()
    if tecla not in movimientos:
        return pos

    dx, dy = movimientos[tecla]
    nuevo = (pos[0] + dx, pos[1] + dy)

    if not dentro_del_mapa(nuevo, paredes):
        print("Movimiento invalido")
        return pos

    tablero[pos[0]][pos[1]] = queso if pos == queso_pos else vacio
    tablero[nuevo[0]][nuevo[1]] = simbolo
    return nuevo

#selector de personajes

def elegir_personaje():
    print("Elegi tu personaje:")
    print("1- Raton")
    print("2- Gato")

    opcion = input("> ")

    if opcion == "1":
        return "raton"

    elif opcion == "2":
        return "gato"

    else:
        print("Opcion invalida, sos raton por defecto")
        return "raton"

# Movimientos del contrincante

def mover_ia_minimax(jugador, raton_pos, gato_pos, queso_pos, paredes, profundidad=3):
    mejor_valor = -9999
    mejor_mov = gato_pos if jugador == "gato" else raton_pos
    pos_actual = gato_pos if jugador == "gato" else raton_pos

    for mov in generar_movimientos(pos_actual, paredes):
        if jugador == "gato":
            valor = minimax(raton_pos, mov, queso_pos, paredes, profundidad, False, jugador)
        else:
            valor = minimax(mov, gato_pos, queso_pos, paredes, profundidad, False, jugador)
        if valor > mejor_valor:
            mejor_valor = valor
            mejor_mov = mov

    return mejor_mov


#generar movimientos (Minimax)

def generar_movimientos(pos, paredes):
    posibles = []

    for dx, dy in movimientos.values():
        nx = pos[0] + dx
        ny = pos[1] + dy
        nuevo = (nx, ny)

        if dentro_del_mapa(nuevo, paredes):
            posibles.append(nuevo)

    return posibles


def evaluar_estado(raton_pos, gato_pos, queso_pos):

    # gato gana
    if raton_pos == gato_pos:
        return 100

    # ratón gana
    if raton_pos == queso_pos:
        return -100

    # heurística: distancias
    dist_gato = abs(raton_pos[0] - gato_pos[0]) + abs(raton_pos[1] - gato_pos[1])
    dist_queso = abs(raton_pos[0] - queso_pos[0]) + abs(raton_pos[1] - queso_pos[1])

    return dist_gato - dist_queso

#minimax

def minimax(raton_pos, gato_pos, queso_pos, paredes, profundidad, es_max, jugador):
    # Terminales
    if raton_pos == gato_pos:  # gato gana
        return 100 if jugador == "gato" else -100
    if raton_pos == queso_pos:  # ratón gana
        return 100 if jugador == "raton" else -100
    if profundidad == 0:
        # heurística
        dist_gato = abs(raton_pos[0] - gato_pos[0]) + abs(raton_pos[1] - gato_pos[1])
        dist_queso = abs(raton_pos[0] - queso_pos[0]) + abs(raton_pos[1] - queso_pos[1])
        if jugador == "raton":
            return -dist_gato - dist_queso  # ratón quiere acercarse al queso y alejarse del gato
        else:
            return dist_gato - dist_queso  # gato quiere acercarse al ratón
       
    if es_max:  # turno del jugador actual
        mejor = -9999
        pos_actual = gato_pos if jugador == "gato" else raton_pos
        for mov in generar_movimientos(pos_actual, paredes):
            if jugador == "gato":
                valor = minimax(raton_pos, mov, queso_pos, paredes, profundidad-1, False, jugador)
            else:
                valor = minimax(mov, gato_pos, queso_pos, paredes, profundidad-1, False, jugador)
            mejor = max(mejor, valor)
        return mejor
    else:  # turno del oponente
        mejor = 9999
        if jugador == "gato":
            for mov in generar_movimientos(pos_actual, paredes):
                valor = minimax(mov, gato_pos, queso_pos, paredes, profundidad-1, True, jugador)
            else:
                valor = minimax(raton_pos, mov, queso_pos, paredes, profundidad-1, True, jugador)
            mejor = min(mejor, valor)
        return mejor


#Funcion controladora del minimax

# verificacion de fin del juego

def verificar_fin(raton_pos, gato_pos, queso_pos, jugador):
    if raton_pos == queso_pos:
        print("GANASTE! 🐭 Conseguiste el queso 🧀" if jugador=="raton" else "PERDISTE 😿 El ratón ganó")
        return True
    if raton_pos == gato_pos:
        print("GANASTE! 🐱 Atrapaste al ratón" if jugador=="gato" else "PERDISTE 💀 El gato te atrapó")
        return True
    return False


#programa principal

def main():
    tablero = crear_tablero()
    raton_pos, gato_pos, queso_pos, paredes = colocar_elementos(tablero)
    jugador = elegir_personaje()

    while True:
        dibujar_tablero(tablero)

        if jugador == "raton":
            # Turno del jugador (ratón)
            raton_pos = mover_jugador(tablero, raton_pos, raton, paredes, queso_pos)
            if verificar_fin(raton_pos, gato_pos, queso_pos, jugador):
                dibujar_tablero(tablero)
                break

            # Turno del gato (IA con Minimax)
            gato_pos = mover_ia_minimax("gato", raton_pos, gato_pos, queso_pos, paredes, profundidad=3)
            tablero[gato_pos[0]][gato_pos[1]] = gato
            tablero[raton_pos[0]][raton_pos[1]] = raton  # para mantener símbolos correctos
            if verificar_fin(raton_pos, gato_pos, queso_pos, jugador):
                dibujar_tablero(tablero)
                break

        else:
            # Turno del jugador (gato)
            gato_pos = mover_jugador(tablero, gato_pos, gato, paredes, queso_pos)
            if verificar_fin(raton_pos, gato_pos, queso_pos, jugador):
                dibujar_tablero(tablero)
                break

            # Turno del ratón (IA con Minimax)
            raton_pos = mover_ia_minimax("raton", raton_pos, gato_pos, queso_pos, paredes, profundidad=3)
            tablero[raton_pos[0]][raton_pos[1]] = raton
            tablero[gato_pos[0]][gato_pos[1]] = gato
            if verificar_fin(raton_pos, gato_pos, queso_pos, jugador):
                dibujar_tablero(tablero)
                break



if __name__ == "__main__":
    main()
