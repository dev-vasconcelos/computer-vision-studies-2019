import numpy as np
import cv2
import pickle
import os
import MqttMessager as mqttmessi

class FaceRecognizer:
    
    def __init__(self):
        self.cap = cv2.VideoCapture(0) #camera ip
        self.messi = mqttmessi.MqttMessager("192.168.1.18", 1883)
        self.popList()

    def popList(self):
        #Diretórios
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.image_dir = os.path.join(self.BASE_DIR, "faces")

        #Cascades de reconhecimento
        self.face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
        self.eye_cascade  = cv2.CascadeClassifier('cascades/data/haarcascade_eye.xml')
        self.smile_cascade = cv2.CascadeClassifier('cascades/data/haarcasacade_smile.xml')

        #Arquivo de reconhecimento
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read("./recognizers/face-trainner.yml")

        #Lista com os nomes
        self.labels = {"person_name" : 1}

        #Popular lista
        with open("pickles/face-labels.pickle", "rb") as f:
            self.og_labels = pickle.load(f)
            self.labels = {v:k for k,v in self.og_labels.items()}

    def recogFaces(self):
        #Flag para saber se rosto esta cadastrado
        self.flagRecog = False
        self.pleaseable = True

        #le e converte imagem para cinza
        ret, frame = self.cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.5, 5)

        for(x,y,w,h) in faces:
            roi_gray = gray[y:y+h, x:x+w] #Regiao de interesse
            roi_color = frame[y+y+h, x:x+w]

            #passa o reconhecedor
            id_, conf = self.recognizer.predict(roi_gray)

            #Caso passe pela validação escreve o nome da pessoa
            if conf >= 4 and conf <= 85 :
                self.flagRecog = True
                self.name = self.labels[id_]

                if self.name.endswith("0"):
                    self.pleaseable = True
                    
            if(self.flagRecog):
                self.messi.publishMessage("maincore/teste", "reconhecido")
                pass
            else:
                self.messi.publishMessage("maincore/teste", "desconhecido")
                bid = 0
                dirname = "generico0-1"
                #a cada encontro com pasta generica, muda ID, ao fina persiste a pasta
                for root, dirs, files in os.walk(self.image_dir):
                    for ds in dirs:
                        if ds.startswith("generico"):
                            ds = ds[:-2]
                            bidantes = int(str(ds).strip("generico"))
                            if(bidantes > bid or bidantes == bid):
                                bid = bidantes + 1
                    dirname = "generico"+str(bid)+"-1"
                    os.mkdir(os.path.join(self.image_dir, dirname))

                    #Adicionar imagem n1
                    img_item = self.image_dir+"/"+dirname+"/"+"1.png"
                    cv2.imwrite(img_item, roi_color)

                    #Supostamente deveria treinar I.A
                    pass

                    #Regiao de interesse:
                    end_x = x + w
                    end_y = y + h
                    #cv2.rectangle(frame, (x,y), (end_x,end_y), color=(255,255,255), stroke=2)
        cv2.imshow('frame', frame)
        
if __name__ == "__main__":
    fr = FaceRecognizer()

    while(True):
        fr.recogFaces()
        if(cv2.waitKey(20) & 0xFF == ord('q')):
            fr.cap.release()
            cv2.destroyAllWindows()
