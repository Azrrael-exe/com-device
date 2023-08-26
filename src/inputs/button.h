#ifndef buttons_h
#define buttons_h

#include <arduino.h>

class Button {
    public:
        Button(uint8_t pin);
        void sample();
        bool hasChanged();
        bool read();
    private:
        uint8_t pin;
        bool state;
        bool changed;
};

Button::Button(uint8_t pin) {
    this->pin = pin;
}

void Button::sample() {
    bool temp_state = digitalRead(this->pin);
    if (temp_state!= this->state) {
        this->changed = true;
        this->state = temp_state;
    }
}

bool Button::hasChanged() {
    return this->changed;
}

bool Button::read() {
    this->changed = false;
    return this->state;
}

#endif