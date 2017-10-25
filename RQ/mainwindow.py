__author__ = "Rosa Quelal"
__version__ = "0.1"
__license__ = "GPL"
#http://audhootchavancv.blogspot.in/2015/08/how-to-install-opencv-30-and.html
#http://stackoverflow.com/questions/42608721/image-fusion-using-wavelet-transform-in-python
import cv2
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qt import *
from PyQt5.QtWidgets import *
import numpy as np
import os
import pywt


(Ui_MainWindow, QMainWindow) = uic.loadUiType('mainwindow.ui')

class ImageProcess():

    def Calib(self, im1, im2, FinalIm, DirectIm, OutIm, FusionIm, algorithm, Alig):
        global w,h
        img1 = cv2.imread(im1)
        img2 = cv2.imread(im2)

        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        if algorithm == "SIFT":
            sift = cv2.xfeatures2d.SIFT_create()
            (kps_1, des_1) = sift.detectAndCompute(gray1, None)
            (kps_2, des_2) = sift.detectAndCompute(gray2, None)

        elif algorithm == "SURF":
            surf = cv2.xfeatures2d.SURF_create()
            (kps_1, des_1) = surf.detectAndCompute(gray1, None)
            (kps_2, des_2) = surf.detectAndCompute(gray2, None)

        elif algorithm == "BRIEF":
            orb = cv2.ORB_create()
            brief = cv2.xfeatures2d.BriefDescriptorExtractor_create()
            star = cv2.xfeatures2d.StarDetector_create()
            kps_1 = orb.detect(gray1, None)
            kps_2 = orb.detect(gray2, None)
            (kps_1, des_1) = brief.compute(gray1, kps_1)
            (kps_2, des_2) = brief.compute(gray2, kps_2)

        elif algorithm == "BRISK":
            brisk = cv2.BRISK_create()
            (kps_1, des_1) = brisk.detectAndCompute(gray1, None)
            (kps_2, des_2) = brisk.detectAndCompute(gray2, None)

        #Mapeo y Corte
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des_1, des_2, k=2)
        good_match = []
        mkp1, mkp2 = [], []
        xx = 0.00
        xxpos = 0.00
        xxneg = 0.00
        yy = 0.00
        yypos = 0.00
        yyneg = 0.00
        count = 0
        for m, n in matches:
            if ((m.distance < 0.7 * n.distance)):
                good_match.append([m])
                mkp1.append(kps_1[m.queryIdx].pt)
                mkp2.append(kps_2[m.trainIdx].pt)
                x1 = str(kps_1[m.queryIdx].pt).replace("(", "").replace(")", "").replace(",", "").split()[0]
                x2 = str(kps_2[m.trainIdx].pt).replace("(", "").replace(")", "").replace(",", "").split()[0]
                y1 = str(kps_1[m.queryIdx].pt).replace("(", "").replace(")", "").replace(",", "").split()[1]
                y2 = str(kps_2[m.trainIdx].pt).replace("(", "").replace(")", "").replace(",", "").split()[1]
                count += 1
                x = float(x2) - float(x1)
                y = float(y2) - float(y1)
                if x >= 0:
                    xxpos = xxpos + x
                else:
                    xxneg = xxneg + x
                if y >= 0:
                    yypos = yypos + y
                else:
                    yyneg = yyneg + y

        imgf = cv2.drawMatchesKnn(img1, kps_1, img2, kps_2, good_match, img1, flags=2)
        cv2.imwrite(FinalIm, imgf)

        if (abs(round(xxpos)) >= abs(round(xxneg))):
            xx = xxpos
        else:
            xx = xxneg
        if (abs(round(yypos)) >= abs(round(yyneg))):
            yy = yypos
        else:
            yy = yyneg
        w = int(abs(round((xx / count), 0)))
        h = int(abs(round((yy / count), 0)))

        ima1 = gray1[h:np.size(gray1[0][:]), w:np.size(gray1[0][:])]
        rows,cols = gray2.shape[:2]
        M = cv2.getRotationMatrix2D((cols/2,rows/2),180,1.0)
        ima2 = cv2.warpAffine(gray2,M,(cols,rows))
        ima2 = ima2[h:np.size(gray1[0][:]), w:np.size(gray1[0][:])]
        rows, cols = ima2.shape[:2]
        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 180, 1.0)
        ima2 = cv2.warpAffine(ima2,M,(cols,rows))

        cv2.imwrite(OutIm, ima1)
        cv2.imwrite(DirectIm, ima2)

        #Fusion de imagenes
        # First: Do wavelet transform on each image
        wavelet = 'db1'
        cooef1 = pywt.wavedec2(ima1[:, :], wavelet)
        cooef2 = pywt.wavedec2(ima2[:, :], wavelet)
        # Second: for each level in both image do the fusion according to the desire option
        fusedCooef = []

        for i in range(len(cooef1) - 1):
            if (i == 0):
                c1 = (cooef1[0] + cooef2[0]) / 2  # mean
                fusedCooef.append((c1))
            else:
                c1 = (cooef1[i][0] + cooef2[i][0]) / 2  # mean
                c2 = (cooef1[i][1] + cooef2[i][1]) / 2  # mean
                c3 = (cooef1[i][2] + cooef2[i][2]) / 2  # mean
                fusedCooef.append((c1, c2, c3))

        # Third: After we fused the cooefficent we nned to transfor back to get the image
        fusedImage = pywt.waverec2(fusedCooef, wavelet)
        # Forth: normmalize values to be in uint8
        fusedImage = np.multiply(
            np.divide(fusedImage - np.min(fusedImage), (np.max(fusedImage) - np.min(fusedImage))), 255)
        fusedImage = np.uint8(fusedImage)
        cv2.imwrite(FusionIm, fusedImage)

    def Alignment(self, im1, im2, FinalIm, DirectIm, OutIm, FusionIm, algorithm, Alig):
        global w,h
        img1 = cv2.imread(im1)
        img2 = cv2.imread(im2)
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        ima1 = gray1[h:np.size(gray1[0][:]), w:np.size(gray1[0][:])]
        rows,cols = gray2.shape[:2]
        M = cv2.getRotationMatrix2D((cols/2,rows/2),180,1.0)
        ima2 = cv2.warpAffine(gray2,M,(cols,rows))
        ima2 = ima2[h:np.size(gray1[0][:]), w:np.size(gray1[0][:])]
        rows, cols = ima2.shape[:2]
        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 180, 1.0)
        ima2 = cv2.warpAffine(ima2,M,(cols,rows))

        cv2.imwrite(OutIm, ima1)
        cv2.imwrite(DirectIm, ima2)

        #Fusion de imagenes
        # First: Do wavelet transform on each image
        wavelet = 'db1'
        cooef1 = pywt.wavedec2(ima1[:, :], wavelet)
        cooef2 = pywt.wavedec2(ima2[:, :], wavelet)
        # Second: for each level in both image do the fusion according to the desire option
        fusedCooef = []

        for i in range(len(cooef1) - 1):
            if (i == 0):
                c1 = (cooef1[0] + cooef2[0]) / 2  # mean
                fusedCooef.append((c1))
            else:
                c1 = (cooef1[i][0] + cooef2[i][0]) / 2  # mean
                c2 = (cooef1[i][1] + cooef2[i][1]) / 2  # mean
                c3 = (cooef1[i][2] + cooef2[i][2]) / 2  # mean
                fusedCooef.append((c1, c2, c3))

        # Third: After we fused the cooefficent we nned to transfor back to get the image
        fusedImage = pywt.waverec2(fusedCooef, wavelet)
        # Forth: normmalize values to be in uint8
        fusedImage = np.multiply(
            np.divide(fusedImage - np.min(fusedImage), (np.max(fusedImage) - np.min(fusedImage))), 255)
        fusedImage = np.uint8(fusedImage)
        cv2.imwrite(FusionIm, fusedImage)

class VideoCam():
    def __init__(self, capture):
        self.capture = capture
        self.currentFrame = np.array([])


    def captureNextFrame(self, color):
        ret, readFrame = self.capture.read()
        if (ret == True):
            #if (color == "RGB"): self.currentFrame = cv2.cvtColor(readFrame, cv2.COLOR_BGR2RGB)
            #if (color == "GRAY"): self.currentFrame = cv2.cvtColor(readFrame, cv2.COLOR_BGR2GRAY)
            self.currentFrame = cv2.cvtColor(readFrame, cv2.COLOR_BGR2RGB)
    def convertFrame(self):
        try:
            height, width = self.currentFrame.shape[:2]
            img = QImage(self.currentFrame,
                         width,
                         height,
                         QImage.Format_RGB888)
            img = QPixmap.fromImage(img)
            self.previousFrame = self.currentFrame
            return img
        except:
            return None

    def capPropId(self,prop):
        return getattr(cv2 ,("") + "CAP_PROP_" + prop)

    def getFrame(self):
        """     converts frame to format suitable for QtGui            """
        try:
            height, width = self.currentFrame.shape[:2]
            img = QImage(self.currentFrame,
                         width,
                         height,
                         QImage.Format_RGB888)
            img = QPixmap.fromImage(img)
            return img
        except:
            return None

    def getImg(self):
        return self.currentFrame

class CameraInfo():
    def clearCapture(self, capture):
        capture.release()
        cv2.destroyAllWindows()

    def Cameras(self):
        Cam = []
        self.numeroCamaras = 0
        for i in range(0,10):
            try:
                cap = cv2.VideoCapture(i)
                ret, frame = cap.read()
                cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                self.clearCapture(cap)
                Cam.append(i)
                self.numeroCamaras = self.numeroCamaras + 1
            except:
                self.clearCapture(cap)
                break
        print(self.numeroCamaras)
        return Cam

class MainWindow(QMainWindow):
    camera01 = False
    camera02 = False
    camera03 = False

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        info = []
        self.Cam = CameraInfo()
        info = self.Cam.Cameras()
        print(self.Cam.numeroCamaras)
        self.raiz = os.getcwd() + "/dataset/"
        self.ruta = self.raiz
        self.secuencia = 1
        print(info,self.ruta,len(info))
        self.imageprocess = ImageProcess()
        if len(info) >= 1:
            self.videoCam1 = VideoCam(cv2.VideoCapture(info[0]))
            self.camera01 = True
            if len(info) >= 3:
                self.videoCam2 = VideoCam(cv2.VideoCapture(info[1]))
                self.videoCam3 = VideoCam(cv2.VideoCapture(info[2]))
                self.camera02 = True
                self.camera03 = True
            else:
                if len(info) == 2:
                    self.videoCam2 = VideoCam(cv2.VideoCapture(info[1]))
                    self.camera02 = True
        self.ui.CalPBCaptureAd.clicked.connect(self.AdquisitionPhoto)
        self.ui.AdqPh_ma.clicked.connect(self.Aumentar)
        self.ui.AdqPh_me.clicked.connect(self.Disminuir)
        self.ui.AdqPh.clicked.connect(self.TraerFoto)
        self.ui.comboBox.addItem("Surf")
        # self.ui.comboBox.addItem("Sift")
        # self.ui.comboBox.addItem("Brief")
        # self.ui.comboBox.addItem("Brisk")
        self.ui.comboBox_2.addItem("Surf")
        # self.ui.comboBox_2.addItem("Sift")
        # self.ui.comboBox_2.addItem("Brief")
        # self.ui.comboBox_2.addItem("Brisk")
        self.ui.CLG1.clicked.connect(self.CalibFirst)
        self.ui.CLG2.clicked.connect(self.CalibSecond)
        self.ui.DCG1.clicked.connect(self.DescribirFirst)
        self.ui.DCG2.clicked.connect(self.DescribirSecond)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.play)
        self._timer.start(27)
        self.ui.lbl_secuencia.setText("0000001")

        self.update()

    def play(self):
        try:
            if self.camera01:
                self.videoCam1.captureNextFrame("RGB")
                self.ui.AdqVideoFrame1.setPixmap(self.videoCam1.convertFrame())

            if self.camera02:
                self.videoCam2.captureNextFrame("GRAY")
                self.ui.AdqVideoFrame2.setPixmap(self.videoCam2.convertFrame())

            if self.camera03:
                self.videoCam3.captureNextFrame("GRAY")
                self.ui.AdqVideoFrame3.setPixmap(self.videoCam3.convertFrame())
        except:
#            print "No frame"
            return None

    def AdquisitionPhoto(self):
        name = "0000000" + str(self.secuencia)
        name = name[len(name)-7:len(name)]
        self.ruta = self.raiz + name

        if self.camera01:
            self.ui.AdqPhotoFrame1.setPixmap(self.videoCam1.getFrame())
            self.IphotoCam1 = self.videoCam1.getImg()
            cv2.imwrite(self.ruta + "IphotoCam1.bmp", self.IphotoCam1)

        # rows,cols = self.IphotoCam1.shape[:2]
        # M = cv2.getRotationMatrix2D((cols/2,rows/2),2,1)
        # img_rotate = cv2.warpAffine(self.IphotoCam1,M,(cols,rows))
        # self.IphotoCam2 = img_rotate
        #
        # rows, cols = self.IphotoCam1.shape[:2]
        # M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 358, 1)
        # img_rotate = cv2.warpAffine(self.IphotoCam1, M, (cols, rows))
        # self.IphotoCam3 = img_rotate

        rows,cols = self.IphotoCam1.shape[:2]
        M = np.float32([[1, 0, 100], [0, 1, 50]])
        dst = cv2.warpAffine(self.IphotoCam1, M, (cols, rows))
        self.IphotoCam2 = dst
        cv2.imwrite(self.ruta + "IphotoCam2.bmp", self.IphotoCam2)

        if self.camera02:
            self.ui.AdqPhotoFrame2.setPixmap(self.videoCam2.getFrame())
            self.IphotoCam2 = self.videoCam1.getImg()
            cv2.imwrite(self.ruta + "IphotoCam2.bmp", self.IphotoCam2)

        if self.camera03:
            self.ui.AdqPhotoFrame3.setPixmap(self.videoCam3.getFrame())
            self.IphotoCam3 = self.videoCam1.getImg()
            cv2.imwrite(self.ruta + "IphotoCam3.bmp", self.IphotoCam3)

        self.secuencia = self.secuencia + 1
        self.ui.lbl_secuencia.setText(name)

    def Aumentar(self):
        sec = int(self.ui.lbl_secuencia.text())
        sec = sec + 1
        name = "0000000" + str(sec)
        name = name[len(name)-7:len(name)]
        self.ui.lbl_secuencia.setText(name)

    def Disminuir(self):
        sec = int(self.ui.lbl_secuencia.text())
        if sec >= 1:
            sec = sec - 1
            name = "0000000" + str(sec)
            name = name[len(name)-7:len(name)]
            self.ui.lbl_secuencia.setText(name)

    def TraerFoto(self):
        name = "0000000" + str(self.ui.lbl_secuencia.text())
        name = name[len(name)-7:len(name)]
        self.ruta = self.raiz + name
        #print (self.ruta+ "IphotoCam1.bmp")
        try:
            self.ui.AdqPhotoFrame1.setPixmap(QPixmap.fromImage(QImage(self.ruta + "IphotoCam1.bmp")))
            self.ui.AdqPhotoFrame2.setPixmap(QPixmap.fromImage(QImage(self.ruta + "IphotoCam2.bmp")))
            self.ui.AdqPhotoFrame3.setPixmap(QPixmap.fromImage(QImage(self.ruta + "IphotoCam3.bmp")))
        except:
            #            print "No frame"
            return None

    def CalibFirst(self):
        global gM1, Gx1, Gy1, Gw1, Gh1, GkpsA1, GkpsB1, Ggood_match1
        global gM2, Gx2, Gy2, Gw2, Gh2, GkpsA2, GkpsB2, Ggood_match2
        self.imageprocess.Calib(self.ruta + "IphotoCam2.bmp", self.ruta + "IphotoCam1.bmp",
                                self.ruta + "SurfMatchPhoto1_2.bmp", self.ruta + "SurfAlgCrop1.bmp",
                                self.ruta + "SurfAlgCrop2.bmp", self.ruta + "Fusion1.bmp", "SURF", 1)
        self.setDescriptorFirst("Surf")
        # if self.ui.comboBox.currentIndex() == 0:    #Surf
        #     self.imageprocess.Calib(self.ruta + "IphotoCam2.bmp", self.ruta + "IphotoCam1.bmp",
        #                             self.ruta + "SurfMatchPhoto1_2.bmp", self.ruta + "SurfAlgCrop1.bmp",
        #                             self.ruta + "SurfAlgCrop2.bmp", self.ruta + "Fusion1.bmp", "SURF",1)
        #     self.setDescriptorFirst("Surf")
        # if self.ui.comboBox.currentIndex() == 1:   #Sift
        #     print("Sift")
        #     self.imageprocess.Calib(self.ruta + "IphotoCam2.bmp", self.ruta + "IphotoCam1.bmp",
        #                             self.ruta + "SiftMatchPhoto1_2.bmp", self.ruta + "SiftAlgCrop1.bmp",
        #                             self.ruta + "SiftAlgCrop2.bmp", self.ruta + "Fusion1.bmp", "SIFT",1)
        #     self.setDescriptorFirst("Sift")
        # if self.ui.comboBox.currentIndex() == 2:  # Brief
        #     print("Brief")
        #     self.imageprocess.Calib(self.ruta + "IphotoCam2.bmp", self.ruta + "IphotoCam1.bmp",
        #                             self.ruta + "BriefMatchPhoto1_2.bmp", self.ruta + "BriefAlgCrop1.bmp",
        #                             self.ruta + "BriefAlgCrop2.bmp", self.ruta + "Fusion1.bmp", "BRIEF",1)
        #     self.setDescriptorFirst("Brief")
        # if self.ui.comboBox.currentIndex() == 3:  # Brisk
        #     print("Brisk")
        #     self.imageprocess.Calib(self.ruta + "IphotoCam2.bmp", self.ruta + "IphotoCam1.bmp",
        #                             self.ruta + "BriskMatchPhoto1_2.bmp", self.ruta + "BriskAlgCrop1.bmp",
        #                             self.ruta + "BriskAlgCrop2.bmp", self.ruta + "Fusion1.bmp", "BRISK",1)
        #     self.setDescriptorFirst("Brisk")

    def CalibSecond(self):
        self.imageprocess.Calib(self.ruta + "IphotoCam3.bmp", self.ruta + "IphotoCam2.bmp",
                                self.ruta + "SurfMatchPhoto2_3.bmp", self.ruta + "SurfAlgCrop2_2.bmp",
                                self.ruta + "SurfAlgCrop3.bmp", self.ruta + "Fusion2.bmp", "SURF", 2)
        self.setDescriptorSecond("Surf")
        # if self.ui.comboBox_2.currentIndex() == 0:  # Surf
        #     self.imageprocess.Calib(self.ruta + "IphotoCam3.bmp", self.ruta + "IphotoCam1.bmp",
        #                             self.ruta + "SurfMatchPhoto2_3.bmp", self.ruta + "SurfAlgCrop1_2.bmp",
        #                             self.ruta + "SurfAlgCrop3.bmp", self.ruta + "Fusion2.bmp", "SURF",2)
        #     self.setDescriptorSecond("Surf")
        # if self.ui.comboBox_2.currentIndex() == 1:  # Sift
        #     self.imageprocess.Calib(self.ruta + "IphotoCam3.bmp", self.ruta + "IphotoCam1.bmp",
        #                             self.ruta + "SiftMatchPhoto2_3.bmp", self.ruta + "SiftAlgCrop1_2.bmp",
        #                             self.ruta + "SiftAlgCrop3.bmp", self.ruta + "Fusion2.bmp", "SIFT",2)
        #     self.setDescriptorSecond("Sift")
        # if self.ui.comboBox_2.currentIndex() == 2:  # Brief
        #     self.imageprocess.Calib(self.ruta + "IphotoCam3.bmp", self.ruta + "IphotoCam1.bmp",
        #                             self.ruta + "BriefMatchPhoto2_3.bmp", self.ruta + "BriefAlgCrop1_2.bmp",
        #                             self.ruta + "BriefAlgCrop3.bmp", self.ruta + "Fusion2.bmp", "BRIEF",2)
        #     self.setDescriptorSecond("Brief")
        # if self.ui.comboBox_2.currentIndex() == 3:  # Brick
        #     self.imageprocess.Calib(self.ruta + "IphotoCam3.bmp", self.ruta + "IphotoCam1.bmp",
        #                             self.ruta + "BriskMatchPhoto2_3.bmp", self.ruta + "BriskAlgCrop1_2.bmp",
        #                             self.ruta + "BriskAlgCrop3.bmp", self.ruta + "Fusion2.bmp", "BRISK",2)
        #     self.setDescriptorSecond("Brisk")

    def DescribirFirst(self):
        self.imageprocess.Alignment(self.ruta + "IphotoCam2.bmp", self.ruta + "IphotoCam1.bmp",
                                    self.ruta + "SurfMatchPhoto1_2.bmp", self.ruta + "SurfAlgCrop1.bmp",
                                    self.ruta + "SurfAlgCrop2.bmp", self.ruta + "Fusion1.bmp", "SURF", 1)
        self.setDescriptorFirst("Surf")
        # if self.ui.comboBox.currentIndex() == 0:    #Surf
        #     self.imageprocess.Alignment(self.ruta + "IphotoCam2.bmp", self.ruta + "IphotoCam1.bmp",
        #                                 self.ruta + "SurfMatchPhoto1_2.bmp", self.ruta + "SurfAlgCrop1.bmp",
        #                                 self.ruta + "SurfAlgCrop2.bmp", self.ruta + "Fusion1.bmp", "SURF",1)
        #     self.setDescriptorFirst("Surf")
        # if self.ui.comboBox.currentIndex() == 1:   #Sift
        #     print("Sift")
        #     self.imageprocess.Alignment(self.ruta + "IphotoCam2.bmp", self.ruta + "IphotoCam1.bmp",
        #                                 self.ruta + "SiftMatchPhoto1_2.bmp", self.ruta + "SiftAlgCrop1.bmp",
        #                                 self.ruta + "SiftAlgCrop2.bmp", self.ruta + "Fusion1.bmp", "SIFT",1)
        #     self.setDescriptorFirst("Sift")
        # if self.ui.comboBox.currentIndex() == 2:  # Brief
        #     print("Brief")
        #     self.imageprocess.Alignment(self.ruta + "IphotoCam2.bmp", self.ruta + "IphotoCam1.bmp",
        #                                 self.ruta + "BriefMatchPhoto1_2.bmp", self.ruta + "BriefAlgCrop1.bmp",
        #                                 self.ruta + "BriefAlgCrop2.bmp", self.ruta + "Fusion1.bmp", "BRIEF",1)
        #     self.setDescriptorFirst("Brief")
        # if self.ui.comboBox.currentIndex() == 3:  # Brisk
        #     print("Brisk")
        #     self.imageprocess.Alignment(self.ruta + "IphotoCam2.bmp", self.ruta + "IphotoCam1.bmp",
        #                                 self.ruta + "BriskMatchPhoto1_2.bmp", self.ruta + "BriskAlgCrop1.bmp",
        #                                 self.ruta + "BriskAlgCrop2.bmp", self.ruta + "Fusion1.bmp", "BRISK",1)
        #     self.setDescriptorFirst("Brisk")

    def DescribirSecond(self):
        self.imageprocess.Alignment(self.ruta + "IphotoCam3.bmp", self.ruta + "IphotoCam2.bmp",
                                    self.ruta + "SurfMatchPhoto2_3.bmp", self.ruta + "SurfAlgCrop2_2.bmp",
                                    self.ruta + "SurfAlgCrop3.bmp", self.ruta + "Fusion2.bmp", "SURF", 2)
        self.setDescriptorSecond("Surf")
        # if self.ui.comboBox_2.currentIndex() == 0:  # Surf
        #     self.imageprocess.Alignment(self.ruta + "IphotoCam3.bmp", self.ruta + "IphotoCam1.bmp",
        #                                 self.ruta + "SurfMatchPhoto2_3.bmp", self.ruta + "SurfAlgCrop1_2.bmp",
        #                                 self.ruta + "SurfAlgCrop3.bmp", self.ruta + "Fusion2.bmp", "SURF",2)
        #     self.setDescriptorSecond("Surf")
        # if self.ui.comboBox_2.currentIndex() == 1:  # Sift
        #     self.imageprocess.Alignment(self.ruta + "IphotoCam3.bmp", self.ruta + "IphotoCam1.bmp",
        #                                 self.ruta + "SiftMatchPhoto2_3.bmp", self.ruta + "SiftAlgCrop1_2.bmp",
        #                                 self.ruta + "SiftAlgCrop3.bmp", self.ruta + "Fusion2.bmp", "SIFT",2)
        #     self.setDescriptorSecond("Sift")
        # if self.ui.comboBox_2.currentIndex() == 2:  # Brief
        #     self.imageprocess.Alignment(self.ruta + "IphotoCam3.bmp", self.ruta + "IphotoCam1.bmp",
        #                                 self.ruta + "BriefMatchPhoto2_3.bmp", self.ruta + "BriefAlgCrop1_2.bmp",
        #                                 self.ruta + "BriefAlgCrop3.bmp", self.ruta + "Fusion2.bmp", "BRIEF",2)
        #     self.setDescriptorSecond("Brief")
        # if self.ui.comboBox_2.currentIndex() == 3:  # Brick
        #     self.imageprocess.Alignment(self.ruta + "IphotoCam3.bmp", self.ruta + "IphotoCam1.bmp",
        #                                 self.ruta + "BriskMatchPhoto2_3.bmp", self.ruta + "BriskAlgCrop1_2.bmp",
        #                                 self.ruta + "BriskAlgCrop3.bmp", self.ruta + "Fusion2.bmp", "BRISK",2)
        #     self.setDescriptorSecond("Brisk")

    def setDescriptorFirst(self, alg):
        try:
            self.ui.AlgMatch1_2.setPixmap(QPixmap.fromImage(QImage(self.ruta + alg + "MatchPhoto1_2.bmp")))
            self.ui.AlgCrop1.setPixmap(QPixmap.fromImage(QImage(self.ruta + alg + "AlgCrop1.bmp")))
            self.ui.AlgCrop2.setPixmap(QPixmap.fromImage(QImage(self.ruta + alg + "AlgCrop2.bmp")))
            self.ui.AlgFusion1.setPixmap(QPixmap.fromImage(QImage(self.ruta +"Fusion1.bmp")))
        except:
            return None

    def setDescriptorSecond(self, alg):
        try:
            self.ui.AlgMatch2_3.setPixmap(QPixmap.fromImage(QImage(self.ruta + alg + "MatchPhoto2_3.bmp")))
            self.ui.AlgCropFusion1_2.setPixmap(QPixmap.fromImage(QImage(self.ruta + alg + "AlgCrop2_2.bmp")))
            self.ui.AlgCrop3.setPixmap(QPixmap.fromImage(QImage(self.ruta + alg + "AlgCrop3.bmp")))
            self.ui.AlgFusion2.setPixmap(QPixmap.fromImage(QImage(self.ruta + "Fusion2.bmp")))
        except:
            return None

def __del__(self):
        self.ui = None
