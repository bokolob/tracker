#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include <avr/sleep.h>
#include <stddef.h>

#include "USI_TWI_Slave.h"
#include "light_ws2812.h"
//#include "greenfade.h"
//#include "palette.h"
#include "TimerOne.h"

void receiveEvent(int howMany);
void requestEvent();
void blink(void);

#define POWER_PIN PORTA6
#define NEOPIXEL_PIN PORTA5

#define MASK  (1 << NEOPIXEL_PIN) | (1 << POWER_PIN) 
// 7 bit slave I2C address
#define SLAVE_ADDR  0x8

#define LIGHT_REG 0
#define POWER_REG 1
#define POWER_TIME_MULTIPLIER 2
#define PING_REG  3

#define A9G_DISABLED 0x1
#define PLAYING_EFFECT 0x2
#define PCINT1_INT 0x4

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
volatile int timeout = 0;
volatile uint8_t state = 0;

int effect_position = 0;
const int (*effect)[4] = NULL;
struct cRGBW led[1];
void play(void);

void usi_init() {
    USI_TWI_Slave_Initialise(SLAVE_ADDR);
    USI_TWI_On_Slave_Transmit = requestEvent;
    USI_TWI_On_Slave_Receive = receiveEvent;
}

void enable_a9g() {
   PORTA &= ~(1 << POWER_PIN);
   usi_init();
   state &= ~A9G_DISABLED;
}

void disable_a9g() {
   USI_TWI_Slave_Disable();
   PORTA |= (1 << POWER_PIN);
   state |= A9G_DISABLED;
}

void start_watchdog() {
    //Watchdog change enabled
    WDTCR |= (1 << WDCE);
    //Watchdog enabled, Watchdog interrupt enabled
    WDTCR |= (1 << WDE) | (1 << WDIE);
    WDTCR |= (1 << WDP3) | (0 << WDP2) | (0 << WDP1) | (1 << WDP0); //8 seconds delay
    //Watchdog change disabled
    WDTCR &= ~(1 << WDCE);
}

void watchdog_disable() {
    //Flags cleared
    MCUSR = 0x00;
    //Watchdog change enabled and Watchdog enabled at the same time to disable
    WDTCR |= (1 << WDCE)  | (1 << WDE);
    //Watchdog disabled
    WDTCR &= ~((1 << WDCE) | (1 << WDE) | (1 << WDIE));
}

void initAccelInterrupt() {
    MCUCR |= 1 << ISC00;      // configure INT0 to ..
    MCUCR &= ~(1 << ISC01);   // .. interrupt at any logical change at INT0
}

void enableAccelInt() {
    GIMSK |= 1 << INT1;       // enable INT0 interrupt
}

void disableAccelInt() {
    GIMSK &= ~(1 << INT1);       // enable INT0 interrupt
}

int main() {
    start_watchdog();
    enable_a9g();
    initAccelInterrupt();
    sei();

    DDRA = MASK;

    while(1) {
       sleep_enable();

       if (state & A9G_DISABLED && (timeout <= 0 || state & PCINT1_INT)) {
           timeout = 0;
           disableAccelInt();
           state &= ~PCINT1_INT;
           enable_a9g();
       }

       while (USI_TWI_Slave_Is_Active()) {
            _delay_ms(10);
       }

       if (i2c_regs[LIGHT_REG] != 0) {
            i2c_regs[LIGHT_REG] = 0;

            timer_stop();
            state |= PLAYING_EFFECT;
//            effect = RAINBOW;
            effect_position = 0;
            attachTimerInterrupt(play, 20000);
            //blink();
       }

       if (i2c_regs[POWER_REG] != 0) {
           watchdog_disable();
           timeout = i2c_regs[POWER_REG] * i2c_regs[POWER_TIME_MULTIPLIER];

           if (timeout & 0x7) {
                timeout &= ~(0x7);
                timeout += 8;
           }

           start_watchdog();
           i2c_regs[POWER_REG] = 0;
           enableAccelInt();
           disable_a9g();
       }

       set_sleep_mode(state & PLAYING_EFFECT ? SLEEP_MODE_IDLE : SLEEP_MODE_PWR_DOWN);
       sleep_mode();
    }

    return 0;
}

ISR(INT1_vect) {
    state |= PCINT1_INT;
}

ISR(WDT_vect) {
    WDTCR |= (1 << WDIE); //Watchdog interrupt enabled

    if (timeout >=8) {
        timeout -= 8;
    }
    else {
        timeout = 0;
    }
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

void play(void) {
    
    if (effect_position < 500) {
    /*    led[0].r = pgm_read_byte(&effect[effect_position][0]);
        led[0].g = pgm_read_byte(&effect[effect_position][1]);
        led[0].b = pgm_read_byte(&effect[effect_position][2]);
        led[0].w = pgm_read_byte(&effect[effect_position][3]);
    */  

        led[0].r = 128;
        led[0].g = 0;
        led[0].b = 0;
        led[0].w = 64;

        effect_position++;
    }
    else {
        led[0].r=0;led[0].g=0;led[0].b=0;led[0].w=0;
        state &= ~PLAYING_EFFECT;
        timer_stop();
    }
    
    ws2812_setleds_rgbw_mask(led, 1, (1 << NEOPIXEL_PIN));
}



