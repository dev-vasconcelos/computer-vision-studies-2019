import numpy as np
import cv2
import pickle
import logging
import time
##LOG
LOG_FILE =  "../Logs/faces.log"
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)


face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
eye_cascade  = cv2.CascadeClassifier('cascades/data/haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('cascades/data/haarcasacade_smile.xml')

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("./recognizers/face-trainner.yml")

labels = {"person_name" : 1}

with open("pickles/face-labels.pickle", "rb") as f:
    og_labels = pickle.load(f)
    labels = {v:k for k,v in og_labels.items()}

cap = cv2.VideoCapture(0) #camera ip

while (True):
    ret, frame = cap.read()
    #frame = cv2.imread('../images/4.jpg_large')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.5, 5)

    for (x,y,w,h) in faces:
        roi_gray = gray[y:y+h, x:x+w] # RegionOfInterest
        roi_color = frame[y:y+h, x:x+w]

        id_, conf = recognizer.predict(roi_gray)

        if conf >= 4 and conf <=85:
            font = cv2.FONT_HERSHEY_SIMPLEX
            name = labels[id_]
            color = (255,255,255)
            stroke = 2

            names = name.split("-")

            if name.endswith("0"):
                color = (0,0,255)
            
            cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)
            logging.debug("{'recognized':'1','name':'"+name+"'currentTime':'"+ str(time.gmtime()) + "'")
        #ok predo here goes the auto Database, with autoDatabase comes a new facetrain
        #so what do I got to do? I need to use threads, to do not create 1000 new folders
        #before faces-train.py run
        

        img_item = "7.png" # get last id + 1 . png
        cv2.imwrite(img_item, roi_color)

        if name.endswith("0"):
                color = (0,0,255)
        else:
            color = (255, 0, 0)
        stroke = 2
        end_x = x + w
        end_y = y + h
        cv2.rectangle(frame, (x,y), (end_x,end_y), color, stroke)

    ### GET INFO'S TO PUBLISH MQTT ###
    ### IS PERSON PLEASUREABLE ? LABEL ENDS WITH 1 ###

    ### PUBLISH MQTT WITH INFOS ###
    ### PUBLISH MQTT WITH INFOS ###
    
    ### TEST ###
    cv2.imshow('frame', frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

    ### TEST ###
cap.release()
cv2.destroyAllWindows()
