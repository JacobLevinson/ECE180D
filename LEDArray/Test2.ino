#include <WiFiNINA.h>
#include <PubSubClient.h>
#include <FastLED.h>
#include <ArduinoJson.h>

// Define WiFi credentials
const char* ssid = "ATTTMBDHWa";
const char* password = "fx7eyh+gdjnn";

// Define MQTT parameters
const char mqtt_server[] = "mqtt.eclipseprojects.io";
const char subscribeTopic[] = "ece180d/team3/reverseabomb/ledcontroller";

// Create a WiFi client and MQTT client
WiFiClient wifiClient;
PubSubClient mqtt(wifiClient);

// Define the number of LED strips and the number of LEDs per strip
#define NUM_STRIPS 6
#define NUM_LEDS_PER_STRIP 90

// Define the data pins for each LED strip
const int DATA_PINS[NUM_STRIPS] = {3, 4, 5, 6, 7, 8};

// Create a 2-dimensional array for the LEDs
CRGB leds[NUM_STRIPS][NUM_LEDS_PER_STRIP];

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
  for (unsigned int i = 0; i < length; i++) {
    Serial.write(payload[i]);
  }
  Serial.println();

  // Allocate a temporary JsonDocument
  StaticJsonDocument<2048> doc;

  // Deserialize the JSON payload
  DeserializationError error = deserializeJson(doc, payload, length);
  if (error) {
    Serial.print("deserializeJson() failed: ");
    Serial.println(error.f_str());
    return;
  }

  // Update the LEDs for each strip
  for (int stripIndex = 0; stripIndex < NUM_STRIPS; stripIndex++) {
    char stripKey[16];
    sprintf(stripKey, "LED_Strip_%d", stripIndex);

    if (doc.containsKey(stripKey)) {
      JsonArray pixels = doc[stripKey]["pixels"];

      for (int pixelIndex = 0; pixelIndex < pixels.size(); pixelIndex++) {
        const char* color = pixels[pixelIndex];
        CRGB ledColor;

        if (strcmp(color, "black") == 0) {
          ledColor = CRGB::Black;
        } else if (strcmp(color, "red") == 0) {
          ledColor = CRGB::Red;
        } else if (strcmp(color, "green") == 0) {
          ledColor = CRGB::Green;
        } else {
          // Handle other colors if needed
          ledColor = CRGB::Black;
        }

        leds[stripIndex][pixelIndex] = ledColor;
      }
    }
  }

  // Show the LEDs
  FastLED.show();

  // Print out the values of the LED arrays for debugging
  Serial.println("Current LED States:");
  for (int stripIndex = 0; stripIndex < NUM_STRIPS; stripIndex++) {
    Serial.print("LED_Strip_");
    Serial.print(stripIndex);
    Serial.print(": ");
    for (int pixelIndex = 0; pixelIndex < NUM_LEDS_PER_STRIP; pixelIndex++) {
      if (leds[stripIndex][pixelIndex] == CRGB::Red) {
        Serial.print("red ");
      } else if (leds[stripIndex][pixelIndex] == CRGB::Green) {
        Serial.print("green ");
      } else {
        Serial.print("black ");
      }
    }
    Serial.println();
  }
}

void setup() {
  Serial.begin(9600);
  setup_wifi();
  mqtt.setServer(mqtt_server, 1883);
  mqtt.setCallback(callback);
  mqtt.subscribe(subscribeTopic); // Subscribe to MQTT topic

  // Initialize each LED strip
  for (int i = 0; i < NUM_STRIPS; i++) {
    FastLED.addLeds<WS2812B, DATA_PINS[i], GRB>(leds[i], NUM_LEDS_PER_STRIP);
  }
}

void loop() {
  // Check if MQTT client is connected
  if (!mqtt.connected()) {
    // If not connected, attempt to reconnect
    reconnect();
  }
  
  // Check for MQTT messages and handle callbacks
  mqtt.loop();
}
