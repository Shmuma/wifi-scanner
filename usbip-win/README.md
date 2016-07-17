# USBIP, windows patches

USBIP consists of three parts
  1. linux driver, it is maintained by linux-usb community and resides in
     linux-kernel source tree
  2. windows driver, which looks abandoned since 2012, git repo is there:
     git://git.code.sf.net/p/usbip/git-windows
  3. userspace tools (usbip and usbipd), which originally were cross-platform
     (linux, windows and macosx), but currently maintained part is linux-only and
     resides in linux kernel tree under tools/usb/usbip

As we need windows version of tools, they need to be grabbed from git-windows
version on sf.net, which is not latest version and contains several weird
bugs. I've fixed them (patches are in *.patch files) and rebuilt tools. Both
driver and those fixed tools can be found in zip archive.

