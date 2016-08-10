all: led_tool led_tool_ll

led_tool: led_tool.c
	gcc -o led_tool -g -O3 -lwiringPi led_tool.c

led_tool_ll: led_tool_ll.c
	gcc -o led_tool_ll -g -O3 led_tool_ll.c

clean:
	rm led_tool