This is a windows virtual machine part of wifi scanner.

# Setup

1. Install minimal windows xp VM
2. Setup python27
3. setup twain module for 2.7: https://pypi.python.org/pypi/twain
4. setup pillow module for python 2.7 & win32: https://pypi.python.org/pypi/Pillow/2.7.0
5. run 'pip install lockfile'
6. install VC redistridutable package for VisualC 2010: https://support.microsoft.com/en-us/kb/2977003
7. copy content of this dir to c:\wifi_scanner
8. run sti_reg.exe (it should report about successfull registartion)
9. unzip included usbip-0.2.1.zip file and setup it according to it's instruction
10. setup hp scanner drivers for your scanner
11. press button on scanner, and in a dialog box select 'Scan to shared folder' and 'Always use this program'

Done!