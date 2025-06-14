import cv2
import torch
import serial
import time 



# Fix Windows path issue
from pathlib import Path
import pathlib
pathlib.PosixPath = pathlib.WindowsPath


#initialisasi port detection
#ports = list(serial.tools.list_ports.comports())
ser = serial.Serial('COM6', baudrate= 9600, timeout = 0.5)


# Inisialisasi model YOLOv5
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best2.pt')  


# Buka video stream
cap = cv2.VideoCapture("http://192.168.0.100:81/stream")


while True:
    ret, frame = cap.read()
    if not ret:
        print("Gagal menerima frame - cek koneksi/kamera")
        break
    
    #perbesar frame
    frame = cv2.resize(frame, (800, 600))


    #mirror y
    frame = cv2.flip(frame, 1)

    #mirror
    frame = cv2.flip(frame, 0)

    # Deteksi objek
    results = model(frame)
    
    # Render hasil deteksi
    detected_frame = results.render()[0]
    
    # Tampilkan hasil
    cv2.imshow('ESP32-CAM with YOLOv5', detected_frame)
    
    # Tekan 'q' untuk keluar
    if cv2.waitKey(1) == ord('q'):
        break
    
    for pred in results.pred:
        for det in pred:
            confidance = det[4].item()
            class_id = int(det[5].item())
            class_name = results.names[class_id]
                
            if confidance >= 0.50 and class_name == "Car":
                ser.write(b'open_gate\n')
            else:
                ser.write(b'not_detected\n')
                
         






# Cleanup
cap.release()
cv2.destroyAllWindows()
