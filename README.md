# 🚗 Asistente de Estacionamiento Autónomo con Visión Artificial

Prototipo de vehículo autónomo capaz de navegar y estacionarse de manera automática mediante el uso de Inteligencia Artificial (Visión Computacional) y control mecatrónico.

Este proyecto fue desarrollado como práctica integradora de la carrera de Ingeniería Mecatrónica en la Facultad de Ingeniería Mecánica y Eléctrica (FIME), UANL.

## 🛠️ Arquitectura del Sistema
El proyecto se divide en dos cerebros principales para separar la carga de procesamiento del control físico:

1. **Cerebro Lógico (Procesamiento de IA):** Un script en Python que se ejecuta en una computadora local. Recibe video en vivo vía Wi-Fi, procesa los frames usando una red neuronal convolucional (TensorFlow/Keras) para detectar cajones de estacionamiento vacíos u ocupados, y envía comandos de navegación por protocolo HTTP.
2. **Cerebro Físico (Control Mecatrónico):** Un Arduino Uno que administra la potencia de los motores DC mediante un Puente H (L298N), gestiona la telemetría del sensor ultrasónico (HC-SR04) para el frenado de emergencia, y ejecuta las rutinas de giro y aparcamiento basadas en la cinemática del chasis.

## ⚙️ Hardware Utilizado
* Chasis de robot 2WD con motores DC (Relación 1:48).
* Microcontrolador Arduino Uno.
* Módulo ESP32-CAM (Configurado como Access Point y servidor de imágenes).
* Controlador de motores Puente H L298N.
* Sensor Ultrasónico HC-SR04.
* Módulo Step-Down LM2596S (Para estabilizar caídas de tensión).
* Batería Li-Po / Eliminador 12V.

## 💻 Requisitos de Software
Para ejecutar el script de visión en tu computadora local, necesitas instalar las siguientes dependencias de Python:
```bash
pip install opencv-python numpy requests tensorflow
```
## 🚀 Cómo ejecutarlo
1. **Electrónica:** Carga el código `.ino` en el Arduino y el código del servidor web en la ESP32-CAM.
2. **Red:** Energiza el vehículo. La ESP32-CAM creará automáticamente una red Wi-Fi local llamada `Estacionamiento_IA`.
3. **Conexión:** Conecta tu computadora a dicha red (Password: `12345678`).
4. **Ejecución:** Corre el script principal de Inteligencia Artificial:
```bash
python ia_carrito.py
```
5. **Seguridad: Presiona la tecla `Q` en la ventana de video en cualquier momento para detener los motores de emergencia.

Autor
Bryant Alberto Martínez Montero
Estudiante de Ingeniería Mecatrónica - FIME, UANL.
