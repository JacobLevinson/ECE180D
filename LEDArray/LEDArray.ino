
#include <FastLED.h>
#include <ArduinoJson.h>
#include <PubSubClient.h>//for MQTT clients library 
#include <WiFiNINA.h>//for wifi library 

///////////////////////////////////////////////////////////////////////////////////////////
//create our variable to hold data 
static char payload[256]; //payload is our message we send, limit to 256 characters
//StaticJsonDocument<256> doc; //creating a JSON document which will hold data messages

#define TOKEN ""
#define DEVICEID ""

//specify your network password that your devices will be sharing 
const char* ssid = " INSERT_WIFI_NETWORK_HERE";
const char* password = "ENTER_PASSWORD_HERE";
const char mqtt_server[] = "mqtt.eclipseprojects.io"; //local server we will use
const char subscribeTopic[] = "ece180d/team3/reverseabomb/ledcontroller"; //the topic we publish to 

//create a client object 
WiFiClient wifiClient;
PubSubClient mqtt(wifiClient);

// How many leds are in the strip?
#define NUM_LEDS 90 // assuming that we have 5 foot strips (1.5m) where there are 60pixels/meter on strips 

// For led chips like WS2812, which have a data line, ground, and power, you just
// need to define DATA_PIN.  
#define DATA_PIN 3// when working with multiple led arrays, we will make this an array of pins

// This is an array of leds.  One item for each led in your strip. So when you have multiple LED
// strips you will need multiple arrays or multi-dimensional arrays
CRGB leds[NUM_LEDS];

//*************************************************************************************
//                          void setup_wifi() 
// Is a function which connects to the wifi network specified above. Function will 
// continuously attempt to connect if no connection is successful. Once connected
// the network details will be printed to the serial monitor.
//*************************************************************************************
void setup_wifi(){

  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  while( WiFi.status() != WL_CONNECTED){

    delay(500);
    Serial.print("."); 
  }

  randomSeed(micros());
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
 
}
//*************************************************************************************
//                          void reconnect()
// This is a function, that when called, will attempt to connect to the MQTT broker. 
// It will confirm if connection was successful otherwise it pint an error message 
// and attempt to reconnect. 
//*************************************************************************************
void reconnect(){

  while(!mqtt.connected()){
  
    //Serial.print("Attempting MQTT connection ....");
    //String clientID = "nano33_accelerometer-";
    //clientID += String(random(0xffff), HEX);
  
    if (mqtt.connect(DEVICEID, TOKEN, NULL)) {
    
      Serial.println("Connected to MQTT broker");
      digitalWrite(LED_BUILTIN, HIGH);
    }

    else
    {
      Serial.print("failed to connect to MQTT broker, rc=");
      Serial.print(mqtt.state());
      Serial.println("try again in 5 seconds");
      digitalWrite(LED_BUILTIN, LOW);
      delay(5000);

    }
     
  }
 
}

//*************************************************************************************
//                          void callback()
// This is a callback function that gets called anytime a message is received through
// the subscibed topic 
// 
//*************************************************************************************

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);

  Serial.print("Message:");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  // Convert the payload to an integer
  int newPosition = atoi((char*)payload);

  // Set position of the led in the array to what was given by the payload 
  leds[newPosition] = CRGB::Red;

  // Show the leds (only one of which is set to white, from above)
  FastLED.show();

  // Wait a little bit
  delay(100);
}
//*************************************************************************************

// This function sets up the ledsand tells the controller about them
void setup() {
    //connect to the wifi network and then connect to the mqtt server 
    setup_wifi();
    mqtt.setServer(mqtt_server, 1883);

	// sanity check delay - allows reprogramming if accidently blowing power w/leds
   	delay(2000);

    // Uncomment/edit one of the following lines for your leds arrangement.
    // ## Clockless types ##
    FastLED.addLeds<WS2812B, DATA_PIN, RGB>(leds, NUM_LEDS);  // GRB ordering is typical
}

// This function runs over and over, and is where you do the magic to light
// your leds.
void loop() {

    //check if connection was successful, otherwise try to reconnect
    if (!mqtt.connected())
    {
     reconnect();
    }

    //begin client loop with MQTT
    mqtt.loop();

}