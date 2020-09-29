#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include <avr/sleep.h>
#include "USI_TWI_Slave.h"

void receiveEvent(int howMany);
void requestEvent();

#define MASK  (1 << PORTB3)
// 7 bit slave I2C address
#define SLAVE_ADDR  0x8

volatile uint8_t i2c_regs[] =
{
    0xDE,
    0xAD,
    0xBE,
    0xEF,
};

// Tracks the current register pointer position
volatile uint8_t reg_position;
uint8_t reg_size = sizeof(i2c_regs);

int main() {
     USI_TWI_Slave_Initialise(SLAVE_ADDR);
     USI_TWI_On_Slave_Transmit = requestEvent;
     USI_TWI_On_Slave_Receive = receiveEvent;
     sei();
    
     //DDRB |= MASK;  // PORTB as OUTPUT
    DDRB = MASK;
    //PORTB = MASK;

    /*while(1) {
        PORTB ^= MASK;
        _delay_ms(500);
    }*/
    while(1) {
       sleep_enable(); // разрешаем сон

       if (USI_TWI_Slave_Is_Active()) {
            set_sleep_mode(SLEEP_MODE_IDLE); // если спать - то на полную
       }
       else {
            set_sleep_mode(SLEEP_MODE_PWR_DOWN); // если спать - то на полную
       }

       sleep_mode();
    }
    
}

void requestEvent()
{
    USI_TWI_Transmit_Byte(i2c_regs[reg_position]);
    PORTB ^= MASK;
    //PORTB = MASK;
    // Increment the reg position on each read, and loop back to zero
    reg_position++;
    if (reg_position >= reg_size)
    {
        reg_position = 0;
    }
}

void receiveEvent(int howMany)
{
    PORTB ^= MASK;
    if (howMany < 1)
    {
        // Sanity-check
        return;
    }
    if (howMany > TWI_RX_BUFFER_SIZE)
    {
        // Also insane number
        return;
    }

    reg_position = USI_TWI_Receive_Byte();
    howMany--;
    if (!howMany)
    {
        // This write was only to set the buffer for next read
        return;
    }
    while(howMany--)
    {
        i2c_regs[reg_position] = USI_TWI_Receive_Byte();
        reg_position++;
        if (reg_position >= reg_size)
        {
            reg_position = 0;
        }
    }
}

