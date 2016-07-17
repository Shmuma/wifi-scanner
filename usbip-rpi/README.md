To setup RPi's side of things, you need to put script S99-export-usbip-scanner into
/etc/rc5.d.

If you're using different scanner than HP ScanJet 200, you may need to put it's
USB id in the begginning of the script.

This script does the following:
1. Inserts required kernel modules
2. Start usbipd if it's not already started
3. Finds scanner's busid
4. Bind's it's device to usbip
5. Attach device locally
6. Detach it again

Last two steps are required as ScanJet 200 has problems with USB interface
enumeration, and without attach/detach, windows won't be able to find it.

Reboot RPi and if everything goes well, you will be able to list your scanner
from windows machine using command "usbip.exe -l <rpi-ip-address>"

