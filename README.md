# Proyecto-Capstone: Sistema de prevención de accidentes para vehículos pesados

## Integrantes del proyecto:
* Hernández Moreno Miriam Lizbeth
* Pérez Murillo Jose Luis
* Sánchez Hernández Luis Angel

## Descripción del proyecto: 
En vehículos de gran tamaño, es normal que los conductores tengan muchos puntos ciegos que podrían provocar un terrible accidente, como se muestra a continuación:
![image](https://user-images.githubusercontent.com/57678190/156950314-4c2b821d-7d2b-4de2-8325-ccd1cd20b200.png)
![image](https://user-images.githubusercontent.com/57678190/156950545-39770f57-90d2-4898-b916-ad370149adad.png)

Es por eso que se propone colocar sensores que calculen la distancia para mostrar al conductor con la ESP32Cam cuando algo esté extremadamente cerca, así mismo, dentro de la cabina se colocaría la cámara con la cual se realizará la detección de somnolencia.

## Objetivos generales.
* Monitorear con una cámara al operador del vehículo, mediante un detector de somnolencia.
* Monitorear con un sensor ultrasónico la parte frontal del vehículo. 

## Objetivos específicos:
* Diseñar y construir el sistema de montaje para la cámara y el microcontrolador utilizado en el sistema propuesto.
* Implementar en un microcontrolador el sistema de control y detector de somnolencia para la interfaz vehículo/conductor.
* Implementar en un microcontrolador el sistema de control para un sensor ultrasónico.
* Instalar y configurar un Bróker MQTT accesible desde Internet.
* Implementar un dashboard que permita la monitorización de “tiempo real” el estado del conductor.
* Implementar una página web que permita captar video cuando el sensor ultrasónico detecte un nivel corto de proximidad.

## Justificación

Como anteriormente se mencionó este proyecto está pensado para disminuir la cantidad de accidentes viales que son causados por vehículos de gran tamaño, centrándose en primer lugar en aquellos que son provocados por el cansancio excesivo en los operadores, debido a las largas distancias que deben recorrer para llegar a sus destinos; como también de los puntos ciegos que este tipo de vehículos poseen.
Es aquí cuando los avances tecnológicos pueden ayudar y mediante el internet de las cosas comunicar el estado actual del conductor y del vehículo hacia una central de monitoreo.

## Productos:
* Alerta de cansancio: Monitorear el estado del conductor y dar una alerta cuando este comience a presentar un nivel elevado de somnolencia. 
* Dashboard en Node-Red: La emisión de la alerta enviara un mensaje a la central de monitoreo indicando el estado actual del conductor identificado por un id.
* Detector de objetos cercanos: Control de objetos cercanos al vehículo que iniciara la transmisión-envio de datos por sensor radiofrecuencia

## Servicios:
* Identificar el estado de alerta del conductor.
* Monitorización en tiempo real del estatus del vehículo.
* Monitorización de los objetos cercanos al área del vehículo.


## Dispositivos utilizados para realizar pruebas de ejecución
* Raspberry Pi4B
* ESP32CAM
* Webcam Game Factor WG400
* Bocinas BOC-067
* Sensor ultrasónico
* Computadora

## Limitaciones técnicas
Debido a lo que este proyecto pretende hacer, se puede puede ver limitado debido a algunos factores como: la potencia del microcontrolador que se propone utilizar y que para subir la señal se tiene que conectar a una red wifi, lo que implica una complejidad de diseño y presupuesto aún mayor. Entonces, si se llegan a mejorar estas limitantes se presentaría un producto con menores perdidas en los datos.
Otra de las limitaciones a considerar es el envió de datos del sensor ultrasónico, dado que, al ser un sensor de mínima capacidad de rango para la detección de objetos cercanos, podría emitir una falsa alarma. 

## Librerías utilizadas
* numpy
* opencv
* dlib
* imutils
* getpass
* paho-mqtt
* pygame

## Referencias
* Resumen boletines. (s/f). Instituto Mexicano del Transporte. Recuperado el 7 de marzo de 2022, de https://imt.mx/resumen-boletines.html?IdArticulo=334&IdBoletin=120
* Rosebrock, A. (2017, mayo 8). Drowsiness detection with OpenCV. PyImageSearch. https://pyimagesearch.com/2017/05/08/drowsiness-detection-opencv/
* Soukupová, T. (s/f). Real-time eye blink detection using facial landmarks. Uni-lj.si. Recuperado el 7 de marzo de 2022, de http://vision.fe.uni-lj.si/cvww2016/proceedings/papers/05.pdf

