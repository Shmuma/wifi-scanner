import os
import twain
from PIL import ImageFile

# ================== Options to tweak
# this string will be looked in list of twain sources
SCANNER_NAME = "scanjet"
# where images will be saved
FOLDER_TO_SAVE = "//192.168.2.10/shared/scans"
# resolution to scan
SCAN_RESOLUTION_DPI = 200
# interval between scans when new folder will be created
NEW_FOLDER_MINUTES = 2*60
# ================== No user-configurable options below


def detect_best_source(src_list):
    print "Got scanners: %s" % ", ".join(src_list)
    for src in src_list:
        if src.lower().find(SCANNER_NAME.lower()) >= 0:
            print "%s selected" % src
            return src
    return src_list[0]


def save_image(bmp_data, file_name):
    parser = ImageFile.Parser()
    parser.feed(bmp_data)
    image = parser.close()
    image.save(file_name)


if __name__ == "__main__":
    # TODO: locking
    # check directory
    if not os.path.exists(FOLDER_TO_SAVE):
        os.makedirs(FOLDER_TO_SAVE)

    # TODO: read directory structure and create new dir if needed

    sm = twain.SourceManager(0)
    src = detect_best_source(sm.GetSourceList())
    ss = sm.OpenSource(src)
    ss.SetCapability(twain.ICAP_XRESOLUTION, twain.TWTY_FIX32, float(SCAN_RESOLUTION_DPI))
    ss.SetCapability(twain.ICAP_YRESOLUTION, twain.TWTY_FIX32, float(SCAN_RESOLUTION_DPI))
    ss.RequestAcquire(0, 0)
    rv = ss.XferImageNatively()
    if rv:
        (handle, count) = rv
        bmp_data = twain.DIBToBMFile(handle)
        save_image(bmp_data, FOLDER_TO_SAVE + "/image.jpg")
