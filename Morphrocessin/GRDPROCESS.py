import cv2
import numpy as np
import tkinter as tk
#from PIL import Image, ImageTk, ImageChops,ImageFilter
import threading
from controleImaginarios import Toolify


# Open the webcam
cap = cv2.VideoCapture(0)

# Cargar el modelo de detección de objetos preentrenado (por ejemplo, YOLO)
net = cv2.dnn.readNet("C:\\Users\iuibu\\Videos\\BunnyRay\\Caldo-Vision-v4.2.0\\funcionzaza\\yolov3.weights", "C:\\Users\iuibu\\Videos\\BunnyRay\\Caldo-Vision-v4.2.0\\funcionzaza\\yolov3.cfg")
# Obtener los nombres de todas las capas en la red
layer_names = net.getLayerNames()

# Convertir los índices de las capas de salida en nombres de capas
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Cargar los nombres de las clases
with open("C:\\Users\iuibu\\Videos\\BunnyRay\\Caldo-Vision-v4.2.0\\funcionzaza\\coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Abrir el archivo de vídeo de entrada (webcam)
#captura = cv2.VideoCapture(0)
x_ai,y_ai,junior_h,w_colon = 0,0,0,0
def zerono(val):
    if val < 0:
        return 0
    else:
        return val
def kilis(frame):
    global junior_h , w_colon,x_ai, y_ai
   
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
                w_colon = int(detection[2] * frame.shape[1])
                junior_h = int(detection[3] * frame.shape[0])
                x_ai = int(center_x - w_colon / 2)
                y_ai = int(center_y - junior_h / 2)

                # Aplicar desenfoque a la región de la botella
                #frame = aplicar_desenfoque_region(frame, (x, y, w, h))
    x_ai=zerono(x_ai)
    y_ai=zerono(y_ai)
    junior_h=zerono(junior_h)
    w_colon=zerono(w_colon)
    return [x_ai, y_ai, junior_h, w_colon]
   

# figuras
def draw_rectangle(frame, cell_x, cell_y, cell_w, cell_h, color=(0, 255, 0), thickness=3):
    cv2.rectangle(frame, (cell_x, cell_y), ((cell_x+cell_w), (cell_y+cell_h)), color, thickness)
    return frame
def draw_circle(frame, center_x, center_y, radius, color=(0, 255, 0), thickness=3):
    cv2.circle(frame, (center_x, center_y), radius, color, thickness)
    return frame


#FFX ZONA
def pixelate_region(frame, cell_x, cell_y, cell_w, cell_h):
        # Ensure the region is within the frame's boundaries
    global pxHei,pxWid
    
    small = cv2.resize(frame[cell_y:cell_y+cell_h, cell_x:cell_x+cell_w],(pxWid,pxHei), interpolation=cv2.INTER_NEAREST)
    blocky = cv2.resize(small, (cell_w, cell_h), interpolation=cv2.INTER_NEAREST)
 
    return blocky
def zoom_region(frame, cell_x, cell_y, cell_w, cell_h, zoomw=80, zoomh=8, offset_x=0, offset_y=0):
    # Asegurarse de que la región esté dentro de los límites del frame
    cell_x = max(0, min(cell_x + offset_x, frame.shape[1] - 1))
    cell_y = max(0, min(cell_y + offset_y, frame.shape[0] - 1))
    cell_w = min(cell_w, frame.shape[1] - cell_x)
    cell_h = min(cell_h, frame.shape[0] - cell_y)

    # Si la región es vacía, devolver el frame original
    if cell_w <= 0 or cell_h <= 0:
        return frame

    # Zoom en la región
    zoom = cv2.resize(frame[cell_y:cell_y+cell_h, cell_x:cell_x+cell_w],
                      (cell_w*zoomw, cell_h*zoomh), interpolation=cv2.INTER_LINEAR)
    return zoom


zoomama_1=2
zoomama_2=2
zoomOff_A=0
zoomOff_B=0
zoom_region1 = lambda frame, cell_x, cell_y, cell_w, cell_h: zoom_region(frame, cell_x, cell_y, cell_w, cell_h, zoomw=zoomama_1, zoomh=zoomama_2,offset_x=zoomOff_A,offset_y=zoomOff_B)
zoom_region2 = lambda frame, cell_x, cell_y, cell_w, cell_h: zoom_region(frame, cell_x, cell_y, cell_w, cell_h, zoomw=zoomama_1, zoomh=zoomama_1)

#EFFECT HANDLER
def move_fx(ffx,frame, cell_x, cell_y, cell_w, cell_h):
   
    # Asegúrate de que la caja esté dentro de los límites del frame
    cell_x = max(0, min(cell_x, frame.shape[1] - cell_w))
    cell_y = max(0, min(cell_y, frame.shape[0] - cell_h))
    cell_w = min(cell_w, frame.shape[1] - cell_x)
    cell_h = min(cell_h, frame.shape[0] - cell_y)

    efectoaplicao = ffx(frame, cell_x, cell_y, cell_w, cell_h)

    # Asegúrate de que efectoaplicao no sea más grande que la región de interés
    efectoaplicao = efectoaplicao[0:min(efectoaplicao.shape[0], cell_h), 0:min(efectoaplicao.shape[1], cell_w)]

    # Reemplaza la región de interés con la imagen modificada
    frame[cell_y:cell_y+efectoaplicao.shape[0], cell_x:cell_x+efectoaplicao.shape[1]] = efectoaplicao

    # Dibuja un rectángulo alrededor de las celdas seleccionadas
    #frame = draw_rectangle(frame, cell_x, cell_y, cell_w, cell_h, thickness=0)

    return frame


def check_collision(box1, box2):
    # Desempaquetar las coordenadas y dimensiones de las cajas
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2

    # Comprobar si hay una colisión
    if x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2:
        return True

    return False


#CONTROLES PAL DEBUGGIN O EL GUSTO DE Xd
def paraXx():
    global herramientas
    Interrz = tk.Tk()
    Interrz.title("~.~ webFck ~u~")
    Interrz.geometry("512x128")
    Interrz.config(bg="black")
    slidesize=Interrz.winfo_screenwidth() 
    ctrlz = ['xUbi', 'yUbi', 'pyHi', 'pxWi', 'zOfa', 'zOfb', 'Zamn', 'ZA',
             'xU2','yU2','pHi2','pWi2','pxWS','pxHS']
    herramientas = Toolify(ctrlz, 
                     Interrz, 
                     'C:\\Users\\iuibu\\Videos\\BunnyRay\\Caldo-Vision-v4.2.0\\but.png', 
                     1,12,slidesize,25,value_type=int,default_value=2)
    def RapiToolAsign(nombreli,minie,maxie):
        herramientas.sliders[nombreli].rango_Edit(minie,maxie)

    RapiToolAsign('xUbi',1,400)
    RapiToolAsign('yUbi',1,365)
    RapiToolAsign('pyHi',1,200)
    RapiToolAsign('pxWi',1,380)
    RapiToolAsign('zOfa',-100,200)
    RapiToolAsign('zOfb',50,180)
    RapiToolAsign('Zamn',1,15)
    RapiToolAsign('ZA',1,15)
    RapiToolAsign('yU2',1,365)
    RapiToolAsign('xU2',1,200)
    RapiToolAsign('pHi2',1,265)
    RapiToolAsign('pWi2',1,265)
    RapiToolAsign('pxWS',1,128)
    RapiToolAsign('pxHS',1,128)


    Interrz.mainloop()
#THREAD CONTROLES
threading.Thread(target=paraXx,daemon=True).start()
###################################################################################################################
######VISUAL LAND#####
while True:
    # Captura Cuadro X Cuadro
    ret, frame = cap.read()
   
    x_ai, y_ai, junior_h, w_colon = kilis(frame)
    # Define the new top-left corner coordinates and the new width and height of the rectangle and the zoom region
    cell_x, cell_y = x_ai,y_ai # coordinadas pal zoom
    cell_w, cell_h = w_colon, junior_h  # specify the new width and height of the cell block here
    cell_x2, cell_y2 = herramientas.sliders['xU2'].value,herramientas.sliders['yU2'].value   # coordinadas pal zoom
    cell_w2, cell_h2 = herramientas.sliders['pWi2'].value, herramientas.sliders['pHi2'].value
    zoomOff_B=herramientas.sliders['zOfa'].value
    zoomOff_A=herramientas.sliders['zOfb'].value
    zoomama_2 = herramientas.sliders['Zamn'].value
    zoomama_1 = herramientas.sliders['ZA'].value
    pxWid = herramientas.sliders[ 'pxWS'].value
    pxHei = herramientas.sliders[ 'pxHS'].value
    # Move the effect to the new area
    frame1 = move_fx(zoom_region1,frame,cell_x,cell_y,cell_w,cell_h)
    frame2 = move_fx(pixelate_region,frame,cell_x2,cell_y2,cell_w2,cell_h2) 
   
    primer = kilis(frame)
     
    # Combine the two frames
    frame = cv2.addWeighted(frame1, 0.5, frame2, 0.5,0)

    #muestra frame
    cv2.imshow('Uwu~ ~uwU', frame) 
    
    # Break the loop on 'q' key press
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

print(f"f shape = {frame.shape} && f pixel = {frame.size}")