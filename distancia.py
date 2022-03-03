import RPi.GPIO as GPIO
import numpy as np
import time
import cv2

#cap = cv2.VideoCapture('http://192.168.100.34:81/stream') #Cambiar por la IP y puerto asignados por tu modem

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

print("Inicia la toma de datos")

try:
	while True:
		print("acerque el objeto para medir la distancia")
		distance=CalcDistancia()
		print( ' distanciacalculada ' + str(distance) )
		time.sleep(2)
		# si se alcanza cierta distancia sonar alarma e iniciar transmicion de la ESP32
		if(distance <= 100): #Un metro de distancia
			cap = cv2.VideoCapture('http://192.168.100.34:81/stream') #Cambiar por la IP y puerto asignados
			print("Hay un objeto demaciado cerca")
			while(True):
				ret, frame = cap.read()
				cv2.imshow('ESP32CAM',frame)
				distance=CalcDistancia()
				print( ' entro ' + str(distance) )
				time.sleep(0.1)
				if cv2.waitKey(1) & 0xFF == ord('q') or distance>100:
					#cv2.destroyWindow('ESP32CAM')
					cap.release()
					cv2.destroyAllWindows()
					break

except KeyboardInterrupt:
	print('\n' + 'termina la captura de datos.' + '\n')
	GPIO.cleanup()

