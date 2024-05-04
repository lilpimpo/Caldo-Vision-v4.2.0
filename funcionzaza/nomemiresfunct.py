import cv2
import numpy as np

# Función para aplicar desenfoque a una región de interés
def aplicar_desenfoque_region(frame, region):
    x, y, w, h = region
    roi = frame[y:y+h, x:x+w]
    blurred_roi = cv2.GaussianBlur(roi, (15, 15), 0)
    frame[y:y+h, x:x+w] = blurred_roi
    return frame

# Cargar el modelo de detección de objetos preentrenado (por ejemplo, YOLO)
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
# Obtener los nombres de todas las capas en la red
layer_names = net.getLayerNames()

# Convertir los índices de las capas de salida en nombres de capas
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Cargar los nombres de las clases
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Abrir el archivo de vídeo de entrada (webcam)
captura = cv2.VideoCapture(0)

while True:
    # Leer el frame de la webcam
    ret, frame = captura.read()
    if not ret:
        break
    
    # Detectar objetos en el frame
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Procesar las detecciones
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = scores.argmax()
            confidence = scores[class_id]
            if confidence > 0.5 and class_id == 39:  # 40 es el ID de la clase 'botella'
                # Obtener las coordenadas de la caja delimitadora de la botella
                center_x = int(detection[0] * frame.shape[1])
                center_y = int(detection[1] * frame.shape[0])
                w = int(detection[2] * frame.shape[1])
                h = int(detection[3] * frame.shape[0])
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                # Aplicar desenfoque a la región de la botella
                frame = aplicar_desenfoque_region(frame, (x, y, w, h))

    # Mostrar el frame procesado
    cv2.imshow('Video con Blur en la Botella', frame)
    
    # Salir del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar los recursos
captura.release()
cv2.destroyAllWindows()