#include <wiringPi.h>

void send_color(int value) {
    int mask = 1 << 7;
    while (mask > 0) {
        if (value & mask) {
            digitalWrite(0, 1);
            digitalWrite(0, 1);
            digitalWrite(0, 0);
        }
        else {
            digitalWrite(0, 1);
            digitalWrite(0, 0);
            digitalWrite(0, 0);            
        }
        mask >>= 1;
    }
}

int main (void)
{
    int i;

    wiringPiSetup ();
    pinMode (0, OUTPUT);

    int red = 0, green = 0, blue = 0;
    int dr = 1, dg = 0, db = 0;

    for (;;) {
        send_color(red);
        send_color(green);
        send_color(blue);

        red += dr;
        if (red == 255)
            dr = -1;
        if (red == 0)
            dr = 1;

        /*
        if (dr != 0)
            red += dr;
        if (dg != 0)
            green += dg;
        if (db != 0)
            blue += db;

        if (red == 255)
            dr = -1;
        if (dr != 0 && red == 0) {
            dr = 0;
            dg = 1;
        }

        if (green == 255)
            dg = -1;
        if (dg != 0 && green == 0) {
            dg = 0;
            db = 1;
        }

        if (blue == 255)
            db = -1;
        if (db != 0 && blue == 0) {
            db = 0;
            dr = 1;
        }
        */

        digitalWrite(0, LOW);
        //        delayMicroseconds (60);
        delay(500);
    }
    return 0;
}
