#ifndef dislpay_h
#define dislpay_h

#include <LiquidCrystal.h>

void showValue(LiquidCrystal& lcd, uint8_t line, String var, uint16_t value) {
    char buffer[16];
    sprintf(buffer, "%s: %u", var.c_str(), value);
    lcd.setCursor(0, line);
    lcd.print(buffer);
}

#endif