"""
calculate and set camera values
for overscan in one camera setup

overscan is not uniform. It matches
image proportions

default overscan:
    10 / 10 pixels :: left / right


###
w = 1920.0
h = 1440.0
w_osc = 1980
w_extra = w_osc - w
osc_factor = w / w_osc
h_osc = h / osc_factor

print '\\noriginal res: ', w, '*', h
print 'overscan res', w_osc, '*', h_osc
print 'overscan factor (uniform)', osc_factor
print 'extra pixels (width, height)', w_osc - w, h_osc - h
###
"""


def set_camera_post_scale(ratio):
    postscale = None

    return postscale


def set_overscan(pixels=10):
    pass

def main():
    pass


def test():
    import setoverscan_tests

    try:
        reload(setoverscan_tests)
    except:
        import importlib

        importlib.reload(setoverscan_tests)

    setoverscan_tests.main()
