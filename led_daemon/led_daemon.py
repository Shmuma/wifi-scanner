#!/usr/bin/env python3
import os
import sys
import stat
import os.path
import argparse
import logging as log



def sanity_checks(args):
    if not os.path.isfile(args.led_tool):
        log.error("Led tool not found (%s)" % args.led_tool)
        return False

    st = os.stat(args.led_tool)
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


if __name__ == "__main__":
    log.basicConfig(format="%(asctime)-15s %(levelname)s %(message)s", level=log.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8000, help="Port to listen")
    parser.add_argument("--led_tool", type=str, default="./led_tool", help="Path to led_tool")
    args = parser.parse_args()

    if not sanity_checks(args):
        sys.exit(1)
