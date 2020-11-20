/*
 *  Interrupt and PWM utilities for 16 bit Timer1 on ATmega168/328
 *  Original code by Jesse Tane for http://labs.ideo.com August 2008
 *  Modified March 2009 by Jérôme Despatis and Jesse Tane for ATmega328 support
 *  Modified June 2009 by Michael Polli and Jesse Tane to fix a bug in setPeriod() which caused the timer to stop
 *  Modified April 2012 by Paul Stoffregen - portable to other AVR chips, use inline functions
 *  Modified again, June 2014 by Paul Stoffregen - support Teensy 3.x & even more AVR chips
 *  Modified July 2017 by Stoyko Dimitrov - added support for ATTiny85 except for the PWM functionality
 *  
 *
 *  This is free software. You can redistribute it and/or modify it under
 *  the terms of Creative Commons Attribution 3.0 United States License. 
 *  To view a copy of this license, visit http://creativecommons.org/licenses/by/3.0/us/ 
 *  or send a letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California, 94105, USA.
 *
 */

#include "TimerOne.h"

#define TIMER1_RESOLUTION 256UL  // Timer1 is 8 bit

// Placing nearly all the code in this .h file allows the functions to be
// inlined by the compiler.  In the very common case with constant values
// the compiler will perform all calculations and simply write constants
// to the hardware registers (for example, setPeriod).

static void (*isrCallback)();

unsigned short pwmPeriod;
unsigned char clockSelectBits;
const uint8_t ratio = (F_CPU)/ ( 1000000 );

//****************************
//  Configuration
//****************************
 void timer_initialize(unsigned long microseconds) {
    TCCR1A = _BV(CTC0);              //clear timer1 when it matches the value in OCR1C
    TIMSK |= _BV(OCIE1A);           //enable interrupt when OCR1A matches the timer value
    timerSetPeriod(microseconds);
}

void timerSetPeriod(unsigned long microseconds)  {
    const unsigned long cycles = microseconds * ratio;
    if (cycles < TIMER1_RESOLUTION) {
        clockSelectBits = _BV(CS10);
        pwmPeriod = cycles;
    } else
    if (cycles < TIMER1_RESOLUTION * 2UL) {
        clockSelectBits = _BV(CS11);
        pwmPeriod = cycles / 2;
    } else
    if (cycles < TIMER1_RESOLUTION * 4UL) {
        clockSelectBits = _BV(CS11) | _BV(CS10);
        pwmPeriod = cycles / 4;
    } else
    if (cycles < TIMER1_RESOLUTION * 8UL) {
        clockSelectBits = _BV(CS12);
        pwmPeriod = cycles / 8;
    } else
    if (cycles < TIMER1_RESOLUTION * 16UL) {
        clockSelectBits = _BV(CS12) | _BV(CS10);
        pwmPeriod = cycles / 16;
    } else
    if (cycles < TIMER1_RESOLUTION * 32UL) {
        clockSelectBits = _BV(CS12) | _BV(CS11);
        pwmPeriod = cycles / 32;
    } else
    if (cycles < TIMER1_RESOLUTION * 64UL) {
        clockSelectBits = _BV(CS12) | _BV(CS11) | _BV(CS10);
        pwmPeriod = cycles / 64UL;
    } else
    if (cycles < TIMER1_RESOLUTION * 128UL) {
        clockSelectBits = _BV(CS13);
        pwmPeriod = cycles / 128;
    } else
    if (cycles < TIMER1_RESOLUTION * 256UL) {
        clockSelectBits = _BV(CS13) | _BV(CS10);
        pwmPeriod = cycles / 256;
    } else
    if (cycles < TIMER1_RESOLUTION * 512UL) {
        clockSelectBits = _BV(CS13) | _BV(CS11);
        pwmPeriod = cycles / 512;
    } else
    if (cycles < TIMER1_RESOLUTION * 1024UL) {
        clockSelectBits = _BV(CS13) | _BV(CS11) | _BV(CS10);
        pwmPeriod = cycles / 1024;
    } else
    if (cycles < TIMER1_RESOLUTION * 2048UL) {
        clockSelectBits = _BV(CS13) | _BV(CS12);
        pwmPeriod = cycles / 2048;
    } else
    if (cycles < TIMER1_RESOLUTION * 4096UL) {
        clockSelectBits = _BV(CS13) | _BV(CS12) | _BV(CS10);
        pwmPeriod = cycles / 4096;
    } else
    if (cycles < TIMER1_RESOLUTION * 8192UL) {
        clockSelectBits = _BV(CS13) | _BV(CS12) | _BV(CS11);
        pwmPeriod = cycles / 8192;
    } else
    if (cycles < TIMER1_RESOLUTION * 16384UL) {
        clockSelectBits = _BV(CS13) | _BV(CS12) | _BV(CS11)  | _BV(CS10);
        pwmPeriod = cycles / 16384;
    } else {
        clockSelectBits = _BV(CS13) | _BV(CS12) | _BV(CS11)  | _BV(CS10);
        pwmPeriod = TIMER1_RESOLUTION - 1;
    }
    OCR1A = pwmPeriod;
    OCR1C = pwmPeriod;
    TCCR1A = _BV(CTC0) | clockSelectBits;
}

//****************************
//  Run Control
//****************************  
inline void timer_start()  {
    TCCR1A = 0;
    TCNT1 = 0;      
    timer_resume();
}

inline void timer_stop() {
    TCCR1A = _BV(CTC0);
}
inline void timer_restart() {
    timer_start();
}
inline void timer_resume() {
    TCCR1A = _BV(CTC0) | clockSelectBits;
}

//****************************
//  Interrupt Function
//****************************
void setTimerInterrupt(void (*isr)())  {
    isrCallback = isr;
    TIMSK |= _BV(OCIE1A);
}

void attachTimerInterrupt(void (*isr)(), unsigned long microseconds)  {
    if(microseconds > 0) timerSetPeriod(microseconds);
    setTimerInterrupt(isr);
}

void detachTimerInterrupt() {
    //TIMSK = 0; // Timer 0 and Timer 1 both use TIMSK register so setting it to 0 will override settings for Timer1 as well
    TIMSK &= ~_BV(OCIE1A);
}

ISR(TIMER1_COMPA_vect)
{
  (*isrCallback)();
}
