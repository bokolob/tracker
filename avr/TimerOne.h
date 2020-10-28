#ifndef TimerOne_h_
#include <avr/io.h>
#include <avr/interrupt.h>
#define TimerOne_h_

    void timer_start();
    void timer_stop();
    void timer_restart();
    void timer_resume();
    void timerSetInterrupt(void (*isr)());
    void attachTimerInterrupt(void (*isr)(), unsigned long microseconds);
    void timerDetachInterrupt();
    void timerSetPeriod(unsigned long microseconds);
    void timerInitialize(unsigned long microseconds);
#endif
