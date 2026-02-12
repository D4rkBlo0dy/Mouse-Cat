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

def mover_jugador(tablero, pos, simbolo, paredes, queso_pos):

    tecla = input("> ").lower()
    if tecla not in movimientos:
        return pos

    dx, dy = movimientos[tecla]
    nuevo = (pos[0] + dx, pos[1] + dy)

    if not dentro_del_mapa(nuevo, paredes):
        print("Movimiento invalido")
        return pos

    # 1️⃣ Restaurar la casilla vieja si era queso
    if pos == queso_pos:
        tablero[pos[0]][pos[1]] = queso
    else:
        tablero[pos[0]][pos[1]] = vacio

    # 2️⃣ Dibujar el jugador en la nueva posición
    tablero[nuevo[0]][nuevo[1]] = simbolo

    return nuevo



# verificacion de fin del juego

def verificar_fin(raton_pos, gato_pos, queso_pos, jugador):

    # ratón llega al queso
    if raton_pos == queso_pos:

        if jugador == "raton":
            print("GANASTE! 🐭 Conseguiste el queso 🧀")
        else:
            print("PERDISTE 😿 El ratón ganó")

        return True


    # gato atrapa al ratón
    if raton_pos == gato_pos:

        if jugador == "gato":
            print("GANASTE! 🐱 Atrapaste al ratón")
        else:
            print("PERDISTE 💀 El gato te atrapó")

        return True


    return False


# Movimientos del Gato

def mover_gato(tablero, gato_pos, raton_pos, queso_pos, paredes):

    gx, gy = gato_pos
    rx, ry = raton_pos


    mejor_mov = gato_pos
    mejor_dist = 9999


    for dx, dy in movimientos.values():

        nx = gx + dx
        ny = gy + dy

        nuevo = (nx, ny)


        if not dentro_del_mapa(nuevo, paredes):
            continue


        # distancia Manhattan
        dist = abs(rx - nx) + abs(ry - ny)


        if dist < mejor_dist:
            mejor_dist = dist
            mejor_mov = nuevo

 #  Restaurar la casilla vieja del gato
    # si la posición vieja era donde estaba el queso, volver a poner Q
    if gato_pos == queso_pos:
        tablero[gx][gy] = queso
    else:
        tablero[gx][gy] = vacio

    #  Dibujar el gato en la nueva posición
    if mejor_mov == queso_pos:
        tablero[mejor_mov[0]][mejor_mov[1]] = gato  # el gato pisa la Q
        # el queso seguirá visible solo para la lógica, pero lo mostramos como gato
    else:
        tablero[mejor_mov[0]][mejor_mov[1]] = gato
 

    return mejor_mov

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

# Logica para que el raton se mueva

def mover_raton_ia(tablero, raton_pos, gato_pos, paredes, queso_pos):
    rx, ry = raton_pos
    mejor_pos = raton_pos
    mejor_puntaje = -9999  # queremos maximizar

    for dx, dy in movimientos.values():
        nx, ny = rx + dx, ry + dy
        nuevo = (nx, ny)

        # validar posición
        if not dentro_del_mapa(nuevo, paredes):
            continue

        # distancia al gato (queremos alejarlo)
        dist_gato = abs(nx - gato_pos[0]) + abs(ny - gato_pos[1])

        # distancia al queso (queremos acercarnos)
        dist_queso = abs(nx - queso_pos[0]) + abs(ny - queso_pos[1])

        # puntuación combinada: alejarse del gato y acercarse al queso
        puntaje = dist_gato - dist_queso  # mientras más grande, mejor

        if puntaje > mejor_puntaje:
            mejor_puntaje = puntaje
            mejor_pos = nuevo

    # limpiar la casilla vieja
    if raton_pos == queso_pos:
        tablero[rx][ry] = queso
    else:
        tablero[rx][ry] = vacio

    # colocar ratón en nueva posición
    tablero[mejor_pos[0]][mejor_pos[1]] = raton

    return mejor_pos


#programa principal

def main():

    tablero = crear_tablero()
    raton_pos, gato_pos, queso_pos, paredes = colocar_elementos(tablero)
    jugador = elegir_personaje()

    while True:

        dibujar_tablero(tablero)

        if jugador == "raton":

            # mueve el ratón (jugador)
            raton_pos = mover_jugador(
                tablero,
                raton_pos,
                raton,
                paredes,
                queso_pos
            )

            # mueve el gato (IA)
            gato_pos = mover_gato(
                tablero,
                gato_pos,
                raton_pos,
                queso_pos,
                paredes
            )

        else:

            # mueve el gato (jugador)
            gato_pos = mover_jugador(
                tablero,
                gato_pos,
                gato,
                paredes,
                queso_pos
            )

            # IA del ratón intenta escapar y llegar al queso
            raton_pos = mover_raton_ia(tablero, raton_pos, gato_pos, paredes, queso_pos)


        if verificar_fin(raton_pos, gato_pos, queso_pos, jugador):
            dibujar_tablero(tablero)
            break


if __name__ == "__main__":
    main()
