#tamaño del mapa

tamaño = 7

#simbolos esto (esto es para no andar escribiendo "." todo el tiempo)

vacio = "."
pared = "#"
raton = "R"
gato = "G"
queso = "Q"

#creo el tablero vacio

def crear_tablero():
    tablero=[]

    for i in range (tamaño):
        fila = []

        for j in range(tamaño):
            fila.append(vacio)

        tablero.append(fila)
    return tablero

def dibujar_tablero(tablero):
    
    print()

    for fila in tablero:
        print(" ".join(fila))
    print()

#colocamos personajes

def colocar_elementos(tablero):

    raton_pos = (6, 0)
    gato_pos = (0, 6)
    queso_pos = (6, 6)

    paredes= {
        (1,1), (1,2), (1,3),
        (3,1), (3,2), (3,3),
        (4,1), (5,1)
    }

#paredes
    for x, y in paredes:
        tablero[x][y] = pared

#personajes
    tablero[raton_pos[0]][raton_pos[1]] = raton
    tablero[gato_pos[0]][gato_pos[1]] = gato
    tablero[queso_pos[0]][queso_pos[1]] = queso

    return raton_pos, gato_pos, queso_pos, paredes

#movimientos

movimientos = {
    "w":(-1, 0),
    "s":(1, 0),
    "a":(0, -1),
    "d":(0, 1)
}

#validacion de posiciones

def dentro_del_mapa(pos, paredes):
    x, y = pos

    if x < 0 or x >= tamaño:
        return False
    elif y < 0 or y >= tamaño:
        return False
    elif pos in paredes:
        return False
    return True

#mover al raton

def mover_raton(tablero, raton_pos, paredes):

    print("Mover con WASD:")
    tecla = input("> ").lower()

    if tecla not in movimientos:
        return raton_pos
    
    dx, dy = movimientos[tecla]

    nuevo = (
        raton_pos[0] + dx,
        raton_pos[1] + dy

    )

    if not dentro_del_mapa(nuevo, paredes):
        print("movimiento invalido")
        return raton_pos
    
    #limpiar vieja posicion
    tablero[raton_pos[0]][raton_pos[1]] = vacio

    #nueva posicion
    tablero[nuevo[0]][nuevo[1]] = raton
    return nuevo

#programa principal

def main():
    tablero = crear_tablero()

    raton_pos, gato_pos, queso_pos, paredes = colocar_elementos(tablero)

    while True:
        dibujar_tablero(tablero)
        raton_pos = mover_raton(tablero, raton_pos, paredes)

if __name__ == "__main__":
    main()
