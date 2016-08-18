#!/usr/bin/env python3
import os
import sys
import stat
import os.path
import argparse
import logging as log

import time
import subprocess
from flask import Flask, request

app = Flask(__name__)


def sanity_checks(led_tool):
    if not os.path.isfile(led_tool):
        log.error("Led tool not found (%s)" % args.led_tool)
        return False

    st = os.stat(led_tool)
    mode = st.st_mode
    if (mode & stat.S_IEXEC) == 0:
        log.error("Led tool is not executable")
        return False
    if (mode & stat.S_ISUID) == 0:
        log.error("Suid bit on let tool isn't set")
        return False
    if st.st_uid != 0:
        log.error("Led tool must be chowned to root")
        return False
    return True


def set_led_color(led_tool, red, green, blue):
    """
    Launch led tool
    :param led_tool: path to tool used to change led color
    :param red: intensity from 0 to 255
    :param green:
    :param blue:
    """
    args = [led_tool, str(red), str(green), str(blue)]
    retcode = subprocess.call(args)
    log.info("%s returned %d", " ".join(args), retcode)


def initial_test(led_tool):
    set_led_color(led_tool, 255, 0, 0)
    time.sleep(1)
    set_led_color(led_tool, 0, 255, 0)
    time.sleep(1)
    set_led_color(led_tool, 0, 0, 255)
    time.sleep(1)
    set_led_color(led_tool, 0, 0, 0)
    set_led_color(led_tool, 0, 0, 0)
    set_led_color(led_tool, 0, 0, 0)


@app.route("/set_led")
def request_set_led():
    red = int(request.args.get('r', '0'))
    green = int(request.args.get('g', '0'))
    blue = int(request.args.get('b', '0'))

    set_led_color(app.led_tool_path, red, green, blue)
    return "OK!"


if __name__ == "__main__":
    log.basicConfig(format="%(asctime)-15s %(levelname)s %(message)s", level=log.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("--no-sanity-check", action='store_false', dest='sanity_check', default=True)
    parser.add_argument("--no-initial-test", action='store_false', dest='initial_test', default=True)
    parser.add_argument("-p", "--port", type=int, default=8000, help="Port to listen")
    parser.add_argument("--led_tool", type=str, default="./led_tool", help="Path to led_tool")
    args = parser.parse_args()

    if args.sanity_check:
        if not sanity_checks(args.led_tool):
            sys.exit(1)

    if args.initial_test:
        initial_test(args.led_tool)

    app.led_tool_path = args.led_tool
    app.run(host='0.0.0.0', port=args.port)
