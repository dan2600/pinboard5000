/**
For Pinboard 5000, gets string from serial and shows it.
*/
#include "HT16K33.h"
#include <avr/pgmspace.h>
HT16K33 matrix = HT16K33();
HT16K33 matrix1 = HT16K33();
#include "font.h"

String inputString = "PINBOARD BOOT   ";
boolean stringComplete = false;
int stringPos = 1;
int stringLen = 27;
bool scroll = true;


void showString() {
  for (int x = 0; x < 8; x++) {
    for (int i = 0; i < 16; i++) {
      matrix.setPixel(i, x, bitRead(pgm_read_word_near(fontTable + (inputString[x] - ' ')), i));
      matrix1.setPixel(i, x, bitRead(pgm_read_word_near(fontTable + (inputString[x + 8] - ' ')), i));

    }
  }
       matrix.write();
      matrix1.write();
}

void scrollString() {
  for (int x = 0; x < 8; x++) {
    for (int i = 0; i < 16; i++) {
      matrix.setPixel(i, x, bitRead(pgm_read_word_near(fontTable + (inputString[x + stringPos] - ' ')), i));
      matrix1.setPixel(i, x, bitRead(pgm_read_word_near(fontTable + (inputString[x + 7 + stringPos] - ' ')), i));
    }
  }

  stringPos++;
  if(stringPos > stringLen)
  {
stringPos = 0;
  }
          matrix.write();
      matrix1.write();
        delay(175);
}


void setup()
{
  Serial.begin(9600);
  inputString.reserve(200);
  matrix.init(0x70);
  matrix1.init(0x71);
 Serial.println("ready");
showString();
inputString = "";
}



void loop()
{
  while (Serial.available() > 0) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
//
}

  if (stringComplete) {
    inputString[inputString.length() - 1] = ' ';
    while (inputString.length() < 17)
    {
      inputString += ' ';
    }
    showString();
    inputString = "";
    stringComplete = false;
  }
  
}


