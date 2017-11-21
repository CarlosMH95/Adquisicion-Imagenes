import cv2
import pypylon.pylon as py
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qt import *
from PyQt5.QtWidgets import *
import numpy as np
import os
import pywt

import pypylon.pylon as pylon
tlfactory = pylon.TlFactory.GetInstance()
ptl = tlfactory.CreateTl('BaslerGigE')
detected_devices = ptl.EnumerateDevices()
print('%i devices detected:' % len(detected_devices))
print([d.GetFriendlyName() for d in detected_devices])
print(' ')
icam = py.InstantCamera(ptl.CreateDevice(detected_devices[0]))
xcam = py.InstantCamera(ptl.CreateDevice(detected_devices[1]))

icam.Open()

img = icam.GrabOne(4000)

print(img)
icam.Close()
xcam.Open()
xcam.PixelFormat = "BGR8"
#xcam.properties['PixelFormat'] = 'BG12'
img2 = xcam.GrabOne(4000)

print (img2)
xcam.Close()
# data  = np.array(img2.GetBuffer()).astype(np.uint8)
# image = data.reshape(img2.GetHeight(), img2.GetWidth())
# cv2.imshow('image', image)
# cv2.waitKey(0)
# print(image)
img = img.Array
img2 = img2.Array
#print(img)

#print(img2)
print(img.shape)
print(img2.shape)
cv2.imshow('img', img)
cv2.waitKey(0)
cv2.imshow('img', img2)
cv2.waitKey(0)
cv2.destroyAllWindows()