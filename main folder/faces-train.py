import cv2
import os
import numpy as np
from PIL import Image
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR, "faces")

face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

current_id = 0
labels_ids = {} # biblio
y_labels = []
x_labels = []

for root, dirs, files in os.walk(image_dir):
    for file in files:
        if file.endswith("png") or file.endswith("jpg") or file.endswith("jpg_large"):
            path = os.path.join(root, file)
            label = os.path.basename(root).replace(" ","-").lower()

            if not label in labels_ids:
                labels_ids[label] = current_id
                current_id += 1
            id_ = labels_ids[label]

            pil_image = Image.open(path).convert("L") # Why? Serious...
            size = (550, 550)
            final_image = pil_image.resize(size, Image.ANTIALIAS)
            image_array = np.array(final_image, "uint8")
            
            faces = face_cascade.detectMultiScale(image_array, 1.5,5)

            for (x,y,w,h) in faces:
                roi = image_array[y:y+h, x:x+w]
                x_labels.append(roi)
                y_labels.append(id_)

with open("pickles/face-labels.pickle", "wb") as f:
    pickle.dump(labels_ids, f)

recognizer.train(x_labels, np.array(y_labels))
recognizer.save("recognizers/face-trainner.yml")