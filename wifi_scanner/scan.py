import os
import sys
import twain
import datetime
import lockfile
import urllib
from PIL import ImageFile

# ================== Options to tweak
# this string will be looked in list of twain sources
SCANNER_NAME = "scanjet"
# network share to attach (need to have backslashes!)
NETWORK_SHARE = r"\\192.168.2.10\shared"
# folder on network share to save image
FOLDER_TO_SAVE = "scans"
# drive letter to use for network share
DRIVE_TO_ATTACH = "x:"
# resolution to scan
SCAN_RESOLUTION_DPI = 200
# interval between scans when new folder will be created
NEW_FOLDER_MINUTES = 2*60
# scanner machine dns name or address
SCANNER_ADDRESS = "pi-scanner"
# ================== No user-configurable options below


def detect_best_source(src_list):
    print "Got scanners: %s" % ", ".join(src_list)
    for src in src_list:
        if src.lower().find(SCANNER_NAME.lower()) >= 0:
            print "%s selected" % src
            return src
    return src_list[0]


def save_image(bmp_data, dir_name):
    parser = ImageFile.Parser()
    parser.feed(bmp_data)
    image = parser.close()
    file_name = os.path.join(dir_name, date_to_name(datetime.datetime.now()) + ".jpg")
    image.save(file_name)


def date_to_name(dt):
    """
    Convert datetime object into human-readable string
    representation used in dirnames and file names. It can be
    reverted back to name_to_date function
    :param dt:
    :return:
    """
    return dt.strftime("%Y-%m-%d_%H-%M-%S")


def name_to_date(s):
    """
    Convert back string representation to datetime object
    :param s:
    :return: None if wrong format detected
    """
    p = s.split("_")
    if len(p) != 2:
        return None

    try:
        p1 = map(int, p[0].split('-'))
        p2 = map(int, p[1].split('-'))
    except ValueError:
        return None

    if len(p1) != 3 or len(p2) != 3:
        return None

    return datetime.datetime(p1[0], p1[1], p1[2], p2[0], p2[1], p2[2])


def find_last_file_datetime_and_dir(path):
    """
    Check all files in subdirs in a path and return datetime corresponding to that
    :param path:
    :return: tuple of datetime and string dir. If no file found, return None,None
    """
    max_dt = None
    max_dir = None
    for entry_path in os.listdir(path):
        full_entry_path = os.path.join(path, entry_path)
        if not os.path.isdir(full_entry_path):
            continue
        if name_to_date(entry_path) is None:
            continue
        for subentry_path in os.listdir(full_entry_path):
            full_subentry_path = os.path.join(full_entry_path, subentry_path)
            if not os.path.isfile(full_subentry_path):
                continue
            dt = name_to_date(subentry_path.split(".")[0])
            if dt is None:
                continue
            if max_dt is None or max_dt < dt:
                max_dt = dt
                max_dir = full_entry_path
    print max_dt, max_dir
    return max_dt, max_dir


def make_new_dir(base_path):
    """
    Create new timestamp-based directory
    :param base_path:
    :return: path name
    """
    path = os.path.join(base_path, date_to_name(datetime.datetime.now()))
    os.makedirs(path)
    return path


def set_led_color(red, green, blue):
    """
    Change led color
    :param red: 0..255
    :param green: 0..255
    :param blue: 0..255
    """
    url = "http://{host}:8000/set_led?r={red}&g={green}&b={blue}".\
                format(host=SCANNER_ADDRESS, red=red, green=green, blue=blue)
    url_obj = urllib.urlopen(url)
    print(url_obj.read())


if __name__ == "__main__":
    base_dir = os.path.dirname(sys.argv[0])
    with lockfile.LockFile(os.path.join(base_dir, "lock")):
        # check directory
        dest_dir = os.path.join(DRIVE_TO_ATTACH + "\\", FOLDER_TO_SAVE)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        last_datetime, last_dir = find_last_file_datetime_and_dir(dest_dir)
        max_delta = datetime.timedelta(minutes=NEW_FOLDER_MINUTES)
        if last_datetime is None or datetime.datetime.now() - last_datetime > max_delta:
            last_dir = make_new_dir(dest_dir)

        set_led_color(255, 0, 0)
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
            save_image(bmp_data, last_dir)
            set_led_color(0, 0, 0)
        else:
            set_led_color(0, 0, 255)
