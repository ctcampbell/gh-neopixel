#include <Adafruit_GFX.h>
#include <Adafruit_NeoMatrix.h>
#include <Adafruit_NeoPixel.h>

int matrixW = 8;
int matrixH = 5;
#define PIN 6

Adafruit_NeoMatrix matrix = Adafruit_NeoMatrix(matrixW, matrixH, PIN,
                            NEO_MATRIX_TOP     + NEO_MATRIX_LEFT +
                            NEO_MATRIX_ROWS    + NEO_MATRIX_PROGRESSIVE,
                            NEO_GRB            + NEO_KHZ800);

const uint16_t colors[] = {
  matrix.Color(255, 0, 0),
  matrix.Color(0, 255, 0),
  matrix.Color(255, 255, 0),
  matrix.Color(0, 0, 255),
  matrix.Color(255, 0, 255),
  matrix.Color(0, 255, 255),
  matrix.Color(255, 255, 255)
};

void setup() {
  matrix.begin();
  matrix.setBrightness(100);
  Serial.begin(9600);
  Serial.print("<ready>\n");
}

void loop() {
  if (Serial.available() > 0) {
    long count = Serial.parseInt();
    count = min(39, count);
    matrix.clear();
    for (long i = 0; i < count; i++) {
      matrix.setPixelColor(i, colors[0]);
    }
  }
  matrix.setPixelColor((matrixH * matrixW) - 1, colors[1]);
  matrix.show();
}
