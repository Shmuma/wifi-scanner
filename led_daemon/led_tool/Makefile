all: led_tool 

led_tool: led_tool.c
	gcc -o led_tool -g -O3 -lwiringPi led_tool.c

test_slow: test_slow.c
	gcc -o test_slow -g -O3 test_slow.c -lwiringPi

clean:
	rm led_tool test_slow