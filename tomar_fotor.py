import cv2
import numpy as np
import requests
import os

# Creamos las carpetas automáticamente donde se guardarán tus fotos
os.makedirs("Dataset_Vacio", exist_ok=True)
os.makedirs("Dataset_Ocupado", exist_ok=True)

URL_FOTO = "http://192.168.4.1/foto"
contador_vacio = 0
contador_ocupado = 0

print("Esperando conexión... (Asegúrate de estar en el Wi-Fi 'Estacionamiento_IA')")
print("Controles:")
print("- Presiona 'V' para guardar foto de lugar VACÍO.")
print("- Presiona 'O' para guardar foto de lugar OCUPADO.")
print("- Presiona 'Q' para salir.")

while True:
    try:
        # Pedimos la foto a la ESP32
        respuesta = requests.get(URL_FOTO, timeout=2)
        img_array = np.array(bytearray(respuesta.content), dtype=np.uint8)
        frame = cv2.imdecode(img_array, -1)
        
        # Mostramos el video en vivo
        cv2.imshow("Recolector de Datos para IA", frame)
        tecla = cv2.waitKey(1) & 0xFF
        
        # Si presionas 'v', toma la foto y la guarda en la carpeta de vacíos
        if tecla == ord('v'):
            cv2.imwrite(f"Dataset_Vacio/vacio_{contador_vacio}.jpg", frame)
            print(f"Foto VACÍO guardada! ({contador_vacio})")
            contador_vacio += 1
            
        # Si presionas 'o', toma la foto y la guarda en ocupados
        elif tecla == ord('o'):
            cv2.imwrite(f"Dataset_Ocupado/ocupado_{contador_ocupado}.jpg", frame)
            print(f"Foto OCUPADO guardada! ({contador_ocupado})")
            contador_ocupado += 1
            
        elif tecla == ord('q'):
            break
            
    except Exception as e:
        pass # Ignora si hay un pequeño corte de red

cv2.destroyAllWindows()