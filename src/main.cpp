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

LiquidCrystal screen = LiquidCrystal(8, 9, 4, 5, 6, 7); 

void setup() {
    Serial.begin(115200);
    screen.begin(16, 2);
}
  
void loop() {
    button_1.sample();
    button_2.sample();
    DataPack input = DataPack();
    if (input.available(Serial)) {
        if (input.hasKey(0x0A)) {
            showValue(screen, 0, "Energy", input.getData(0x0A));
        }
        if (input.hasKey(0x0B)) {
            showValue(screen, 1, "Coffe", input.getData(0x0B));
        }
    }
    if (button_1.hasChanged() || button_2.hasChanged()) {
        DataPack out = DataPack();
        out.addData(0xA1, button_1.read());
        out.addData(0xA2, button_2.read());
        out.write(Serial);
    }    
}