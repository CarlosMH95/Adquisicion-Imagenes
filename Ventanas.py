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
        self.id = ''
        self.contador = 0
        self.toma = 0
        self.edad = ''
        self.genero = ''
        self.nombre = ''
        self.apellido = ''
    def sum(self):
        self.contador+=1
    def reset(self):
        self.id = ''
        self.contador = 0
        self.toma = 0
        self.edad =''
        self.genero = ''
        self.nombre = ''
        self.apellido = ''



def main():

    def select_image():

        global panelA, panelB
        # obtener las dos Imagenes
        prueba = Camaras.Camaras()
        a = prueba.detectar_camaras()
        b = prueba.crear_camara()
        if (a and b):
            global img1, img2
            img1, img2 = prueba.capturar_imagen()

            image = Image.fromarray(img1)
            image2 = Image.fromarray(img2)
            maxsize = (640, 640)
            image = image.resize(maxsize)
            image2 = image2.resize(maxsize)

            image = ImageTk.PhotoImage(image)
            image2 = ImageTk.PhotoImage(image2)
        else:
            mbox.showerror("Error", "No Se puede acceder a las camaras")
            return 0

        if panelA is None or panelB is None:

            panelA = Label(image=image)
            panelA.image = image
            panelA.pack(side="left", padx=10, pady=10)


            panelB = Label(image=image2)
            panelB.image = image2
            panelB.pack(side="right", padx=10, pady=10)


        else:
            # update the pannels
            panelA.configure(image=image)
            panelB.configure(image=image2)
            panelA.image = image
            panelB.image = image2

        root.after(3000, select_image)

    def save_image():
        global panelA, panelB
        try:
            global img1, img2
            global perfil
           # manejador = Camaras.ManejaImagen()
            print(img1)
            print(img2)
            cv2.imwrite(perfil.id +"-T"+perfil.toma+"-C1.bmp", img1)
            cv2.imwrite(perfil.id +"-T"+perfil.toma+"-C2.bmp", img2)
            perfil.sum()

            mbox.showinfo("Guardado", "Las Imagenes fueron guardadas con exito")
        except:
            mbox.showerror("Error", "No se pudo guardar las Imagenes")
    img1=0
    img2=0
    root = Tk()
    panelA = None
    panelB = None
    btn = Button(root, text="Preview", command=select_image)
    btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

    btn2 = Button(root, text="Guardar", command=save_image())
    btn2.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")
    btn3 = Button(root, text="Reset", command= lambda : reset_perfil(root))
    btn3.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")
    root.after(3000, select_image)
    # th = threading.Thread(target=select_image())
    # th.daemon = True  # terminates whenever main thread does
    # th.start()
    # kick off the GUI
    root.mainloop()

def set_perfil(id, toma, gen, ed, nom, ape, tk):
    global perfil
    perfil.id=id
    perfil.toma=toma
    perfil.genero=gen
    perfil.edad=ed
    perfil.nombre=nom
    perfil.apellido=ape

    print("holi")
    tk.destroy()
    main()


def nuevo_perfil():
    perfil = Tk()
    Label(perfil, text="Identificador").grid(row=0)
    Label(perfil, text="Numero de Toma").grid(row=1)
    Label(perfil, text="Genero").grid(row=2)
    Label(perfil, text='Edad').grid(row=3)
    Label(perfil, text='Nombre').grid(row=4)
    Label(perfil, text='Apellido').grid(row=5)

    input_id = Entry(perfil)
    toma = Entry(perfil)
    genero = Entry(perfil)
    edad = Entry(perfil)
    nombre = Entry(perfil)
    apellido = Entry(perfil)


    input_id.grid(row=0, column=1)
    toma.grid(row=1, column=1)
    genero.grid(row=2, column=1)
    edad.grid(row=3, column=1)
    nombre.grid(row=4, column=1)
    apellido.grid(row=5, column=1)

    btn = Button(perfil, text="Establecer Perfil", command=lambda: set_perfil(input_id.get(), toma.get(), genero.get(), edad.get(), nombre.get(), apellido.get(), perfil))
    btn.grid(row=6, column=1)
    w=400
    h=130
    ws=perfil.winfo_screenwidth()
    hs=perfil.winfo_screenheight()
    x=(ws/2) - (w/2)
    y=(hs/2) - (h/2)
    perfil.geometry('%dx%d+%d+%d' % (w,h,x,y))
    perfil.mainloop()

def reset_perfil(root):
    global perfil
    perfil.reset()
    root.destroy()
    nuevo_perfil()

perfil = Perfil()
nuevo_perfil()