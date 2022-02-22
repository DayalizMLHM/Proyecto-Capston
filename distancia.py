import RPi.GPIO as GPIO
import numpy as np
import time
import cv2
from datetime import datetime
import pygame

#Initialize Pygame, load music and streaming video
pygame.mixer.init()
pygame.mixer.music.load('audio/alert.mp3')
cap = cv2.VideoCapture('http://192.168.1.74:81/stream') #Cambiar por la IP y puerto asignados por tu modem

#Configuraciones para leer el sensor ultrasónico
GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 23
GPIO_ECHO    = 24
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)
GPIO.setup(GPIO_ECHO,GPIO.IN)
GPIO.output(GPIO_TRIGGER, False)

def CalcDistancia():
	GPIO.output(GPIO_TRIGGER,True)
	time.sleep(0.00001)
	GPIO.output(GPIO_TRIGGER,False)
	start = time.time()
	while GPIO.input(GPIO_ECHO)==0:
		start = time.time()
	while GPIO.input(GPIO_ECHO)==1:
		stop = time.time()
	elapsed = stop-start
	distance = (elapsed * 34300)/2
	
	return distance

sFileStamp = time.strftime('%Y%m%d%H')
sFileName = '\out' + sFileStamp + '.txt'
f=open(sFileName, 'a')
f.write('TimeStamp,Value' + '\n')
print("Inicia la toma de datos")

try:
	while True:
		print("acerque el objeto para medir la distancia")
		# si se alcanza cierta distancia sonar alarma e iniciar transmicion de la ESP32
		while(CalcDistancia() < 200): #Dos metros de distancia
			pygame.mixer.music.play(-1)
			print("Hay un objeto demaciado cerca")
			while(True):
				ret, frame = cap.read()
				cv2.imshow('ESP32CAM',frame)
				if cv2.waitKey(1) & 0xFF == ord('q') or CalcDistancia()>200:
					break
		pygame.mixer.music.stop()
		
		sTimeStamp = time.strftime('%Y%m%d%H%M%S')
		f.write(sTimeStamp + ',' + str(distance) + '\n')
		print( sTimeStamp + ' ' + str(distance) )
		time.sleep(1)
		sTmpFileStamp = time.strftime('%Y%m%d%H')
		if sTmpFileStamp != sFileStamp:
			f.close
			sFileName = 'out/' + sTmpFileStamp + '.txt'
			f=open(sFileName, 'a')
			sFileStamp = sTmpFileStamp
			print("creando el archivo")
		   	

except KeyboardInterrupt:
	print('\n' + 'termina la captura de datos.' + '\n')
	f.close
	GPIO.cleanup()

#Finally when video capture is over, release the video capture and destroyAllWindows
cap.release()
cv2.destroyAllWindows()
