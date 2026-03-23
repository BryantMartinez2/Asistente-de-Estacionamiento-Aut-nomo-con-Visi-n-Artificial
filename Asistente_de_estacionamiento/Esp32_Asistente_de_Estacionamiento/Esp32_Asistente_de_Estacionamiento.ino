#include "esp_camera.h"
#include <WiFi.h>
#include <WebServer.h>

// --- 1. PINES DE LA CÁMARA (AI THINKER) ---
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27
#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

// Crear el servidor web en el puerto 80
WebServer server(80);

// --- 2. FUNCIONES DEL SERVIDOR ---

void enviarFoto() {
  camera_fb_t * fb = esp_camera_fb_get();
  
  if (!fb) {
    server.send(500, "text/plain", "Fallo al capturar imagen");
    return;
  }
  
  // FORMA CORRECTA Y SEGURA DE ENVIAR LA IMAGEN EN ESP32
  server.setContentLength(fb->len);
  server.send(200, "image/jpeg", "");
  server.client().write(fb->buf, fb->len);
  
  esp_camera_fb_return(fb);
}

void recibirOrden() {
  if (server.hasArg("letra")) {
    String letra = server.arg("letra");
    
    // MANDAR LA ORDEN FÍSICA AL ARDUINO POR EL CABLE TX
    Serial.print(letra); 
    
    server.send(200, "text/plain", "Orden transmitida: " + letra);
  } else {
    server.send(400, "text/plain", "Error: Falta la letra");
  }
}

// --- 3. CONFIGURACIÓN INICIAL ---
void setup() {
  // Inicializamos el Serial a 9600 para que el Arduino lo entienda
  Serial.begin(9600);
  
  // Configurar como Módem (Access Point)
  WiFi.softAP("Estacionamiento_IA", "12345678"); 
  
  // Configurar la Cámara
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sccb_sda = SIOD_GPIO_NUM;
  config.pin_sccb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  
  // Calidad baja (VGA) para procesar rápido y no trabar la ESP32
  config.frame_size = FRAMESIZE_VGA; 
  config.jpeg_quality = 12;
  config.fb_count = 1;

  esp_camera_init(&config);

  // Configurar las rutas del Servidor
  server.on("/foto", enviarFoto); 
  server.on("/comando", recibirOrden); 
  
  server.begin();
}

// --- 4. CICLO PRINCIPAL ---
void loop() {
  server.handleClient();
}