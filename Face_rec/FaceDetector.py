import numpy as np
import cv2

robot_1 = cv2.imread('robot-face_1f916.png',-1)
resfactor = 1

detector= cv2.CascadeClassifier('C:\Users\utente\Desktop\Face_rec\haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

while(True):
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)
    #width, height = cv2.GetSize(img)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        res_h = int(resfactor * h)
        res_w = int(resfactor * w)
        delta_x = int(0.5*(res_w - w))
        delta_y = int(0.5*(res_h - h))
        x_face = x - delta_x
        y_face = y - delta_y
        robot_1_res = cv2.resize(robot_1,(res_w,res_h))
        
        alpha_s = robot_1_res[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s

        for c in range(0, 3):
            img[y:y+res_h, x:x+res_w, c] = (alpha_s * robot_1_res[:, :, c] + alpha_l * img[y:y+res_h, x:x+res_w, c])
        

    cv2.imshow('frame',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()