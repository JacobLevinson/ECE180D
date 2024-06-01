#include <WiFiNINA.h>
#include <PubSubClient.h>
#include <FastLED.h>

// Define WiFi credentials
const char* ssid = "William";
const char* password = "12345678";

// Define MQTT parameters
const char mqtt_server[] = "mqtt.eclipseprojects.io";
const char subscribeTopic[] = "ece180d/team3/reverseabomb/ledcontroller";

// Create a WiFi client and MQTT client
WiFiClient wifiClient;
PubSubClient mqtt(wifiClient);

// Define the number of LED strips and the number of LEDs per strip
#define NUM_STRIPS 6
#define NUM_LEDS_PER_STRIP 11

// Define the data pins for each LED strip
const int DATA_PINS[NUM_STRIPS] = {3, 4, 5, 6, 7, 8};

// Create a 2-dimensional array for the LEDs. We have The num_strips as the row, and pixels as the columns
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

// Function to reconnect to MQTT broker if disconnected
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

  // // DEBUGGING: Print the received message
  // Serial.println("LED State:");
  // for (unsigned int i = 0; i < length; i++) {
  //   Serial.write(payload[i]); //write each byte(character) to the screen
  // }
  // Serial.println();

  // Ensure the payload length matches the number of LEDs
  if (length == NUM_STRIPS * NUM_LEDS_PER_STRIP) 
  {
    //if the payload length is correct, then we can update the led arrays
    for (int strip = 0; strip < NUM_STRIPS; strip++) 
    {
      for (int led = 0; led < NUM_LEDS_PER_STRIP; led++) 
      {
        int index = strip * NUM_LEDS_PER_STRIP + led;
        if (payload[index] == 'r') 
        {
          leds[strip][led] = CRGB::Red;
        } 
        else 
        {
          leds[strip][led] = CRGB::Black;
        }
      }
    }
    // Show the LEDs
    FastLED.show();
  } else {
    Serial.println("Payload length mismatch.");
  }
}

void setup() {
  Serial.begin(9600);
  setup_wifi();
  mqtt.setServer(mqtt_server, 1883);
  mqtt.setCallback(callback);
  mqtt.subscribe(subscribeTopic); // Subscribe to MQTT topic

  // tell FastLED there's 6 WS2812B Led strips with 90 pixels each
  FastLED.addLeds<WS2812B, 3, GRB>(leds[0], NUM_LEDS_PER_STRIP);
  FastLED.addLeds<WS2812B, 4, GRB>(leds[1], NUM_LEDS_PER_STRIP);
  FastLED.addLeds<WS2812B, 5, GRB>(leds[2], NUM_LEDS_PER_STRIP);
  FastLED.addLeds<WS2812B, 6, GRB>(leds[3], NUM_LEDS_PER_STRIP);
  FastLED.addLeds<WS2812B, 7, GRB>(leds[4], NUM_LEDS_PER_STRIP);
  FastLED.addLeds<WS2812B, 8, GRB>(leds[5], NUM_LEDS_PER_STRIP);
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