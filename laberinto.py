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

    paredes = {
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

#programa principal

def main():
    tablero = crear_tablero()

    raton, gato, queso, pared = colocar_elementos(tablero)

    dibujar_tablero(tablero)

if __name__ == "__main__":
    main()
