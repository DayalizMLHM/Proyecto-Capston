#Librerias necesarias
from paho.mqtt import client as mqtt_client
from scipy.spatial import distance
from imutils import face_utils
from datetime import datetime
import numpy as np
import pygame #Para hacer sonar la alarma
import time
import dlib
import cv2
import random
import getpass
import os

#Variables para publicar en MQTT
broker = 'broker.hivemq.com'
port = 1883
topic = "somnolencia/luisangel"
estado = 0 # 0 Despierto - 1 Dormido
#Generar cliente para mqtt
client_id = f'python-mqtt-{random.randint(0, 100)}'

#Inicializar pygame y reproductor de audio (cargar)
pygame.mixer.init()
pygame.mixer.music.load('audio/alarma.mp3')

#Umbral mínimo de la relación de aspecto de los ojos por debajo del cual se activa la alarma
EYE_ASPECT_RATIO_THRESHOLD = 0.3

#Fotogramas consecutivos mínimos en los que la proporción de ojos está por debajo del umbral para que se active la alarma
EYE_ASPECT_RATIO_CONSEC_FRAMES = 50

#Cuenta No. de fotogramas consecutivos por debajo del valor umbral
COUNTER = 0

#Cargue la cascada de caras que se usará para dibujar un rectángulo alrededor de las caras detectadas.

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

#Función para conectar al broker MQTT
def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

#Función para publicar en el broker MQTT, se utiliza un topic conocido para poder leerlo por fuera
def publish(client, topic, counter):
    #usr_name = getpass.getuser()
    usr_name = "Luis Angel Sánchez Hernández"
    #formato_Mensaje: ' nombre;counter;fecha '
    msg = usr_name + ";"
    msg += str(counter) + ";"
    msg += str(datetime.now())
    
    print(msg)
    result = client.publish(topic, msg)
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

def enviar_mensaje_central(topic, counter):
    client = connect_mqtt()
    client.loop_start()
    publish(client, topic, counter)
    client.loop_stop(True)


#Esta función calcula y devuelve la relación de aspecto de los ojos
def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])

    ear = (A+B) / (2*C)
    return ear

#Cargue el detector y el predictor de rostros, utiliza el archivo predictor de forma dlib
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('../shape_predictor_68_face_landmarks.dat')

#Extraiga índices de puntos de referencia faciales para el ojo izquierdo y derecho
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS['left_eye']
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']

#Inicie la captura de video de la cámara web
video_capture = cv2.VideoCapture(0)

#Dé algo de tiempo para que la cámara se inicialice (no es necesario)
time.sleep(2)

os.system("lxterminal -e 'python3 distancia.py'")

while(True):
    #Lea cada cuadro y gírelo, y conviértalo a escala de grises
    ret, frame = video_capture.read()
    frame = cv2.flip(frame,1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Detecta puntos faciales a través de la función de detector.
    faces = detector(gray, 0)

    #Detectar rostros a través de haarcascade_frontalface_default.xml
    face_rectangle = face_cascade.detectMultiScale(gray, 1.3, 5)

    #Dibuja un rectángulo alrededor de cada cara detectada
    for (x,y,w,h) in face_rectangle:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

    #Detecta puntos faciales
    for face in faces:

        shape = predictor(gray, face)
        shape = face_utils.shape_to_np(shape)

        #Obtener las coordenadas del ojo izquierdo y derecho
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]

        #Calcula aspecto de ojos
        leftEyeAspectRatio = eye_aspect_ratio(leftEye)
        rightEyeAspectRatio = eye_aspect_ratio(rightEye)

        eyeAspectRatio = (leftEyeAspectRatio + rightEyeAspectRatio) / 2

        #Use el casco para eliminar las discrepancias de contorno convexo y dibuje la forma de los ojos alrededor de los ojos
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

        #Detectar si la relación de aspecto de los ojos es inferior al umbral
        if(eyeAspectRatio < EYE_ASPECT_RATIO_THRESHOLD):
            COUNTER += 1
            #Si el No. de fotogramas es mayor que el umbral de fotogramas
            if COUNTER >= EYE_ASPECT_RATIO_CONSEC_FRAMES:
                estado = 1
                enviar_mensaje_central(topic, estado);
                pygame.mixer.music.play(-1)
                cv2.putText(frame, "Somnolencia, peligro", (150,200), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,255), 2)
        else:
            pygame.mixer.music.stop()
            COUNTER = 0
            if(estado == 1):
                estado = 0
                enviar_mensaje_central(topic, estado);

    #Mostrar video
    cv2.imshow('Video', frame)
    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break

#Finalmente, cuando termine la captura de video, suelte la captura de video y destruya Todas las ventanas
video_capture.release()
cv2.destroyAllWindows()


