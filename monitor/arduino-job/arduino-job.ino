
#include <ArduinoBLE.h>
#include <BH1750FVI.h>
#include <SPI.h>
#include <WiFiNINA.h>

#define BUZZER_PIN 2
#define TIMEOUT 15

#include "secrets.h"
char ssid[] = SECRET_SSID;        // your network SSID
char pass[] = SECRET_PASS;    // your network password
int status = WL_IDLE_STATUS;     // the WiFi radio's status

WiFiClient client;
char HOST_NAME[] = "maker.ifttt.com";
String PATH_NAME = "/trigger/raspberry-pi-condition/with/key/" + String(API_KEY);

BH1750FVI LightSensor(BH1750FVI::k_DevModeContLowRes);

long start;

enum condition {
  OK = '3',
  NO_INTERNET = '2',
  BAD = '1',
  BYE = '9'
};


void setup() {
  Serial.begin(115200);
  while (!Serial);

  // attempt to connect to WiFi network:
  while (status != WL_CONNECTED) {
    status = WiFi.begin(ssid, pass);

    // wait 10 seconds for connection:
    delay(10000);
  }

  Serial.println("ready");
  // Set up Light sensor
  LightSensor.begin();

  // Setup buzzer
  pinMode(BUZZER_PIN, OUTPUT);
  start = millis();
}

void loop() {
  condition message;
  
  uint16_t lux = LightSensor.GetLightIntensity();
  if (lux < 10){
    // notify the user
    httpRequest("?value1=NO_ENOUGH_LIGHT");
    activateBuzzer(1);
    start = millis();
  }
  
  while(Serial.available() > 0){
    int content = Serial.read();
    if(content != 10){
      message = (condition)content;
      Serial.println(message);
    }
    start = millis();
  }

  if(message == BYE){
    Serial.println("BYEEE");
    while(1){}
  }

  int waitingPeriod = (millis() - start) / 1000;
  if(waitingPeriod >= TIMEOUT){
    // notify the user that RPi has no power
    httpRequest("?value1=NO_POWER");
    activateBuzzer(3);
    start = millis();
  }
  else if(message == NO_INTERNET){
    // notify the user that RPi has no internet
    Serial.println("No internet");
    httpRequest("?value1=NO_INTERNET");
    activateBuzzer(2);
    start = millis();
  }
  else if (message == BAD){
    // notify the user
    Serial.println("BAD");
    httpRequest("?value1=BAD");
    activateBuzzer(3);
    start = millis();
  }
}


void activateBuzzer(int iterations){
  for(int i =0; i< iterations; i++){
    tone(BUZZER_PIN, 1000); // Send 1KHz sound signal...
    delay(1000);        // ...for 1 sec
    noTone(BUZZER_PIN);     // Stop sound...
    delay(1000);        // ...for 1sec
  }
}

int httpRequest(String queryString){
  // Try to connect to IFTTT HTTP service
  client.stop();
  // make a HTTP request:
  // send HTTP header
  if(client.connect(HOST_NAME, 80)){
    // Serial.println("Connected to server");
    client.println("GET " + PATH_NAME + queryString + " HTTP/1.1");
    client.println("Host: " + String(HOST_NAME));
    client.println("Connection: close");
    client.println(); // end HTTP header
  }else{
    // Serial.println("connection failed");
  }
}