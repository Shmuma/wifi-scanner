
//
//  How to access GPIO registers from C-code on the Raspberry-Pi
//  Example program
//  15-January-2012
//  Dom and Gert
//  Revised: 15-Feb-2013


// Access from ARM Running Linux

#define BCM2708_PERI_BASE        0x20000000
#define GPIO_BASE                (BCM2708_PERI_BASE + 0x200000) /* GPIO controller */


#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>

#define PAGE_SIZE (4*1024)
#define BLOCK_SIZE (4*1024)

int  mem_fd;
#include <time.h>
#include <wiringPi.h>

void *gpio_map;

// I/O access
volatile unsigned *gpio;


// GPIO setup macros. Always use INP_GPIO(x) before using OUT_GPIO(x) or SET_GPIO_ALT(x,y)
#define INP_GPIO(g) *(gpio+((g)/10)) &= ~(7<<(((g)%10)*3))
#define OUT_GPIO(g) *(gpio+((g)/10)) |=  (1<<(((g)%10)*3))
#define SET_GPIO_ALT(g,a) *(gpio+(((g)/10))) |= (((a)<=3?(a)+4:(a)==4?3:2)<<(((g)%10)*3))

#define GPIO_SET *(gpio+7)  // sets   bits which are 1 ignores bits which are 0
#define GPIO_CLR *(gpio+10) // clears bits which are 1 ignores bits which are 0

#define GET_GPIO(g) (*(gpio+13)&(1<<g)) // 0 if LOW, (1<<g) if HIGH

#define D1_ZERO 200L
#define D0_ZERO 450L
#define D1_ONE 400L
#define D0_ONE 200L
#define GAP_DELAY 30000L

// Calibrated timings
unsigned send_zero_1_loop;
unsigned send_zero_0_loop;
unsigned send_one_1_loop;
unsigned send_one_0_loop;
unsigned gap_loop;

// decoded sequence to set led color. Every entry is count of iterations we need to wait at output level.
// https://cdn-shop.adafruit.com/datasheets/WS2812B.pdf
// Structure: 
//   2 -- we have two levels for every bit to send
//   8 -- we have eight bits for every color channel
//   3 -- we have three color channels
// This sequence values is based on calibration timings and filled by decode_sequence function
unsigned sequence[2*8*3];


void setup_io();
void calibrate(int);
void send_rgb(int, int, int);
void decode_sequence(int, int, int);
void send_sequence();

int main(int argc, char **argv)
{
    int i;
    int bright = 255;
    int delta = -20;
    // Set up gpi pointer for direct register access
    setup_io();
    
    calibrate(1000000);

    // Set GPIO pin 4 to output
    INP_GPIO(4); // must use INP_GPIO before we can use OUT_GPIO
    OUT_GPIO(4);

    while (1) {
        decode_sequence(bright, 0, 0);
        send_sequence();
        sleep(1);
        decode_sequence(0, bright, 0);
        send_sequence();
        sleep(1);
        decode_sequence(0, 0, bright);
        send_sequence();
        sleep(1);

        if (bright+delta <= 0 || bright+delta >= 255)
            delta = -delta;

        bright += delta;
    }
  
    return 0;
} // main


//
// Set up a memory regions to access GPIO
//
void setup_io()
{
   /* open /dev/mem */
   if ((mem_fd = open("/dev/mem", O_RDWR|O_SYNC) ) < 0) {
      printf("can't open /dev/mem \n");
      exit(-1);
   }

   /* mmap GPIO */
   gpio_map = mmap(
      NULL,             //Any adddress in our space will do
      BLOCK_SIZE,       //Map length
      PROT_READ|PROT_WRITE,// Enable reading & writting to mapped memory
      MAP_SHARED,       //Shared with other processes
      mem_fd,           //File to map
      GPIO_BASE         //Offset to GPIO peripheral
   );

   close(mem_fd); //No need to keep mem_fd open after mmap

   if (gpio_map == MAP_FAILED) {
      printf("mmap error %d\n", (int)gpio_map);//errno also set!
      exit(-1);
   }

   // Always use volatile pointer!
   gpio = (volatile unsigned *)gpio_map;


} // setup_io


void calibrate(int count) {
    int i;
    double single_ns;
    struct timespec time_1;
    struct timespec time_2;

    clock_gettime(CLOCK_MONOTONIC_RAW, &time_1);
    for (i = 0; i < count; i++) {
        GPIO_CLR = 1<<4;
    }
    clock_gettime(CLOCK_MONOTONIC_RAW, &time_2);

    single_ns = (double)(time_2.tv_nsec - time_1.tv_nsec) / count;
    printf("calibrate %d: delta = %ld, single=%.4f\n", count, time_2.tv_nsec - time_1.tv_nsec, single_ns);

    send_zero_1_loop = (unsigned)(400 / single_ns);
    send_zero_0_loop = (unsigned)(850 / single_ns);
    send_one_1_loop = (unsigned)(800 / single_ns);
    send_one_0_loop = (unsigned)(450 / single_ns);
    gap_loop = (int)(50000 / single_ns);

    printf("zero_1: %d, zero_0: %d\n", send_zero_1_loop, send_zero_0_loop);
    printf("one_1:  %d, one_0:  %d\n", send_one_1_loop, send_one_0_loop);
    printf("gap: %d\n", gap_loop);
}


void send_rgb(int r, int g, int b) {
    int i, k;

    for (k = 0; k < 8; k++) {
        for (i = 0; i < (g == 0 ? send_zero_1_loop : send_one_1_loop); i++)
            GPIO_SET = 1<<4;
        for (i = 0; i < (g == 0 ? send_zero_0_loop : send_one_0_loop); i++)
            GPIO_CLR = 1<<4;
    }
    for (k = 0; k < 8; k++) {
        for (i = 0; i < (r == 0 ? send_zero_1_loop : send_one_1_loop); i++)
            GPIO_SET = 1<<4;
        for (i = 0; i < (r == 0 ? send_zero_0_loop : send_one_0_loop); i++)
            GPIO_CLR = 1<<4;
    }
    for (k = 0; k < 8; k++) {
        for (i = 0; i < (b == 0 ? send_zero_1_loop : send_one_1_loop); i++)
            GPIO_SET = 1<<4;
        for (i = 0; i < (b == 0 ? send_zero_0_loop : send_one_0_loop); i++)
            GPIO_CLR = 1<<4;
    }

    for (i = 0; i < gap_loop; i++)
        GPIO_CLR = 1<<4;
}


void send_sequence() {
    int i, k;
    unsigned t;

    for (k = 0; k < 10; k++) {
        for (i = 0; i < sizeof(sequence) / sizeof(sequence[0]); i += 2) {
            t = sequence[i];
            while (t > 0) {
                GPIO_SET = 1<<4;
                t--;
            }
            t = sequence[i+1];
            while (t > 0) {
                GPIO_CLR = 1<<4;
                t--;
            }
        }

        for (i = 0; i < gap_loop; i++)
            GPIO_CLR = 1<<4;        
    }
}


void decode_color(unsigned* buf, int val) {
    int bit;
    int bit_val;

    for (bit = 7; bit >= 0; bit--) {
        bit_val = val % 2;
        if (bit_val) {
            buf[bit*2] = send_one_1_loop;
            buf[bit*2+1] = send_one_0_loop;
        }
        else {
            buf[bit*2] = send_zero_1_loop;
            buf[bit*2+1] = send_zero_0_loop;
        }
        val >>= 1;
    }
}


void decode_sequence(int r, int g, int b) {
    decode_color(sequence, g);
    decode_color(&sequence[2*8], r);
    decode_color(&sequence[2*8*2], b);
}


