import numpy as np
import cv2
import pickle
import os 
    
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
    #Flag para saber se rosto está cadastrado
    flagRecog = False
    pleaseable = True

    #Lê e converte a imagem para escala de cinza
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.5, 5)

    #para cada região de interesse em faces
    for (x,y,w,h) in faces:

        #Marcação do ponto de interesse
        roi_gray = gray[y:y+h, x:x+w] # RegionOfInterest
        roi_color = frame[y:y+h, x:x+w]
        
        #Passa o reconhecedor
        id_, conf = recognizer.predict(roi_gray)

        #Caso passe pela validação escreve o nome da pessoa em cima do retângulo
        if conf >= 4 and conf <=85:
            #Pessoa é cadastrada
            flagRecog = True

            #configuração da fonte e cor a destacar
            ## Mostragem em tela para debug ##
            font = cv2.FONT_HERSHEY_SIMPLEX 
            name = labels[id_] 
            color = (255,255,255) 
            stroke = 2 
            ## Mostragem em tela para debug ##

            #Se o nome terminar com 0 é uma pessoa indesejada
            if name.endswith("0"):
                pleaseable = True
                color = (0,0,255) #Mostragem em tela para debug
            
            cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA) #Mostragem em tela para debug
        
        if(flagRecog):
            pass
            print("publish reconhecido")
        else:
            pass
            bid = 0
            dirname = "generio0-1"
            print("publish desconhecido")
            #lista os diretorios da pasta de imagem
            for root, dirs, files in os.walk(image_dir):
                print("esta entrando")
                #a cada encontro com uma pasta generica, seta o id como maior
                for dire in dirs:
                    if dire.startswith("generico"):
                        print("dire :::" + dire)
                        dire = dire[:-2]
                        bidantes = int(str(dire).strip("generico"))
                        print("bid antes strip generico:::" + str(bidantes))
                        if(bidantes > bid or bidantes == bid):
                            bid = bidantes + 1
                        print("bid antes" + str(bidantes))
                        print("bid atual" + str(bid))
                dirname = "generico"+str(bid)+"-1"
            #CRIAR PASTA GENERICO+IDCORRESPONDENTE-1
            os.mkdir(os.path.join(image_dir, dirname))
            
            #ADICONAR IMAGEM 1.png
            img_item = image_dir+"/"+dirname+"/"+"1.png" #get last id + 1 . png
            cv2.imwrite(img_item, roi_color)
            print("DESCONHECIDO SALVADO EM:"+ str(img_item))
            
            #TREINAR I.A.
            #os.system('python faces-train.py')

        ## Mostragem em tela para debug ##
        if name.endswith("0"):
                color = (0,0,255)
        else:
            color = (255, 0, 0)
        stroke = 2
        ## Mostragem em tela para debug ##

        ## Região de interesse ## 
        end_x = x + w
        end_y = y + h
        ## Região de interesse ##
        cv2.rectangle(frame, (x,y), (end_x,end_y), color, stroke)

    cv2.imshow('frame', frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

    ### TEST ###
cap.release()
cv2.destroyAllWindows()
