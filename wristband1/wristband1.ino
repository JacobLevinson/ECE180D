// https://community.element14.com/challenges-projects/design-challenges/design-for-a-cause-2021/b/blog/posts/connecting-the-arduino-nano-33-iot-with-local-mqtt-broker-2

#include <Arduino.h>

#include <SPI.h>

#include <Wire.h>

#include <Arduino_LSM6DS3.h>

#include <ArduinoJson.h>

#include <PubSubClient.h>

#include <WiFiNINA.h>

#define CONVERT_G_TO_MS2 9.80665f

#define FREQUENCY_HZ 104

#define INTERVAL_MS (1000 / (FREQUENCY_HZ + 1))

struct Acc_senseData
{

  float acc_x = 0.0F;

  float acc_y = 0.0F;

  float acc_z = 0.0F;
};

struct Gyr_senseData

{

  float gyr_x = 0.0F;

  float gyr_y = 0.0F;

  float gyr_z = 0.0F;
};

void setup_wifi();

void reconnect();

static Acc_senseData acc_data;

static Gyr_senseData gyr_data;

#define TOKEN "j"

#define DEVICEID "j"

const char *ssid = "Jacob IPhone";

const char *password = "wifi1234";

const char mqtt_server[] = "mqtt.eclipseprojects.io";

const char publishTopic[] = "ece180d/team3/reverseabomb/wristband1";

WiFiClient wifiClient;

PubSubClient mqtt(wifiClient);

void setup_wifi()
{

  delay(10);

  Serial.println();

  Serial.print("Connecting to ");

  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED)
  {

    delay(500);

    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");

  Serial.println("WiFi connected");

  Serial.println("IP address: ");

  Serial.println(WiFi.localIP());
}

void reconnect()
{

  while (!mqtt.connected())
  {

    Serial.println("Attempting to connect to MQTT");
    if (mqtt.connect(DEVICEID, TOKEN, NULL))
    {

      Serial.println("Connected to MQTT broker");

      digitalWrite(LED_BUILTIN, HIGH);
    }

    else

    {

      Serial.print("failed to connect to MQTT broker, rc=");

      Serial.print(mqtt.state());

      Serial.println("try again in 5 second");

      digitalWrite(LED_BUILTIN, LOW);

      delay(5000);
    }
  }
}

void setup()
{

  pinMode(LED_BUILTIN, OUTPUT);

  Serial.begin(9600);

  while (!Serial)
    ;

  if (!IMU.begin())

  {

    Serial.println("Failed to initialize IMU!");

    while (1)
      ;
  }

  setup_wifi();

  mqtt.setServer(mqtt_server, 1883);
}

void loop()
{

  if (!mqtt.connected())

  {

    reconnect();
  }

  mqtt.loop();

  static unsigned long last_interval_ms = 0;

  float a_x, a_y, a_z;

  float g_x, g_y, g_z;

  if (millis() > last_interval_ms + INTERVAL_MS)

  {

    last_interval_ms = millis();

    IMU.readAcceleration(a_x, a_y, a_z);

    acc_data.acc_x = a_x * CONVERT_G_TO_MS2;

    acc_data.acc_y = a_y * CONVERT_G_TO_MS2;

    acc_data.acc_z = a_z * CONVERT_G_TO_MS2;

    IMU.readGyroscope(g_x, g_y, g_z);

    gyr_data.gyr_x = g_x;

    gyr_data.gyr_y = g_y;

    gyr_data.gyr_z = g_z;

    if (sqrt(acc_data.acc_x * acc_data.acc_x + acc_data.acc_y * acc_data.acc_y + acc_data.acc_z * acc_data.acc_z) > 30.0 && acc_data.acc_z > 25)
    {
      digitalWrite(LED_BUILTIN, HIGH);
      mqtt.publish(publishTopic, "SLAP");
      Serial.println(sqrt(acc_data.acc_x * acc_data.acc_x + acc_data.acc_y * acc_data.acc_y + acc_data.acc_z * acc_data.acc_z));
      Serial.println(acc_data.acc_z);
      Serial.println();
      delay(100);
    }
    else
    {
      digitalWrite(LED_BUILTIN, LOW);
    }

    // Serial.print("acc_x: ");
    // Serial.print(acc_data.acc_x);
    // Serial.print(" acc_y: ");
    // Serial.print(acc_data.acc_y);
    // Serial.print(" acc_z: ");
    // Serial.print(acc_data.acc_z);
    // Serial.print(" gyr_x: ");
    // Serial.print(gyr_data.gyr_x);
    // Serial.print(" gyr_y: ");
    // Serial.print(gyr_data.gyr_y);
    // Serial.print(" gyr_z: ");
    // Serial.println(gyr_data.gyr_z);

    delay(10);
  }
}