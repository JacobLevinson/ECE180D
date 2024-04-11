#include <FastLED.h>
#include <PubSubClient.h>
#include <WiFiNINA.h>

const char* ssid = "INSERT_WIFI_NETWORK_HERE";
const char* password = "ENTER_PASSWORD_HERE";
const char mqtt_server[] = "mqtt.eclipseprojects.io";
const char subscribeTopic[] = "ece180d/team3/reverseabomb/ledcontroller";

WiFiClient wifiClient;
PubSubClient mqtt(wifiClient);

// Number of LED arrays
#define NUM_LED_ARRAYS 6

// How many leds are in each strip?
#define NUM_LEDS_PER_ARRAY 90

// Specify the data pins for each LED array
const int DATA_PINS[NUM_LED_ARRAYS] = {3, 4, 5, 6, 7, 8};


#define TOKEN ""
#define DEVICEID ""

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

  Serial.print("LED State:");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  

  //now with the read data, update the LEDS for the gameboard
  for (int stripIndex = 0; stripIndex < NUM_LED_ARRAYS; stripIndex++) 
  {
    const char* stripKey = ("LED_Strip_" + String(stripIndex)).c_str();
    const JsonArray& pixels = doc[stripKey]["pixels"];

    for (int pixelIndex = 0; pixelIndex < pixels.size(); pixelIndex++) 
    {
      const char* color = pixels[pixelIndex];
      CRGB ledColor;

      if (strcmp(color, "black") == 0) 
      {
        ledColor = CRGB::Black;
      } 
      else if (strcmp(color, "red") == 0) 
      {
        ledColor = CRGB::Red;
      } 
      else 
      {
        // Handle other colors if needed
        ledColor = CRGB::Black;
      }

      leds[stripIndex][pixelIndex] = ledColor;
    }
  }

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
