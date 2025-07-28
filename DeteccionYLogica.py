import cv2
import numpy as np
from robot_control import *
from config import * 
from dashboard_control import *
ROBOT_IP = "192.168.0.2"  # Reemplaza con la IP real del UR5
ROBOT_PORT = 30002
import time

def sum(A, B):
    return [a + b for a, b in zip(A, B)]

def pickup(i):
    pickups=[pickup1,pickup2,pickup3,pickup4,pickup5]
    z_dim = 8.2/1000
    tot = 5
    approach_height = 15
    approach = sum(pickup_base, [0, 0, z_dim * approach_height, 0, 0, 0])
    #move_j(approach)
    #time.sleep(3.5)
    ##pos = sum(pickup_base, [0, 0, z_dim * (tot - i), 0, 0, 0])
    
    pos = pickups[i-1]
    move_l(pos)
    time.sleep(3+i)
    close_gripper()
    time.sleep(2)
    move_l(approach)
    time.sleep(1)

#Definicion de movimientos:
def primer_movimiento():
    pickup(1)
    """move_j(pickup1)
    time.sleep(4)
    close_gripper()
    time.sleep(3)
    move_j(home_position)"""

def segundo_movimiento():
    pickup(2)
    """ move_j(pickup2)
    time.sleep(4)
    close_gripper()
    time.sleep(3)
    move_j(home_position)"""

def tercer_movimiento():
    pickup(3)
    """move_j(pickup3)
    time.sleep(4)
    close_gripper()
    time.sleep(3)
    move_j(home_position)"""

def cuarto_movimiento():
    pickup(4)
    """move_j(pickup4)
    time.sleep(4)
    close_gripper()
    time.sleep(3)
    move_j(home_position)"""

def mover_a_celda(i, j):
    pose = celda_a_posicion.get((i, j))
    if pose:
        #move_j(sum(pose, [0, 0, 0.05, 0, 0, 0]))
        #time.sleep(3)
        move_l(pose)
        time.sleep(2)
        open_gripper()
        time.sleep(2)
        move_l(home_position)
        time.sleep(2)
    else:
        print(f"No hay posición definida para la celda ({i},{j})")





# ======== Lógica del juego ========

def hay_ganador(tablero, ficha):
    for i in range(3):
        if all([tablero[i][j] == ficha for j in range(3)]):
            return True
        if all([tablero[j][i] == ficha for j in range(3)]):
            return True
    if all([tablero[i][i] == ficha for i in range(3)]): #diagonal
        return True
    if all([tablero[i][2 - i] == ficha for i in range(3)]):#La otra diagonal

        return True
    return False

def obtener_celdas_vacias(tablero):
    return [(i, j) for i in range(3) for j in range(3) if tablero[i][j] == ""]

def elegir_jugada(tablero):
    for i, j in obtener_celdas_vacias(tablero):#Si el robot gana poniendo una ficha ahi
        tablero[i][j] = "X"#Para ver que pasa
        if hay_ganador(tablero, "X"):
            tablero[i][j] = ""#limpia el estado, lo devuelve al real
            return (i, j)
        tablero[i][j] = ""

    for i, j in obtener_celdas_vacias(tablero):#Si el otro gana poniendo una ficha ahi
        tablero[i][j] = "O"#Para ver que pasa
        if hay_ganador(tablero, "O"):
            tablero[i][j] = ""#limpia el estado, lo devuelve al real
            return (i, j)
        tablero[i][j] = ""

    if tablero[1][1] == "":#Si no hay nada en el centro ponerla aho
        return (1, 1)

    for i, j in [(0, 0), (0, 2), (2, 0), (2, 2)]:#Si habia algo en el centro efectivamente ponerla en la primer esquina vacia
        if tablero[i][j] == "":
            return (i, j)

    for i, j in obtener_celdas_vacias(tablero):
        return (i, j)

    return None

# ======== Visión por computadora ========

def dividir_en_celdas(frame):
    height, width = frame.shape[:2]
    cell_h, cell_w = height // 3, width // 3
    celdas = []

    for i in range(3):
        for j in range(3):
            y1 = i * cell_h
            y2 = (i + 1) * cell_h
            x1 = j * cell_w
            x2 = (j + 1) * cell_w
            celda = frame[y1:y2, x1:x2]
            celdas.append(((i, j), celda))
    return celdas

def detectar_circulo(celda):
    gray = cv2.cvtColor(celda, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 5)

    circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, dp=1.2, minDist=20,
                               param1=50, param2=50, minRadius=40, maxRadius=60)


    if circles is not None:
        circles = np.uint16(np.around(circles))
        for x, y, r in circles[0, :1]:
            cv2.circle(celda, (x, y), r, (0, 255, 0), 2)
        return True
    return False

# ======== Loop principal ========

cap = cv2.VideoCapture(0)

# Estado interno del robot
tablero_robot = [["" for _ in range(3)] for _ in range(3)]
cruces_colocadas = 0

if __name__ == '__main__':

    move_j(home_position)
    time.sleep(7)
    open_gripper()
    time.sleep(2)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_copy = frame.copy()
        h, w = frame.shape[:2]

        # Dibujar grilla
        for i in range(1, 3):
            cv2.line(frame_copy, (0, i * h // 3), (w, i * h // 3), (0, 255, 0), 2)
            cv2.line(frame_copy, (i * w // 3, 0), (i * w // 3, h), (0, 255, 0), 2)

        # Inicializar el tablero vacío
        tablero = [["" for _ in range(3)] for _ in range(3)]

        # Analizar cada celda
        cantidad_de_O = 0  # antes del for
        
        celdas = dividir_en_celdas(frame)
        for (i, j), celda in celdas:
            if detectar_circulo(celda):
                tablero[i][j] = "O"
                cantidad_de_O += 1  # cuenta cuántas O hay
                cv2.putText(frame_copy, f"O", (j * w // 3 + 30, i * h // 3 + 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            elif tablero_robot[i][j] == "X":
                tablero[i][j] = "X"
                # dibujar cruz visual
                x0 = j * w // 3 + 20
                y0 = i * h // 3 + 20
                x1 = (j + 1) * w // 3 - 20
                y1 = (i + 1) * h // 3 - 20
                cv2.line(frame_copy, (x0, y0), (x1, y1), (255, 0, 0), 3)
                cv2.line(frame_copy, (x0, y1), (x1, y0), (255, 0, 0), 3)



        # Determinar jugada del robot
        if cantidad_de_O > cruces_colocadas+1:
            print('demasiados circulos xd')
        if cantidad_de_O > cruces_colocadas:
            jugada = elegir_jugada(tablero)
            if jugada:
                i, j = jugada
                if tablero_robot[i][j] == "":
                    tablero_robot[i][j] = "X"
                    if cruces_colocadas==3:
                        cuarto_movimiento()
                        time.sleep(2)
                        mover_a_celda(i, j)
                        time.sleep(2)
                        cruces_colocadas += 1
                    if cruces_colocadas==2:
                        tercer_movimiento()
                        time.sleep(2)
                        mover_a_celda(i, j)
                        time.sleep(2)
                        cruces_colocadas += 1
                    if cruces_colocadas==1:
                        segundo_movimiento()
                        time.sleep(2)
                        mover_a_celda(i, j)
                        time.sleep(2)
                        print("primer mov terminado")
                        cruces_colocadas += 1
                    if cruces_colocadas==0:
                        primer_movimiento()
                        time.sleep(1)
                        mover_a_celda(i, j)
                        time.sleep(2)
                        print("primer mov terminado")
                        cruces_colocadas += 1
                    


                
                cv2.putText(frame_copy, f"Robot jugaria en: ({i},{j})", (10, h - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
                # Dibujar una cruz simulada sobre el frame (solo visual)
                x0 = j * w // 3 + 20
                y0 = i * h // 3 + 20
                x1 = (j + 1) * w // 3 - 20
                y1 = (i + 1) * h // 3 - 20
                cv2.line(frame_copy, (x0, y0), (x1, y1), (255, 0, 0), 3)
                cv2.line(frame_copy, (x0, y1), (x1, y0), (255, 0, 0), 3)
                print(f"Cruces colocadas: {cruces_colocadas}")

        cv2.imshow("Tateti Robot", frame_copy)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
