import tkinter as TK
from tkinter import Canvas, PhotoImage,Frame,Scrollbar
from PIL import Image, ImageTk


def scalo(value, leftMin, leftMax, rightMin, rightMax):
    # algoritmo pa sacar cuanto es el maximo y cual es el valor minimo
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

class Slido:
    
    def __init__(self, master, image_path, x, y, label_x, label_y, min_cantida=0, max_cantida=1, width=400, height=25, value_type=float, default_value=0.0,nombra='value'):
        
        self.master = master
        self.canvas = TK.Canvas(master, bg="black", width=width, height=height)
        self.canvas.pack()
        self.canvas.place(x=x, y=y)
        self.image_path = image_path
        self.x = x
        self.y = y
        self.original_x = x
        self.original_y = y
        self.original_label_x = label_x
        self.original_label_y = label_y
        self.min_cantida = min_cantida
        self.max_cantida = max_cantida
        self.value_type = value_type
        # CANVA AND IMAGE SPACE
         # Open and resize the image
  
        self.picpic = PhotoImage(file=self.image_path)
        image = Image.open(image_path)
        image = image.resize((width , height * 4), Image.LANCZOS)
        self.lapicnic = self.canvas.create_image(self.x, self.y, image=self.picpic)
        self.movement = 0
        self.visible = True
        self.nombre = nombra
        # un labelsillo pa que aparezca la cantidad que estamos alterando con el slider
        self.label = TK.Label(master, text='Value: 0', bg='light green', font='1', padx=1, pady=2)
        self.label.pack()
        #self.label.place(x=label_x, y=label_y)
        self.label.place(x=x, y=y)
        # eventos (en este caso son del mouse)
        self.canvas.bind("<Button-1>", self.move)
        self.canvas.bind("<B1-Motion>", self.move)

        # Inicializa self.value con el valor predeterminado
        self.value = self.value_type(default_value)

        
        # Convert the image to a PhotoImage
        self.picpic = ImageTk.PhotoImage(image)
    def move(self, event):
      
        # ancho y alto de la ventana
        canvAncho = self.canvas.winfo_width()
        canvAlto = self.canvas.winfo_height()
        # Check if the new position is within the boundaries of the canvas
        if 0 <= event.x <= canvAncho and 0 <= event.y <= canvAlto:
            self.picpic = PhotoImage(file=self.image_path)
            # Borra la imagen vieja pa reemplaxza posicion
            self.canvas.delete(self.lapicnic)
            # pon la nueva imagen 
           # (el numero 10 es la posicion de y si quieres que se tome en cuenta para xy pad ponerle (event.y))
            self.lapicnic = self.canvas.create_image(event.x, 10, image=self.picpic)
            self.movement += abs(self.x - event.x) + abs(self.y - event.y)
            self.x = event.x
            self.y = event.y

            # calcular valor para afectar x and y
            # ahora solo tenemos x ya que es un slider pero slido puede ser o slider o xyPad
            self.value = self.value_type(round(scalo(self.x,0,canvAncho,self.min_cantida,self.max_cantida), 1))

            # Refresca el valor uWu
            self.label.config(text=f"{self.nombre} = {self.value}")

    def visibilidad(self):
      
        if self.visible:
            self.canvas.place_forget()
            self.label.place_forget()
            self.visible = False
        else:
            # Use the original x and y coordinates to place the canvas and label
            self.canvas.place(x=self.original_x, y=self.original_y)
            self.label.place(x=self.original_label_x, y=self.original_label_y)
            self.visible = True
    def rango_Edit(self, min_val, max_val):
        self.min_cantida = min_val
        self.max_cantida = max_val
        # Ensure the current value is within the new range
        self.value = max(min_val, min(self.value, max_val))

#esto es prueba 
#ventanai = TK.Tk()
#ventanai.title("xd xd xd ")
#ventanai.geometry("500x500")
#ventanai.config(bg="black")

# mueve el slider example
#movable_image1 = Slido(ventanai, 'x.png', 50, 300, 50, 330,0,1)
#movable_image2 = Slido(ventanai, 'x.png', 50, 400, 50, 435,4,37)
#slideo3= Slido(ventanai,'x.png',50,200,50,250,14,33)

def hide_images():
    #movable_image1.visibilidad()
    #movable_image2.visibilidad()
    #slideo3.visibilidad()
    return
#hide_button = TK.Button(ventanai, text="oculta!", command=hide_images)
#hide_button.pack()
#ventanai.mainloop()
class Scrollable(Frame):
    def __init__(self, master, **kwargs):
        Frame.__init__(self, master, **kwargs)
        self.canvas = Canvas(self, bg="black")
        self.frame = Frame(self.canvas)
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.window = self.canvas.create_window((0,0), window=self.frame, anchor="nw", tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind("<Configure>", self.onCanvasConfigure)
        self.canvas.bind("<Configure>", self.onCanvasConfigure)
        self.canvas.bind_all("<MouseWheel>", self.onMouseWheel)

    def onMouseWheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def onCanvasConfigure(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.window, width = canvas_width)

#kit de sliders para modificar parametros GUI
class Toolify:
    def __init__(self, name_list, master, image_path, min_val=0, max_val=100, width=400, height=25, value_type=float, default_value=0.0):

        self.scroll_frame = Scrollable(master)
        self.scroll_frame.pack(fill="both", expand=True)
        self.sliders = {}
        start_x = 200
        start_y = 50

        label_start_x = 1
        label_start_y = 1
        num_sliders = len(name_list)
        for i in range(num_sliders):
            slider_name = name_list[i] if i < len(name_list) else f'Slider{i+1}'
            slider = Slido(self.scroll_frame.frame, 
                           image_path, 
                           start_x, start_y + i*35, label_start_x, label_start_y + i*35, 
                           min_val, max_val, width, height, value_type, default_value, slider_name)
            slider.canvas.pack() #pack es importante pa ver los resultados!
            self.sliders[slider_name] = slider

    def get_values(self):
        return {name: slider.value for name, slider in self.sliders.items()}
