import datetime

if __name__ == "__main__":
    with open("c:/wifi_scanner/test.log", "a") as fd:
        fd.write("Called %s\n" % datetime.datetime.now())
