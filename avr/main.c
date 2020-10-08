#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include <avr/sleep.h>

#include "USI_TWI_Slave.h"
#include "light_ws2812.h"
#include "greenfade.h"

void receiveEvent(int howMany);
void requestEvent();
void blink(void);

#define POWER_PIN PORTB4
#define NEOPIXEL_PIN PORTB3

#define MASK  (1 << PORTB3) | (1 << POWER_PIN) 
// 7 bit slave I2C address
#define SLAVE_ADDR  0x8

#define LIGHT_REG 0
#define POWER_REG 1
#define POWER_TIME_MULTIPLIER 2
#define PING_REG  3

volatile uint8_t i2c_regs[] =
{
    0x0,  //Light
    0x0,  //A9G Power-off time
    0x1,  //A9G poer-off time multiplier
    0x0,  //Ping
    0xEF,
};

// Tracks the current register pointer position
volatile uint8_t reg_position;
uint8_t reg_size = sizeof(i2c_regs);
int timeout = 0;

int main() {
    USI_TWI_Slave_Initialise(SLAVE_ADDR);
    USI_TWI_On_Slave_Transmit = requestEvent;
    USI_TWI_On_Slave_Receive = receiveEvent;
    sei();

    DDRB = MASK;

    while(1) {
       sleep_enable(); // разрешаем сон
      
       if (timeout <= 0) {
           timeout = 0;
           enable_a9g();
       }

       while (USI_TWI_Slave_Is_Active()) {
            _delay_ms(10);
       }

       if (i2c_regs[LIGHT_REG] != 0) {
            i2c_regs[LIGHT_REG] = 0;
            blink();
       }

       if (i2c_regs[POWER_REG]) {
           timeout = i2c_regs[POWER_REG] * i2c_regs[POWER_TIME_MULTIPLIER];
           i2c_regs[POWER_REG] = 0;
           disable_a9g();
       }

       set_sleep_mode(SLEEP_MODE_PWR_DOWN);
       sleep_mode();
    }

    return 0;
}

void enable_a9g() {
   PORTB &= ~(1 << POWER_PIN);
}

void disable_a9g() {
   PORTB |= (1 << POWER_PIN);
}

void requestEvent() //write to master
{
    USI_TWI_Transmit_Byte(i2c_regs[reg_position]);
    // Increment the reg position on each read, and loop back to zero
    reg_position++;
    if (reg_position >= reg_size)
    {
        reg_position = 0;
    }
}

void receiveEvent(int howMany)
{
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

    reg_position = USI_TWI_Receive_Byte() % reg_size;

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


void blink(void)
{
    struct cRGBW led[2];
    led[1].r=0;led[1].g=128;led[1].b=0;led[1].w=0;    // Write red to array

    for (int i = 0; i < 100; i++) {
        led[0].r= pgm_read_byte(&GREEN[i][0]);
        led[0].g= pgm_read_byte(&GREEN[i][1]);
        led[0].b= pgm_read_byte(&GREEN[i][2]);
        led[0].w=0;

        ws2812_setleds_rgbw_mask(led, 1, (1 << NEOPIXEL_PIN));
        _delay_ms(50);
    }

    led[0].r=0;led[0].g=0;led[0].b=0;led[0].w=0;    // Write red to array
    ws2812_setleds_rgbw_mask(led,2, (1 << NEOPIXEL_PIN));
}


