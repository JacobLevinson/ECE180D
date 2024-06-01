#include <FastLED.h>

// Define the number of LED strips and the number of LEDs per strip
#define NUM_STRIPS 6
#define NUM_LEDS_PER_STRIP 11

// Define the data pins for each LED strip
const int DATA_PINS[NUM_STRIPS] = {3, 4, 5, 6, 7, 8};

// Create a 2-dimensional array for the LEDs. We have The num_strips as the row, and pixels as the columns
CRGB leds[NUM_STRIPS][NUM_LEDS_PER_STRIP];

// Function to process incoming serial data
void processSerialData(char *payload, unsigned int length)
{
    Serial.print("Message arrived with length: ");
    Serial.println(length);

    // Ensure the payload length matches the number of LEDs
    if (length == NUM_STRIPS * NUM_LEDS_PER_STRIP)
    {
        // if the payload length is correct, then we can update the led arrays
        for (int strip = 0; strip < NUM_STRIPS; strip++)
        {
            for (int led = 0; led < NUM_LEDS_PER_STRIP; led++)
            {
                int index = strip * NUM_LEDS_PER_STRIP + led;
                if (payload[index] == 'r')
                {
                    leds[strip][led] = CRGB::Red;
                }
                else if (payload[index] == 'g')
                {
                    leds[strip][led] = CRGB::Green;
                }
                else if (payload[index] == 'b')
                {
                    leds[strip][led] = CRGB::Blue;
                }
                else if (payload[index] == 'o')
                {
                    leds[strip][led] = CRGB::Black;
                }
            }
        }
        // Show the LEDs
        FastLED.show();
    }
    else
    {
        Serial.println("Payload length mismatch.");
    }
}

void setup()
{
    Serial.begin(9600);

    // Initialize LED strips
    FastLED.addLeds<WS2812B, 3, GRB>(leds[0], NUM_LEDS_PER_STRIP);
    FastLED.addLeds<WS2812B, 4, GRB>(leds[1], NUM_LEDS_PER_STRIP);
    FastLED.addLeds<WS2812B, 5, GRB>(leds[2], NUM_LEDS_PER_STRIP);
    FastLED.addLeds<WS2812B, 6, GRB>(leds[3], NUM_LEDS_PER_STRIP);
    FastLED.addLeds<WS2812B, 7, GRB>(leds[4], NUM_LEDS_PER_STRIP);
    FastLED.addLeds<WS2812B, 8, GRB>(leds[5], NUM_LEDS_PER_STRIP);
}

void loop()
{
    if (Serial.available() > 0)
    {
        // Read the incoming serial data
        char payload[NUM_STRIPS * NUM_LEDS_PER_STRIP];
        unsigned int length = Serial.readBytes(payload, NUM_STRIPS * NUM_LEDS_PER_STRIP);
        processSerialData(payload, length);
    }
}
