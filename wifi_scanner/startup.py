"""
Started every time win computer boots to:
1. attach network share
2. detect available usbip devices
3. attach usbip device
"""
import logging as log
import subprocess
import sys

from scan import NETWORK_SHARE, DRIVE_TO_ATTACH, SCANNER_ADDRESS


def get_usbip_exported(address):
    out = subprocess.check_output(['usbip.exe', '-l', address], stderr=subprocess.STDOUT)
    out = out.split("\n")
    result = []
    for idx, line in enumerate(out):
        if line.startswith("- "):
            v = out[idx+1].split(":")[0].strip()
            result.append(v)
    return result

def usbip_attach(address, busid):
    ret = subprocess.call(["usbip.exe", "-a", address, busid])
    log.error("Usbip attach exited with code %d", ret)


if __name__ == "__main__":
    log.basicConfig(level=log.INFO, format="%(asctime)-15s %(levelname)s %(message)s", filename="startup.log")

    log.info("Attaching %s to drive %s", NETWORK_SHARE, DRIVE_TO_ATTACH)
    ret = subprocess.call(["net", "use", DRIVE_TO_ATTACH, NETWORK_SHARE])
    log.info("Net use returned code %d", ret)

    usbip_exported = get_usbip_exported(SCANNER_ADDRESS)
    if len(usbip_exported) > 1:
        log.error("Scanner host exports more than one device, fatal")
        sys.exit(1)
    if len(usbip_exported) == 0:
        log.error("Scanner host doesn't export usbip devices")
        sys.exit(1)
    log.info("Attaching usbip device from %s, busid %s", SCANNER_ADDRESS, usbip_exported[0])
    usbip_attach(SCANNER_ADDRESS, usbip_exported[0])