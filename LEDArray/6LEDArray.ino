#include <FastLED.h>
#include <ArduinoJson.h>
#include <PubSubClient.h>
#include <WiFiNINA.h>
#include <Arduino_JSON.h>

// Number of LED arrays
#define NUM_LED_ARRAYS 6

// How many leds are in each strip?
#define NUM_LEDS_PER_ARRAY 90

// Specify the data pins for each LED array
const int DATA_PINS[NUM_LED_ARRAYS] = {3, 4, 5, 6, 7, 8};

StaticJsonDocument<256> doc;

#define TOKEN ""
#define DEVICEID ""

const char* ssid = "INSERT_WIFI_NETWORK_HERE";
const char* password = "ENTER_PASSWORD_HERE";
const char mqtt_server[] = "mqtt.eclipseprojects.io";
const char subscribeTopic[] = "ece180d/team3/reverseabomb/ledcontroller";

WiFiClient wifiClient;
PubSubClient mqtt(wifiClient);

CRGB leds[NUM_LED_ARRAYS][NUM_LEDS_PER_ARRAY]; //2D array to help control the 6 LED arrays 

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!mqtt.connected()) {
    if (mqtt.connect(DEVICEID, TOKEN, NULL)) {
      Serial.println("Connected to MQTT broker");
      digitalWrite(LED_BUILTIN, HIGH);
    } else {
      Serial.print("failed to connect to MQTT broker, rc=");
      Serial.print(mqtt.state());
      Serial.println("try again in 5 seconds");
      digitalWrite(LED_BUILTIN, LOW);
      delay(5000);
    }
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);

  Serial.print("Message:");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  deserializeJson(doc, payload);

  int arrayIndex = doc["arrayIndex"];
  int newPosition = doc["position"];

  for (int i = 0; i < NUM_LEDS_PER_ARRAY; i++) {
    leds[arrayIndex][i] = CRGB::Black;
  }

  leds[arrayIndex][newPosition] = CRGB::Red;
  FastLED.show();
}

void setup() {
  setup_wifi();
  mqtt.setServer(mqtt_server, 1883);
  delay(2000);

  for (int i = 0; i < NUM_LED_ARRAYS; i++) {
    FastLED.addLeds<WS2812B, DATA_PINS[i], RGB>(leds[i], NUM_LEDS_PER_ARRAY);
  }
}

void loop() {
  if (!mqtt.connected()) {
    reconnect();
  }

  mqtt.loop();
}