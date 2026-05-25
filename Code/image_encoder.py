import face_recognition
import os
import cv2



image_name = []
image_paths = []
folder_path = r"D:\CODING STUFFS\PROJECTS\ATTENDANCE-SYSTEM\Students"


def folder():
    
    for filename in os.listdir(folder_path):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            img_path = os.path.join(folder_path, filename)
            image_paths.append(img_path)
            image_name.append(os.path.splitext(filename)[0])


def img_name():
    return image_name



def encoder():
    folder()
    img_encode = []
    for i in image_paths:
        uimg=cv2.imread(i)
        uimg = cv2.cvtColor(uimg, cv2.COLOR_BGR2RGB)
        uimg=cv2.resize(uimg,(0,0),fx=0.25,fy=0.25)
        code = face_recognition.face_encodings(uimg)[0]
        img_encode.append(code)
    return img_encode

