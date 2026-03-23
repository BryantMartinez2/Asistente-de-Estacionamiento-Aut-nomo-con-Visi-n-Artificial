//Asistente de estacionamiento autonomo 
//Creado por Bryant Martinez
#include <SoftwareSerial.h>

// Pines de comunicación con ESP32-CAM

SoftwareSerial espSerial(11,12);

// Pines del Sensor Ultrasónico HC-SR04

// Pines del Puente H L298N
const int Trig = 3;
const int Echo = 4;
const int ENA = 5;
const int IN1 = 6;
const int IN2 = 7;
const int IN3 = 8;
const int IN4 = 9;
const int ENB = 10;

// Velocidad ajustada para evitar caídas de tensión (0-255)
const int velocidad_segura = 75;

void setup() {
  Serial.begin(9600);
  espSerial.begin(9600);
  Serial.println("Arduino Iniciado. Esperando ordenes...");
  pinMode(Trig, OUTPUT);
  pinMode(Echo, INPUT);
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENB, OUTPUT);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}

void loop() {
  int distanciaActual = medirDistancia();
  
  //Activacion de "Stop" por el sensor de ultrasonido.

  if (distanciaActual > 0 && distanciaActual < 10) {
    detener ();
    Serial.println("Obstaculo en frente.");
    delay(100);
    return;
  } 
  
  // 2. Escuchar a la IA (ESP32-CAM)
  if (espSerial.available() > 0){
    char orden = espSerial.read();
    Serial.print("Comunicacion recibida.");
    Serial.print(orden);
    if (orden == 'A'){
      Serial.println("Avanzar buscando lugar...");
      avanzar();
    }
    else if (orden == 'E'){
      Serial.println("Lugar encontrado, Iniciando aparcamiento.");
      rutinaEstacionar();
    }
    else if (orden == 'S'){
      detener();
    }
  }
  delay (50);
}

int medirDistancia(){
  digitalWrite(Trig, LOW);
  delayMicroseconds(2);
  digitalWrite(Trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(Trig, LOW);
  long duracion = pulseIn(Echo, HIGH);
  int distancia_cm = duracion * 0.034/2;
  return distancia_cm;
}

void avanzar(){
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, velocidad_segura);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENB, velocidad_segura);
}
void detener(){
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}
void rutinaEstacionar(){
  detener();
  Serial.println("Iniciando estacionamiento...");
  delay(500);

  // Giro de 90 grados

  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENA, velocidad_segura);
  analogWrite(ENB, velocidad_segura);
  delay(1000);
  avanzar();
  delay(1000);
  detener();
  Serial.println("Estacionado!");

  // Bloqueo de seguridad al terminar
  while (true){

  }
}