import cv2
from tkinter import *
from PIL import Image as Im
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog as tkFileDialog
from Camaras import Camaras
from tkinter import messagebox as mbox
import itertools
import os
import shutil
import threading
import time
class Perfil():
    def __init__(self):
        self.id=''
        self.contador=0
        self.toma=0
    def sum(self):
        self.contador+=1
    def reset(self):
        self.id = ''
        self.contador = 0
        self.toma = 0



def main():
    def select_image():
        # grab a reference to the image panels
        global panelA, panelB
        # obtener las dos Imagenes
        prueba = Camaras.Camaras()
        a = prueba.detectar_camaras()
        b = prueba.crear_camara()
        if (a and b):
            global img1, img2
            img1, img2 = prueba.capturar_imagen()
            # convert the images to PIL format...
            image = Image.fromarray(img1)
            image2 = Image.fromarray(img2)
            maxsize = (640, 640)
            image = image.resize(maxsize)
            image2 = image2.resize(maxsize)

            # ...and then to ImageTk format
            image = ImageTk.PhotoImage(image)
            image2 = ImageTk.PhotoImage(image2)
        else:
            mbox.showerror("Error", "No Se puede acceder a las camaras")
            return 0
        # if the panels are None, initialize them
        if panelA is None or panelB is None:
            # the first panel will store our original image
            panelA = Label(image=image)
            panelA.image = image
            panelA.pack(side="left", padx=10, pady=10)

            # while the second panel will store the edge map
            panelB = Label(image=image2)
            panelB.image = image2
            panelB.pack(side="right", padx=10, pady=10)

        # otherwise, update the image panels
        else:
            # update the pannels
            panelA.configure(image=image)
            panelB.configure(image=image2)
            panelA.image = image
            panelB.image = image2
        # panelA.after(8000, select_image())
        # panelB.after(8000, select_image())
        root.after(3000, select_image)
        print("Hola Mundo")

    def save_image(perfil):
        global panelA, panelB
        try:
            global img1, img2
            manejador = Camaras.ManejaImagen()
            print(img1)
            print(img2)
            cv2.imwrite("panelA-img-.bmp", img1)
            cv2.imwrite("panelB-img-.jpg", img2)

            # r=manejador.guardar_imagen(img1, img2, 'prueba-i', 'prueba-x')
            # print (r)
            mbox.showinfo("Guardado", "Las Imagenes fueron guardadas con exito")
        except:
            mbox.showerror("Error", "No se pudo guardar las Imagenes")
    img1=0
    img2=0
    root = Tk()
    panelA = None
    panelB = None


    # create a button, then when pressed, will trigger a file chooser
    # dialog and allow the user to select an input image; then add the
    # button the GUI
    btn = Button(root, text="Preview", command=select_image)
    btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

    btn2 = Button(root, text="Guardar", command=save_image)
    btn2.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")
    root.after(3000, select_image)
    # th = threading.Thread(target=select_image())
    # th.daemon = True  # terminates whenever main thread does
    # th.start()
    # kick off the GUI
    root.mainloop()
def set_perfil():
    pass
