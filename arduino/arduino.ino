#include <FastLED.h>

#define NUM_LEDS 40
#define DATA_PIN 6

// See https://raw.githubusercontent.com/FastLED/FastLED/gh-pages/images/HSV-rainbow-with-desc.jpg
CHSV notificationPixel(32, 128, 50);
CHSV powerPixel(96, 128, 50);
CRGB leds[NUM_LEDS];

void setup()
{
    FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);
    Serial.begin(9600);
    Serial.println("<ready>");
}

void loop()
{
    if (Serial.available() > 0)
    {
        long count = Serial.parseInt();
        // Last pixel is reserved for power status so max
        // count is 1 less than total pixel count
        count = max(0, min(NUM_LEDS - 1, count));
        FastLED.clear();
        for (int i = 0; i < count; i++)
        {
            leds[i] = notificationPixel;
        }
    }
    leds[NUM_LEDS - 1] = powerPixel;
    FastLED.show();
}
