import cv2
import numpy as np

def tomar_no_negativo(valor):
    if valor < 0:
        return 0
    else:
        return valor

# Función para aplicar desenfoque a una región de interés
def aplicar_desenfoque_region(frame, region):
    x, y, w, h = region
    roi = frame[y:y+h, x:x+w]
    blurred_roi = cv2.GaussianBlur(roi, (15, 15), 0)
    frame[y:y+h, x:x+w] = blurred_roi
    return frame

#
def pixelate_region(frame, cell_x, cell_y, cell_w, cell_h):

    # Ensure the region is within the frame's boundaries
    cell_x = tomar_no_negativo(min(cell_x, frame.shape[1] - 1))
    cell_y = tomar_no_negativo(min(cell_y, frame.shape[0] - 1))
    cell_w = tomar_no_negativo(min(cell_w, frame.shape[1] - cell_x))
    cell_h = tomar_no_negativo(min(cell_h, frame.shape[0] - cell_y))

    #global pxHei,pxWid
    roi = frame[cell_y:cell_y+cell_h, cell_x:cell_x+cell_w]

    #print("Dimensiones de la imagen:", frame.shape)
    #print("Coordenadas de la región:", cell_x, cell_y, cell_w, cell_h)
    #print("Dimensiones de la región de interés (ROI):", roi.shape)
    
    small = cv2.resize(roi,(15,15), interpolation=cv2.INTER_NEAREST)
    blocky = cv2.resize(small, (cell_w, cell_h), interpolation=cv2.INTER_NEAREST)
    frame[cell_y:cell_y+cell_h, cell_x:cell_x+cell_w] = blocky
 
    return frame

def zoom_region(frame, cell_x, cell_y, cell_w, cell_h, zoomw=80, zoomh=8, offset_x=0, offset_y=0):
    # Ensure the region is within the frame's boundaries
    cell_x = min(cell_x + offset_x, frame.shape[1] - 1)
    cell_y = min(cell_y + offset_y, frame.shape[0] - 1)
    cell_w = min(cell_w, frame.shape[1] - cell_x)
    cell_h = min(cell_h, frame.shape[0] - cell_y)

# Cargar el modelo de detección de objetos preentrenado (por ejemplo, YOLO)
net = cv2.dnn.readNet("funcionzaza/yolov3.weights", "funcionzaza/yolov3.cfg")
# Obtener los nombres de todas las capas en la red
layer_names = net.getLayerNames()

# Convertir los índices de las capas de salida en nombres de capas
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Cargar los nombres de las clases
with open("funcionzaza/coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

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
            if confidence > 0.5 and (class_id == 39 or class_id == 42 or class_id == 0):  # 40 es el ID de la clase 'botella'
                # Obtener las coordenadas de la caja delimitadora de la botella
                center_x = int(detection[0] * frame.shape[1])
                center_y = int(detection[1] * frame.shape[0])
                w = int(detection[2] * frame.shape[1])
                h = int(detection[3] * frame.shape[0])
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                # Aplicar desenfoque a la región de la botella
                frame = pixelate_region(frame, x, y, w, h)

    # Mostrar el frame procesado
    cv2.imshow('Video con Blur en la Botella', frame)
    
    # Salir del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar los recursos
captura.release()
cv2.destroyAllWindows()