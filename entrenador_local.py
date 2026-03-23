import cv2
import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

print("Iniciando entrenamiento local de IA...")

datos = []
etiquetas = []

# 1. Cargar fotos del lugar vacío
print("Leyendo fotos de lugares vacíos...")
for nombre_archivo in os.listdir("Dataset_Vacio"):
    ruta = os.path.join("Dataset_Vacio", nombre_archivo)
    img = cv2.imread(ruta)
    if img is not None:
        img = cv2.resize(img, (224, 224))
        datos.append(img)
        etiquetas.append(0) # 0 significa Vacío

# 2. Cargar fotos del lugar ocupado
print("Leyendo fotos de lugares ocupados...")
for nombre_archivo in os.listdir("Dataset_Ocupado"):
    ruta = os.path.join("Dataset_Ocupado", nombre_archivo)
    img = cv2.imread(ruta)
    if img is not None:
        img = cv2.resize(img, (224, 224))
        datos.append(img)
        etiquetas.append(1) # 1 significa Ocupado

# 3. Preparar los datos matemáticamente (Igual que Teachable Machine)
print("Procesando imágenes...")
datos = (np.array(datos, dtype=np.float32) / 127.5) - 1
etiquetas = np.array(etiquetas)

# 4. Crear la Red Neuronal (El Cerebro)
modelo = Sequential([
    Conv2D(16, (3,3), activation='relu', input_shape=(224, 224, 3)),
    MaxPooling2D(2,2),
    Conv2D(32, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    Flatten(),
    Dense(64, activation='relu'),
    Dense(2, activation='softmax')
])

modelo.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# 5. Entrenar a la IA
print("\n¡Comenzando el entrenamiento! (Esto tomará unos segundos)...")
modelo.fit(datos, etiquetas, epochs=10)

# 6. Guardar los archivos idénticos a los de Google
print("\nGuardando modelo...")
modelo.save("keras_model.h5")

with open("labels.txt", "w") as f:
    f.write("0 Lugar_Vacio\n1 Lugar_Ocupado")

print("¡ÉXITO ROTUNDO! Archivos keras_model.h5 y labels.txt creados.")
print("Ya puedes ejecutar tu archivo ia_carrito.py")