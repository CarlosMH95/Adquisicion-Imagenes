import cv2
import numpy as np
import pypylon.pylon as PYLON

cameras = []

try:
    #create an instant camera object with the camera devices founded
    devices = PYLON.TlFactory.GetInstance().EnumerateDevices()
    for deviceInfo in devices:
        device = PYLON.TlFactory.GetInstance().CreateDevice(deviceInfo)
        camera = PYLON.InstantCamera(device)

        #print the model name of the camera
        print("Using device: "+camera.GetDeviceInfo().GetModelName())

        #open the camera before accessing any parameters
        camera.Open()

        #define frame rate acquired
        camera.AcquisitionFrameRateEnable.SetValue(True)
        camera.AcquisitionFrameRateAbs.SetValue(3.0)

        #start grabbing
        camera.StartGrabbing(PYLON.GrabStrategy_LatestImageOnly)

        cameras.append(camera)

    # create a pylon ImageFormatConverter object
    formatConverter = PYLON.ImageFormatConverter()
    # specify the output pixel format
    formatConverter.OutputPixelFormat.SetValue(PYLON.PixelType_BGR8packed)
    
    while True:#camera.IsGrabbing():
        i = 1
        for camera in cameras:
            grabResult = camera.RetrieveResult(5000, PYLON.TimeoutHandling_ThrowException)
            if grabResult.GrabSucceeded():
                pylonImage = formatConverter.Convert(grabResult)
                rows = grabResult.GetHeight()
                cols = grabResult.GetWidth()
                cvImage = np.frombuffer(pylonImage.GetBuffer(), np.uint8).reshape(rows, cols, 3)
                resized = cv2.resize(cvImage, (700, 500))
                cv2.imshow('frame {}'.format(i), resized)
                i = i + 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    for camera in cameras:
        camera.Close()
        print("Closed")

    cv2.destroyAllWindows()


except Exception as e:
    print(e)
    for camera in cameras:
        if camera.IsOpen():
            camera.Close()
            print("Closed")

