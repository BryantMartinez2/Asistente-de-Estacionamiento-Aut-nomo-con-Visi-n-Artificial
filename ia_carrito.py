import cv2
import numpy as np
import requests
from keras.models import load_model
import time

# --- 1. CONFIGURACIÓN DE RED ---
# La IP de la ESP32 en modo módem (Access Point)
URL_FOTO = "http://192.168.4.1/foto"
URL_COMANDO = "http://192.168.4.1/comando"

# --- 2. CARGAR EL CEREBRO (IA) ---
print("Cargando modelo de Inteligencia Artificial... (puede tardar unos segundos)")
# Asegúrate de que los nombres de los archivos coincidan con los que descargues
modelo = load_model("keras_model.h5", compile=False)
etiquetas = open("labels.txt", "r").readlines()
print("¡Modelo cargado con éxito!")

# --- 3. FUNCIÓN DE COMUNICACIÓN ---
def enviar_orden(letra):
    try:
        # Enviamos la petición web súper rápido (1 segundo de tolerancia)
        requests.get(f"{URL_COMANDO}?letra={letra}", timeout=1)
    except:
        pass # Si la red parpadea, ignoramos el error para no trabar el programa

# --- 4. CICLO PRINCIPAL DE VISIÓN ---
print("Conéctate a la red Wi-Fi 'Carrito_PIA' para empezar...")

while True:
    try:
        # A. Pedir foto a la ESP32
        respuesta = requests.get(URL_FOTO, timeout=2)
        img_array = np.array(bytearray(respuesta.content), dtype=np.uint8)
        frame = cv2.imdecode(img_array, -1) # Convertir a imagen de OpenCV

        # B. Preparar la imagen para la IA (Teachable Machine pide 224x224)
        imagen_redimensionada = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)
        imagen_normalizada = np.asarray(imagen_redimensionada, dtype=np.float32).reshape(1, 224, 224, 3)
        imagen_normalizada = (imagen_normalizada / 127.5) - 1

        # C. La IA decide qué está viendo
        prediccion = modelo.predict(imagen_normalizada, verbose=0)
        indice_clase = np.argmax(prediccion)
        nombre_clase = etiquetas[indice_clase][2:].strip() # Quitar el número del inicio
        confianza = prediccion[0][indice_clase]

        # D. LÓGICA DE CONTROL (Mecatrónica)
        # Asumiendo que nombraste tus clases "Lugar_Vacio" y "Lugar_Ocupado"
        if nombre_clase == "Lugar_Vacio" and confianza > 0.85:
            cv2.putText(frame, "ORDEN: ESTACIONAR (E)", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            enviar_orden("E")
            
            # Pausa para dejar que el carrito termine su maniobra física
            cv2.imshow("Cámara del Carrito", frame)
            cv2.waitKey(1)
            time.sleep(3) 
            
        else:
            cv2.putText(frame, "ORDEN: AVANZAR (A)", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            enviar_orden("A")

        # E. Mostrar video en tu pantalla
        texto_ia = f"{nombre_clase} ({int(confianza*100)}%)"
        cv2.putText(frame, texto_ia, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.imshow("Cámara del Carrito", frame)

    except Exception as e:
        # Si no hay conexión, muestra este mensaje sin crashear
        print("Esperando video del carrito... Revisa tu conexión Wi-Fi.")
        time.sleep(1)

    # Presiona 'q' en tu teclado para detener todo de emergencia
    if cv2.waitKey(1) & 0xFF == ord('q'):
        enviar_orden("S") # Ordenamos detener los motores
        break

cv2.destroyAllWindows()