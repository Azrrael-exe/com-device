#ifndef printer_h
#define printer_h

#include <Arduino.h>

void serialPrinter(Stream& uart, uint8_t line, String var, uint8_t value) {
    char buffer[16];
    sprintf(buffer, "%s: %d\n", var.c_str(), value);
    uart.print(buffer);
}
#endif