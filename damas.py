
from automata.fa.dfa import DFA
from typing import Set, List, Tuple, Optional

tablero = [['-', 'n', '-', 'n', '-', 'n', '-', 'n'],
           ['n', '-', 'n', '-', 'n', '-', 'n', '-'],
           ['-', 'n', '-', 'n', '-', 'n', '-', 'n'],
           ['-', '-', '-', '-', '-', '-', '-', '-'],
           ['-', '-', '-', '-', '-', '-', '-', '-'],
           ['b', '-', 'b', '-', 'b', '-', 'b', '-'],
           ['-', 'b', '-', 'b', '-', 'b', '-', 'b'],
           ['b', '-', 'b', '-', 'b', '-', 'b', '-']]

letras = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7}
movimientoValido = True
jugador = 'n'
capturas_blanca_count: int = 0
capturas_negra_count: int = 0

def crear_automata_captura():
    return DFA(
        states={'inicio', 'ficha_propia', 'ficha_enemiga', 'captura_valida', 'invalido'},
        input_symbols={'P', 'E', 'V', 'O'},
        transitions={
            'inicio': {'P': 'ficha_propia', 'E': 'invalido', 'V': 'invalido', 'O': 'invalido'},
            'ficha_propia': {'P': 'invalido', 'E': 'ficha_enemiga', 'V': 'invalido', 'O': 'invalido'},
            'ficha_enemiga': {'P': 'invalido', 'E': 'invalido', 'V': 'captura_valida', 'O': 'invalido'},
            'captura_valida': {'P': 'invalido', 'E': 'invalido', 'V': 'invalido', 'O': 'invalido'},
            'invalido': {'P': 'invalido', 'E': 'invalido', 'V': 'invalido', 'O': 'invalido'}
        },
        initial_state='inicio',
        final_states={'captura_valida'}
    )
automata_captura = crear_automata_captura()
def moValido(jugada, colorJugador):
    if len(jugada) != 4:
        print('Formato incorrecto. Use formato: LetraNumeroLetraNumero (ej: A3B4)')
        return False
    if not jugada[0].isalpha():
        print('Formato incorrecto. Debe empezar con una letra (A-H)')
        return False
    if not jugada[2].isalpha():
        print('Formato incorrecto. El tercer caracter debe ser una letra (A-H)')
        return False
    if not jugada[1].isdigit():
        print('Formato incorrecto. El segundo caracter debe ser un número (1-8)')
        return False
    if not jugada[3].isdigit():
        print('Formato incorrecto. El cuarto caracter debe ser un número (1-8)')
        return False

    if jugada[0].upper() not in letras:
        print('la primera letra no esta en letras')
        return False

    elif int(jugada[1]) > 8 or int(jugada[1]) < 1:
        print('el primer numero no esta en el rango')
        return False

    elif jugada[2].upper() not in letras:
        print('la segunda letra no esta en letras')
        return False

    elif int(jugada[3]) > 8 or int(jugada[3]) < 1:
        print('el segundo numero no esta en el rango')
        return False
    movOriRow = 8 - int(jugada[1])
    movOriCol = letras[jugada[0].upper()]
    movDesRow = 8 - int(jugada[3])
    movDesCol = letras[jugada[2].upper()]
    if tablero[movOriRow][movOriCol] == '-':
        print('No hay ficha en la posición de origen')
        return False

    ficha = tablero[movOriRow][movOriCol]
    if ficha.lower() != colorJugador:
        print('No coincide con el turno del jugador')
        return False
    if tablero[movDesRow][movDesCol] != '-':
        print('La casilla destino no está vacía')
        return False
    if ficha.upper() == 'N' or ficha.upper() == 'B':
        numCasillas = abs(movOriCol - movDesCol)
        
        if numCasillas == abs(movOriRow - movDesRow):
            if numCasillas > 2:
                for i in range(1, numCasillas):
                    if movDesRow < movOriRow:
                        check_row = movOriRow - i
                    else:
                        check_row = movOriRow + i
                        
                    if movDesCol < movOriCol:
                        check_col = movOriCol - i
                    else:
                        check_col = movOriCol + i
                    
                    if tablero[check_row][check_col] != '-':
                        print('Hay obstáculos en el camino')
                        return False
            return True
        else:
            print('Las damas solo se mueven diagonalmente')
            return False
    else:
 
        if not ((abs(movDesRow - movOriRow) == 1 or abs(movDesRow - movOriRow) == 2) and 
                abs(movDesCol - movOriCol) == abs(movDesRow - movOriRow)):
            print('Las fichas solo se mueven diagonalmente 1 o 2 casillas')
            return False
        if ficha.islower(): 
            if abs(movDesRow - movOriRow) == 1:
                if ficha == 'n':
                    if movDesRow <= movOriRow:
                        print('Las fichas negras solo pueden moverse hacia adelante (hacia abajo)')
                        return False
                elif ficha == 'b':
                    if movDesRow >= movOriRow:
                        print('Las fichas blancas solo pueden moverse hacia adelante (hacia arriba)')
                        return False
            
            elif abs(movDesRow - movOriRow) == 2:
                if ficha == 'n':
                    if movDesRow <= movOriRow:
                        print('Las fichas negras solo pueden capturar hacia adelante (hacia abajo)')
                        return False
                elif ficha == 'b':
                    if movDesRow >= movOriRow:
                        print('Las fichas blancas solo pueden capturar hacia adelante (hacia arriba)')
                        return False
        
        return True

def validar_captura_con_automata(movOriRow: int, movOriCol: int, movDesRow: int, movDesCol: int, colorJugador: str) -> bool:
    """
    Valida una captura usando el autómata finito determinístico.
    Retorna True si la captura es válida según el autómata.
    Para damas (piezas coronadas), permite capturas en cualquier dirección.
    """
    ficha_origen = tablero[movOriRow][movOriCol]
    es_dama = ficha_origen.isupper()
 
    if es_dama:
        if abs(movDesRow - movOriRow) != abs(movDesCol - movOriCol):
            return False
        
        distancia = abs(movDesRow - movOriRow)
        if distancia < 2:
            return False
            
        dir_row = 1 if movDesRow > movOriRow else -1
        dir_col = 1 if movDesCol > movOriCol else -1
        
        fichas_enemigas_encontradas = 0
        ficha_enemiga_pos = None
        for i in range(1, distancia):
            check_row = movOriRow + (i * dir_row)
            check_col = movOriCol + (i * dir_col)
            ficha_en_camino = tablero[check_row][check_col]
            
            if ficha_en_camino != '-':
                if ficha_en_camino.lower() != colorJugador:
                    fichas_enemigas_encontradas += 1
                    ficha_enemiga_pos = (check_row, check_col)
                else:
                    return False
        
        if fichas_enemigas_encontradas != 1:
            return False
            
        return tablero[movDesRow][movDesCol] == '-'
    
    else:
        if abs(movDesRow - movOriRow) != 2 or abs(movDesCol - movOriCol) != 2:
            return False
    secuencia_simbolos = ""
    ficha_origen = tablero[movOriRow][movOriCol]
    if ficha_origen != '-' and ficha_origen.lower() == colorJugador:
        secuencia_simbolos += 'P'
    else:
        secuencia_simbolos += 'O'
 
    ficha_medio_row = (movOriRow + movDesRow) // 2
    ficha_medio_col = (movOriCol + movDesCol) // 2
    ficha_medio = tablero[ficha_medio_row][ficha_medio_col]
    
    if ficha_medio != '-' and ficha_medio.lower() != colorJugador:
        secuencia_simbolos += 'E'
    else:
        secuencia_simbolos += 'O'
 
    ficha_destino = tablero[movDesRow][movDesCol]
    if ficha_destino == '-':
        secuencia_simbolos += 'V'
    else:
        secuencia_simbolos += 'O'
 
    try:
        resultado = automata_captura.accepts_input(secuencia_simbolos)
        return resultado
    except Exception:
        return False

def obtener_capturas_multiples(movOriRow: int, movOriCol: int, colorJugador: str, fichas_capturadas: Set[Tuple[int, int]] = None) -> List[List[Tuple[int, int]]]:
    if fichas_capturadas is None:
        fichas_capturadas = set()
    
    capturas_posibles = []
    ficha_origen = tablero[movOriRow][movOriCol]
    es_dama = ficha_origen.isupper()
    direcciones = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    
    for dir_row, dir_col in direcciones:
        if es_dama:
            for distancia in range(2, 8):
                nuevaRow = movOriRow + (distancia * dir_row)
                nuevaCol = movOriCol + (distancia * dir_col)
                if not (0 <= nuevaRow < 8 and 0 <= nuevaCol < 8):
                    break
                if validar_captura_con_automata(movOriRow, movOriCol, nuevaRow, nuevaCol, colorJugador):
                    ficha_capturada_pos = None
                    for i in range(1, distancia):
                        check_row = movOriRow + (i * dir_row)
                        check_col = movOriCol + (i * dir_col)
                        ficha_check = tablero[check_row][check_col]
                        if ficha_check != '-' and ficha_check.lower() != colorJugador:
                            ficha_capturada_pos = (check_row, check_col)
                            break
                    
                    if ficha_capturada_pos and ficha_capturada_pos not in fichas_capturadas:
                        procesar_captura_temporal(movOriRow, movOriCol, nuevaRow, nuevaCol, 
                                                ficha_capturada_pos, colorJugador, fichas_capturadas, capturas_posibles)
                    if ficha_capturada_pos:
                        break
        else:

            ficha_origen = tablero[movOriRow][movOriCol]
            direccion_valida = True
            if ficha_origen == 'n':
                if dir_row <= 0:
                    direccion_valida = False
            elif ficha_origen == 'b':
                if dir_row >= 0:
                    direccion_valida = False
            
            if direccion_valida:
                deltaRow = dir_row * 2
                deltaCol = dir_col * 2
                nuevaRow = movOriRow + deltaRow
                nuevaCol = movOriCol + deltaCol
                if 0 <= nuevaRow < 8 and 0 <= nuevaCol < 8:
                    ficha_medio_row = movOriRow + dir_row
                    ficha_medio_col = movOriCol + dir_col
                    ficha_capturada_pos = (ficha_medio_row, ficha_medio_col)
                    
                    if ficha_capturada_pos not in fichas_capturadas:
                        if validar_captura_con_automata(movOriRow, movOriCol, nuevaRow, nuevaCol, colorJugador):
                            procesar_captura_temporal(movOriRow, movOriCol, nuevaRow, nuevaCol,
                                                    ficha_capturada_pos, colorJugador, fichas_capturadas, capturas_posibles)
    
    return finalizar_capturas_multiples(capturas_posibles)

def procesar_captura_temporal(movOriRow, movOriCol, nuevaRow, nuevaCol, ficha_capturada_pos, colorJugador, fichas_capturadas, capturas_posibles):

    ficha_medio_row, ficha_medio_col = ficha_capturada_pos
    ficha_original = tablero[movOriRow][movOriCol]
    ficha_capturada = tablero[ficha_medio_row][ficha_medio_col]
    ficha_destino_original = tablero[nuevaRow][nuevaCol]
    tablero[nuevaRow][nuevaCol] = ficha_original
    tablero[movOriRow][movOriCol] = '-'
    tablero[ficha_medio_row][ficha_medio_col] = '-'
    nuevas_fichas_capturadas = fichas_capturadas.copy()
    nuevas_fichas_capturadas.add((ficha_medio_row, ficha_medio_col))
    capturas_adicionales = obtener_capturas_multiples(nuevaRow, nuevaCol, colorJugador, nuevas_fichas_capturadas)
    
    if capturas_adicionales:
        for secuencia in capturas_adicionales:
            capturas_posibles.append([(movOriRow, movOriCol, nuevaRow, nuevaCol)] + secuencia)
    else:
        capturas_posibles.append([(movOriRow, movOriCol, nuevaRow, nuevaCol)])
    tablero[movOriRow][movOriCol] = ficha_original
    tablero[ficha_medio_row][ficha_medio_col] = ficha_capturada
    tablero[nuevaRow][nuevaCol] = ficha_destino_original

def finalizar_capturas_multiples(capturas_posibles):
    capturas_posibles.sort(key=len, reverse=True)
    return capturas_posibles

def ejecutar_captura_multiple_automatica(movDesRow: int, movDesCol: int, colorJugada: str, fichas_ya_capturadas: Set[Tuple[int, int]]) -> Tuple[int, int]:
    """
    Ejecuta automáticamente una secuencia de capturas múltiples usando el autómata.
    Retorna las coordenadas finales de la ficha y el total de capturas realizadas.
    """
    capturas_disponibles = obtener_capturas_multiples(movDesRow, movDesCol, colorJugada, fichas_ya_capturadas)
    
    if not capturas_disponibles:
        return movDesRow, movDesCol, 0
    mejor_secuencia = capturas_disponibles[0]
    capturas_realizadas = 0
    
    print(f"Ejecutando secuencia de {len(mejor_secuencia)} capturas automáticas...")
    
    posicion_actual_row, posicion_actual_col = movDesRow, movDesCol
    global capturas_blanca_count, capturas_negra_count

    for i, captura in enumerate(mejor_secuencia):
        origen_row, origen_col, destino_row, destino_col = captura
        if (origen_row, origen_col) != (posicion_actual_row, posicion_actual_col):
            print(f"⚠️ Error de secuencia en captura {i+1}: posición no coincide")
            break
        if validar_captura_con_automata(origen_row, origen_col, destino_row, destino_col, colorJugada):
            ficha_cap_row = (origen_row + destino_row) // 2
            ficha_cap_col = (origen_col + destino_col) // 2
            ficha_movida = tablero[origen_row][origen_col]
            ficha_capturada = tablero[ficha_cap_row][ficha_cap_col]

            tablero[destino_row][destino_col] = ficha_movida
            tablero[origen_row][origen_col] = '-'
            tablero[ficha_cap_row][ficha_cap_col] = '-'
            if ficha_capturada.lower() == 'n':
                capturas_blanca_count += 1
            elif ficha_capturada.lower() == 'b':
                capturas_negra_count += 1

            capturas_realizadas += 1
            posicion_actual_row, posicion_actual_col = destino_row, destino_col
            
            print(f'   {i+1}. {chr(65 + origen_col)}{8 - origen_row} → {chr(65 + destino_col)}{8 - destino_row} (captura en {chr(65 + ficha_cap_col)}{8 - ficha_cap_row})')
        else:
            print(f"ERROR: Captura {i+1} falló la validación del autómata")
            break
    
    print(f"Capturas múltiples completadas: {capturas_realizadas} fichas capturadas")
    return posicion_actual_row, posicion_actual_col, capturas_realizadas

def convertirDama(coordenadas, ficha):

    if (coordenadas[0] == '7') and (ficha == 'n'):
        tablero[int(coordenadas[0])][int(coordenadas[1])] = 'N'
    elif (coordenadas[0] == '0') and (ficha == 'b'):
        tablero[int(coordenadas[0])][int(coordenadas[1])] = 'B'

def moverFicha(jugada, colorJugada):
    movOriRow = 8 - int(jugada[1])
    movOriCol = letras[jugada[0].upper()]
    movDesRow = 8 - int(jugada[3])
    movDesCol = letras[jugada[2].upper()]
    coordenadasFicha = ''
    global capturas_blanca_count, capturas_negra_count

    fichaOrigen = tablero[movOriRow][movOriCol]
    fichaDestino = tablero[movDesRow][movDesCol]
    if fichaOrigen == '-':
        print('No hay ficha en la posición de origen')
        return False
    if fichaOrigen.lower() != colorJugada:
        print('La ficha no pertenece al jugador actual')
        return False
    if fichaDestino != '-':
        print('La casilla destino no está vacía')
        return False

    es_dama = fichaOrigen.isupper()
    distancia_movimiento = abs(movDesRow - movOriRow)
    
    if distancia_movimiento == 1 or (es_dama and distancia_movimiento > 1 and abs(movDesCol - movOriCol) == distancia_movimiento and 
                                      not (validar_captura_con_automata(movOriRow, movOriCol, movDesRow, movDesCol, colorJugada))):
        if es_dama and distancia_movimiento > 1:
            dir_row = 1 if movDesRow > movOriRow else -1
            dir_col = 1 if movDesCol > movOriCol else -1
            for i in range(1, distancia_movimiento):
                check_row = movOriRow + (i * dir_row)
                check_col = movOriCol + (i * dir_col)
                if tablero[check_row][check_col] != '-':
                    print('Hay obstáculos en el camino de la dama')
                    return False
        tablero[movDesRow][movDesCol] = fichaOrigen
        tablero[movOriRow][movOriCol] = '-'
        coordenadasFicha = str(movDesRow) + str(movDesCol)
    elif (distancia_movimiento == 2 and abs(movDesCol - movOriCol) == 2) or (es_dama and distancia_movimiento > 1 and abs(movDesCol - movOriCol) == distancia_movimiento):
        if validar_captura_con_automata(movOriRow, movOriCol, movDesRow, movDesCol, colorJugada):
            ficha_capturada_row = None
            ficha_capturada_col = None
            
            if es_dama and distancia_movimiento > 2:
                dir_row = 1 if movDesRow > movOriRow else -1
                dir_col = 1 if movDesCol > movOriCol else -1
                
                for i in range(1, distancia_movimiento):
                    check_row = movOriRow + (i * dir_row)
                    check_col = movOriCol + (i * dir_col)
                    ficha_check = tablero[check_row][check_col]
                    if ficha_check != '-' and ficha_check.lower() != colorJugada:
                        ficha_capturada_row = check_row
                        ficha_capturada_col = check_col
                        break
            else:
                ficha_capturada_row = (movOriRow + movDesRow) // 2
                ficha_capturada_col = (movOriCol + movDesCol) // 2
            
            if ficha_capturada_row is not None and ficha_capturada_col is not None:
                ficha_capturada = tablero[ficha_capturada_row][ficha_capturada_col]
                tablero[movDesRow][movDesCol] = fichaOrigen
                tablero[movOriRow][movOriCol] = '-'
                tablero[ficha_capturada_row][ficha_capturada_col] = '-'
                coordenadasFicha = str(movDesRow) + str(movDesCol)
                if ficha_capturada.lower() == 'n':
                    capturas_blanca_count += 1
                elif ficha_capturada.lower() == 'b':
                    capturas_negra_count += 1

                print(f'¡Ficha capturada en {chr(65 + ficha_capturada_col)}{8 - ficha_capturada_row}!')

                fichas_ya_capturadas = {(ficha_capturada_row, ficha_capturada_col)}
                capturas_adicionales = obtener_capturas_multiples(movDesRow, movDesCol, colorJugada, fichas_ya_capturadas)
                
                if capturas_adicionales:
                    print("Ejecutando capturas multiples!")
                    posicion_final_row, posicion_final_col, total_capturas = ejecutar_captura_multiple_automatica(
                        movDesRow, movDesCol, colorJugada, fichas_ya_capturadas
                    )
                    coordenadasFicha = str(posicion_final_row) + str(posicion_final_col)
                    
                    print(f"¡Secuencia de capturas completada! Total: {total_capturas + 1} fichas eliminadas")
                else:
                    print("No hay capturas adicionales disponibles.")
            else:
                print('No se encontró ficha enemiga para capturar')
                return False
        else:
            print('Captura inválida según el autómata - No se puede realizar el movimiento')
            return False
    else:
        if es_dama:
            print('Movimiento inválido para dama: debe ser diagonal')
        else:
            print('Movimiento inválido: debe ser 1 o 2 casillas diagonales')
        return False
    convertirDama(coordenadasFicha, fichaOrigen)
    return True

def imprimirTablero():
    print("\n  +---+---+---+---+---+---+---+---+")
    for i in range(8):
        fila_num = 8 - i  
        print(f"{fila_num} |", end="")
        
        for j in range(8):
            ficha = tablero[i][j]
            if ficha == '-':
                print(" · |", end="")
            elif ficha == 'n':
                print(" ○ |", end="") 
            elif ficha == 'b':
                print(" ● |", end="") 
            elif ficha == 'N':
                print(" ♕ |", end="")  
            elif ficha == 'B':
                print(" ♔ |", end="") 
        
        print("\n  +---+---+---+---+---+---+---+---+")
    
    print("    A   B   C   D   E   F   G   H")

def comprobarVictoria():
    hayNegras = False
    hayBlancas = False
    for i in tablero:
        for x in i:
            if x.lower() == 'n':
                hayNegras = True
            elif x.lower() == 'b':
                hayBlancas = True

    if hayBlancas and hayNegras:
        return False
    else:
        return True

print ('Bienvenidos al juego de las damas')
print ('Formato de jugada: A3B4')
print ('Las fichas negras (n) están en las filas 8,7,6')
print ('Las fichas blancas (b) están en las filas 1,2,3')

print ('\n')

imprimirTablero()


while movimientoValido:

    if (jugador == 'n'):
        jugador = 'b'
        print(f"Capturas - Blancas: {capturas_blanca_count}  |  Negras: {capturas_negra_count}")
        movimiento = input('Mueven las blancas: ')

    else:
        jugador = 'n'
        print(f"Capturas - Blancas: {capturas_blanca_count}  |  Negras: {capturas_negra_count}")
        movimiento = input('Mueven las negras: ')

    if moValido(movimiento, jugador):

        if moverFicha(movimiento, jugador):
            imprimirTablero()

            if comprobarVictoria():
                if jugador == 'n':
                    print ('¡Ganan las Negras!')

                else:
                    print ('¡Ganan las Blancas!')

                movimientoValido = False

        else:
            print ('Movimiento no válido - No se puede realizar el movimiento')
            if jugador == 'b':
                jugador = 'n'
            else:
                jugador = 'b'

    else:
        print ('Movimiento no válido - Jugada incorrecta')
        if jugador == 'b':
            jugador = 'n'
        else:
            jugador = 'b'
