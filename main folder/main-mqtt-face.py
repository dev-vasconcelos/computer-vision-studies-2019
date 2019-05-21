import numpy as np
import cv2
import pickle
import os 
import MqttMessager as mqttMessi
import logging
import time
##LOG
LOG_FILE =  "../Logs/main-mqtt-face.log"
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)

#Mqtt Initializer
messi = mqttMessi.MqttMessager("192.168.15.157", 1883)

#Diretórios
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR, "faces")

#Cascades de reconhecimento
face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
eye_cascade  = cv2.CascadeClassifier('cascades/data/haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('cascades/data/haarcasacade_smile.xml')

#Arquivo de reconhecimento
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("./recognizers/face-trainner.yml")

#Lista com os nomes
labels = {"person_name" : 1}

#Popular lista
with open("pickles/face-labels.pickle", "rb") as f:
    og_labels = pickle.load(f)
    labels = {v:k for k,v in og_labels.items()}

#Ler vídeo
cap = cv2.VideoCapture(0) #camera ip

#Inicialização de variaveis chatas
name = "generico"
flagRecog = False

while (True):
    flagRecog = False
    pleaseable = True

    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.5, 5)

    for (x,y,w,h) in faces:
        ## Região de interesse ## 
        end_x = x + w
        end_y = y + h
        
        color = (255,0,0)
        stroke = 2
        cv2.rectangle(frame, (x,y), (end_x,end_y), color, stroke)
        ## Região de interesse ##

        roi_gray = gray[y:y+h, x:x+w] # RegionOfInterest
        roi_color = frame[y:y+h, x:x+w]
        
        id_, conf = recognizer.predict(roi_gray)

        if conf >= 4 and conf <=85:
            flagRecog = True
            name = labels[id_] 
            
            #Se o nome terminar com 0 é uma pessoa indesejada
            if name.endswith("0"):
                pleaseable = False

            font = cv2.FONT_HERSHEY_SIMPLEX
            color = (255,255,255)
            stroke = 2 
            cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)
                
        if(flagRecog):
            pass
            messi.publishMessage("maincore/smart","{'recognized':'1','name':'"+name[:-2]+"','pleaseable':'"+str(pleaseable)+"'}")
            ##CONVERSAR COM PIAZADA... DEIXAR ISSO SOLTO NÃO VAI GERAR LOG DEMAIS?
            logging.debug("{'recognized':'1','name':'"+name[:-2]+"','pleaseable':'"+str(pleaseable)+"','RectangleDimension':'(x,y,end_x,end_y):("+str(x)+","+str(y)+","+str(end_x)+","+str(end_y)+")','currentTime':'"+ str(time.gmtime()) + "'")
        else:
            pass
            bid = 0
            dirname = "generio0-1"
            messi.publishMessage("maincore/smart","{'recognized':'0','name':'"+name[:-2]+"','pleaseable':'"+str(pleaseable)+"'}")
            logging.debug("recognized:0;name:NONANME;pleaseable:"+str(pleaseable)+";RectangleDimension(x,y,end_x,end_y):("+str(x)+","+str(y)+","+str(end_x)+","+str(end_y)+");currentTime:"+ str(time.gmtime()))

            #lista os diretorios da pasta de imagem
            for root, dirs, files in os.walk(image_dir):
                #a cada encontro com uma pasta generica, seta o id como maior
                for dire in dirs:
                    if dire.startswith("generico"):
                        dire = dire[:-2]
                        bidantes = int(str(dire).strip("generico"))
                        if(bidantes > bid or bidantes == bid):
                            bid = bidantes + 1
                dirname = "generico"+str(bid)+"-1"
            #CRIAR PASTA GENERICO+IDCORRESPONDENTE-1
            os.mkdir(os.path.join(image_dir, dirname))
            
            #ADICONAR IMAGEM 1.png
            img_item = image_dir+"/"+dirname+"/"+"1.png" #get last id + 1 . png
            cv2.imwrite(img_item, roi_color)
            logging.debug("DESCONHECIDO SALVADO EM:"+ str(img_item))
            
            #TREINAR I.A.
            #os.system('python faces-train.py')
    
    cv2.imshow('frame', frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

    ### TEST ###
cap.release()
cv2.destroyAllWindows()
