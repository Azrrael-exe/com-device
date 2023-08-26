#include <Arduino.h>
#include <LiquidCrystal.h>
#include <display/display.h>

String button_1 = "Green";
String button_2 = "White";

LiquidCrystal lcd = LiquidCrystal(8, 9, 4, 5, 6, 7); 

void setup() {
    Serial.begin(115200);
    lcd.begin(16, 2);
}
  
void loop() {
    showValue(lcd, 0, button_1, 10);
    showValue(lcd, 1, button_2, 10);
    while (true) {
        /* code */
    }
    
}