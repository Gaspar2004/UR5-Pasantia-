# UR5-Pasantia-
UR5 Pasantia 

---

## **Flujo general del programa - "Tateti Robot UR5"**

---

### 1. **Inicialización**

* Se importan librerías (`cv2`, `numpy`, módulos de control `robot_control`, `dashboard_control`, etc.)
* Se define la IP y puerto del robot UR5.
* Se inicializa el estado interno del juego (`tablero_robot`) y contador de cruces (`cruces_colocadas`).
* Se inicia la cámara con `cv2.VideoCapture(0)`.
* El robot va a la posición `home` y abre el gripper para estar listo.

---

### 2. **Loop principal (visión + lógica del juego)**

Este bloque se ejecuta constantemente dentro del `while True`:

#### a. **Captura de imagen**

* Se captura un frame de la cámara.
* Se hace una copia para visualizar anotaciones (`frame_copy`).
* Se dibuja la grilla del tablero visualmente.

#### b. **División y análisis de celdas**

* Se divide la imagen en 9 celdas (3x3).
* Se analiza cada celda:

  * Si se detecta un círculo (`O`) mediante HoughCircles → se actualiza el tablero visual.
  * Si hay una `X` ya colocada por el robot (según `tablero_robot`) → se dibuja la cruz.

#### c. **Decisión de jugada del robot**

* Si hay más `O`s que cruces colocadas (es decir, le toca jugar al robot):

  * Se elige la mejor jugada con `elegir_jugada(tablero)` (estrategia simple tipo AI).
  * Se llama a la función `pickup(n)` para agarrar una cruz física del stack.
  * Luego, `mover_a_celda(i, j)` la mueve a la celda destino.
  * Se actualiza `tablero_robot` y el contador `cruces_colocadas`.

---

### 3. **Módulos de control del robot**

#### `pickup(i)`

* Posiciona el robot sobre una cruz del stack y la agarra con el gripper.
* Usa `move_l()` para moverse y `close_gripper()` para cerrar el gripper.

#### `mover_a_celda(i, j)`

* Busca la posición física de la celda en `celda_a_posicion[(i, j)]`.
* Mueve el robot a esa posición y deja la cruz usando `open_gripper()`.

---

### 4. **Lógica del juego**

#### `hay_ganador(tablero, ficha)`

* Verifica si hay línea ganadora en filas, columnas o diagonales.

#### `elegir_jugada(tablero)`

* Selecciona el mejor movimiento para el robot:

  1. Gana si puede.
  2. Bloquea al rival si es necesario.
  3. Prioriza el centro.
  4. Luego esquinas.
  5. Finalmente cualquier celda vacía.

---

### 5. **Detección visual**

#### `detectar_circulo(celda)`

* Convierte la celda a escala de grises.
* Aplica `cv2.HoughCircles` para detectar círculos (las fichas O del humano).
* Dibuja la circunferencia en la interfaz si se detecta.

---

## 📌 Ejecución general:

1. **Robot va a home y se posiciona**
2. **Cámara detecta O del humano**
3. **Robot analiza el tablero**
4. **Elige jugada y coloca una X**
5. **Actualiza estado**
6. **Repite el ciclo hasta que se cierre el programa**

---
