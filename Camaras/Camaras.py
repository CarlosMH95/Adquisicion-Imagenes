import cv2
import numpy
import pypylon.pylon as pylon
class Camaras():

    def __init__(self):

        self.camarasDetectadas = []
        self.numCamaras = 0
        self.nombreCamaras = []
        self.tlfactory = tlfactory = pylon.TlFactory.GetInstance()
        self.ptl = tlfactory.CreateTl('BaslerGigE')
        self.icam = False
        self.xcam = False

    def detectar_camaras(self):

        try:
            self.camarasDetectadas = self.ptl.EnumerateDevices()
            self.numCamaras = len(self.camarasDetectadas)
            return True
        except:
            return False
    def nombre_camaras(self):

        try:
            for camara in self.camarasDetectadas:
                self.nombreCamaras.append(camara.GetFriendlyName())
                print('Nombre: ' + camara.GetFriendlyName())
            return True
        except:
            return False

    def crear_camara(self):
        try:
            self.icam = pylon.InstantCamera(self.ptl.CreateDevice(self.camarasDetectadas[0]))
            self.xcam = pylon.InstantCamera(self.ptl.CreateDevice(self.camarasDetectadas[1]))
            return True
        except:
            return False
    def capturar_imagen(self):

        if(self.icam and self.xcam):
            self.icam.Open()
            img = self.icam.GrabOne(4000)
            self.icam.Close()
            self.xcam.Open()
            img2 = self.xcam.GrabOne(4000)
            self.xcam.Close()
            img = img.Array
            img2 = img2.Array
            return img, img2
        else:
            return False

class ManejaImagen():
    def __init__(self):
        self.ruta = ''
        self.nombre = ''
        self.contador = 0

    def guardar_imagen(self, imagen1, imagen2, ncam1, ncam2):
        try:
            cv2.imwrite(ncam1+"-img-" + self.contador+ ".jpg", imagen1)
            self.contador +=1
            cv2.imwrite(ncam2 + "-img-" + self.contador + ".jpg", imagen2)
            self.contador +=1
            return True
        except:
            return False

    def set_ruta(self, ruta):
        self.ruta=ruta

    def set_nombre(self, nombre):
        self.nombre = nombre

