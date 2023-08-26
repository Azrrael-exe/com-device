#include <Arduino.h>
#include <LiquidCrystal.h>
#include <display/display.h>
#include <inputs/button.h>
#include <communication/printer.h>

#include "llp.h"

String variable_1 = "Juan";
String variable_2 = "White";

Button button_1 = Button(A4);
Button button_2 = Button(A5);

LiquidCrystal lcd = LiquidCrystal(8, 9, 4, 5, 6, 7); 

void setup() {
    Serial.begin(115200);
    lcd.begin(16, 2);
}
  
void loop() {
    button_1.sample();
    button_2.sample();
    DataPack input = DataPack();
    if (input.available(Serial)) {
        showValue(lcd, 0, "tests", input.getData(0x01));
    }
    if (button_1.hasChanged() || button_2.hasChanged()) {
        showValue(lcd, 0, variable_1, button_1.read());
        showValue(lcd, 1, variable_2, button_2.read());
        //serialPrinter(Serial, 0, variable_1, button_1.read());
        //serialPrinter(Serial, 1, variable_2, button_2.read());
        DataPack out = DataPack();
        out.addData(0xA1, button_1.read());
        out.addData(0xA2, button_2.read());
        out.write(Serial);
    }    
}