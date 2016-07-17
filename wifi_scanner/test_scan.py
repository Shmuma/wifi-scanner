import twain

def detect_best_source(src_list):
    for src in src_list:
        if src.lower().find("scanjet") >= 0:
            print src
            return src
    return src_list[0]

sm = twain.SourceManager(0)
src = detect_best_source(sm.GetSourceList())
ss = sm.OpenSource(src)
ss.RequestAcquire(0,0)
rv = ss.XferImageNatively()
if rv:
    (handle, count) = rv
    twain.DIBToBMFile(handle, 'c:/wifi_scanner/image.bmp')
