import cv2
import numpy as np
import tkinter as tk
#from PIL import Image, ImageTk, ImageChops,ImageFilter
import threading
from controleImaginarios import Toolify

# Open the webcam
cap = cv2.VideoCapture(0)

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
    # Ensure the region is within the frame's boundaries
    cell_x = min(cell_x + offset_x, frame.shape[1] - 1)
    cell_y = min(cell_y + offset_y, frame.shape[0] - 1)
    cell_w = min(cell_w, frame.shape[1] - cell_x)
    cell_h = min(cell_h, frame.shape[0] - cell_y)

    # Zoom into the region
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
   
    efectoaplicao = ffx(frame, cell_x, cell_y, cell_w, cell_h)

    # aplicar el efecto solo a la zona de interes
    efectoaplicao = efectoaplicao[0:min(efectoaplicao.shape[0], cell_h), 0:min(efectoaplicao.shape[1], cell_w)]
    # reemplaza la zona de interes con la imagen modificada
    frame[cell_y:cell_y+efectoaplicao.shape[0], cell_x:cell_x+efectoaplicao.shape[1]] = efectoaplicao

    # Draw a rectangle around the selected cells
    frame = draw_rectangle(frame, cell_x, cell_y, cell_w, cell_h, thickness=0)

    return frame


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
                     'C:\\Users\\iuibu\\Videos\\PROJECTS\\CALDO-TECH\\but.png', 
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
    
    # Define the new top-left corner coordinates and the new width and height of the rectangle and the zoom region
    cell_x, cell_y = herramientas.sliders['xUbi'].value,herramientas.sliders['yUbi'].value # coordinadas pal zoom
    cell_w, cell_h = herramientas.sliders['pxWi'].value, herramientas.sliders['pyHi'].value  # specify the new width and height of the cell block here
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