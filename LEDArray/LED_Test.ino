#include <WiFiNINA.h>
#include <PubSubClient.h>
#include <FastLED.h>

// Define WiFi credentials
const char* ssid = "ATTTMBDHWa";
const char* password = "fx7eyh+gdjnn";

// Define MQTT parameters
const char mqtt_server[] = "mqtt.eclipseprojects.io";
const char subscribeTopic[] = "ece180d/team3/reverseabomb/ledcontroller";

// Create a WiFi client and MQTT client
WiFiClient wifiClient;
PubSubClient mqtt(wifiClient);

// How many leds are in the strip?
#define NUM_LEDS 11 // assuming that we have 5 foot strips (1.5m) where there are 60pixels/meter on strips 

// For led chips like WS2812, which have a data line, ground, and power, you just
// need to define DATA_PIN.  
#define DATA_PIN 3// when working with multiple led arrays, we will make this an array of pins

// This is an array of leds.  One item for each led in your strip. So when you have multiple LED
// strips you will need multiple arrays or multi-dimensional arrays
CRGB leds[NUM_LEDS];

// Function to connect to WiFi
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

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

// Function to reconnect to MQTT broker
void reconnect() {
  while (!mqtt.connected()) {
    Serial.println("Attempting MQTT connection...");
    if (mqtt.connect("arduinoClient")) {
      Serial.println("Connected to MQTT broker");
      mqtt.subscribe(subscribeTopic);
    } else {
      Serial.print("Failed, rc=");
      Serial.print(mqtt.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

// Callback function to handle incoming MQTT messages
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);

  // Print the received message
  Serial.println("LED State:");
  for (int i = 0; i < length; i++) {
    Serial.write(payload[i]);
  }
  Serial.println();

  for (int i =0; i< NUM_LEDS; i++)//turn off leds before updating 
  {
   if(payload[i] == 'r')
   {
    leds[i] = CRGB::Red;
   }
   else
   {
    leds[i] = CRGB::Black;
   }
  }
  // Show the leds (only one of which is set to white, from above)
  FastLED.show();
}

void setup() {
  Serial.begin(9600);
  setup_wifi();
  mqtt.setServer(mqtt_server, 1883);
  mqtt.setCallback(callback);
  mqtt.subscribe(subscribeTopic); // Subscribe to MQTT topic
  FastLED.addLeds<WS2812B, DATA_PIN, GRB>(leds, NUM_LEDS);  // GRB ordering is typical
}

void loop() {
  if (!mqtt.connected()) {
    reconnect();
  }
  mqtt.loop();
}
