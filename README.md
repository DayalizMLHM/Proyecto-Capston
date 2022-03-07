# Proyecto-Capston Detector de personas y vehiculos para trailers
Integrantes del proyecto:
Hernández Moreno Miriam Lizbeth
Pérez Murillo Jose Luis

## Objetivos generales.
* Comunicar mediante un sensor una transmisión que alerte en cadena a los vehículos que se encuentren dentro de cierto rango para alertar acerca de un posible accidente.
* Evitar accidentes con vehículos pesados mediante la detección de personas u objetos próximos en puntos ciegos (peatones, motocicletas, obstáculos, etc.)
* Evitar accidentes automovilísticos provocados por los conductores que se quedan dormidos en el camino.
## Objetivos específicos
* Diseñar y construir el sistema de montaje para los sensores y microcontroladores utilizados en el sistema propuesto.
* Implementar en un microcontrolador (ESP32 o quizá otro) el sistema de control y reconocimiento facial para la interfaz vehículo/conductor.
* Implementar en un microcontrolador (ESP32 o quizá otro) el sistema de control en el volante del vehículo para la interfaz vehículo/conductor.
* Instalar y configurar un Bróker MQTT accesible desde Internet.
* Implementar el módulo de comunicaciones para el envío de datos del microcontrolador (ESP32 CAM o quizá otro) y el Bróker MQTT empleando la red de Internet.
* Implementar el módulo de comunicaciones para el envío de datos del sensor de proximidad a través de la tarjeta de desarrollo raspberry pi 4 y el bróker MQTT empleando la red de Internet.
* Implementar la aplicación WEB que permita la monitorización en tiempo real de los parámetros observados empleando Node-RED.

## Justificación
El internet de las cosas es fundamental en esta parte del proyecto ya que requiere una correcta comunicación entre sensores y dispositivos para notificar el accidente a las personas cercanas una vez que detecta la posible colisión.
Una vez que los datos sean procesados un programa automáticamente se encargará de enviar la información a la gente cercana para que tenga precaución y tome las medidas necesarias.
El sistema pretende a reducir la cantidad de accidentes por colisión provocados por un choque inicial, sin embargo, es poco útil si se implementa solamente en algunos vehículos, se debe tener en cuenta que dicho sistema tendría que estar implementado en todos los autos para que funcione de la mejor manera.
