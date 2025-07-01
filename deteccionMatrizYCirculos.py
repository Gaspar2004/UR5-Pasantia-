import cv2
import numpy as np

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
                               param1=50, param2=30, minRadius=40, maxRadius=55)
#cuanto mas bajo sea param2, mas permisivo será con tema reconocimiento de circulos
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for x, y, r in circles[0, :1]:  # solo marcamos el primero
            cv2.circle(celda, (x, y), r, (0, 255, 0), 2)
            print(f"Radio detectado: {r}")

        return True
    return False

# Captura desde webcam
cap = cv2.VideoCapture(0)

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

    # Procesar celdas
    celdas = dividir_en_celdas(frame)

    for (i, j), celda in celdas:
        if detectar_circulo(celda):
            cv2.putText(frame_copy, f"O en ({i},{j})", (j * w // 3 + 10, i * h // 3 + 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Detección de círculos", frame_copy)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
