"""
calculate and set camera values
for overscan in one camera setup

overscan is not uniform. It matches
image proportions - rounded

if the selected camera has post scale
you get an error - no duplaicate overscan

default overscan:
    10 / 10 pixels :: top / bottom

Select camera, call: main(); main(pixels=30)
for tests call: tests()
"""


from fractions import Fraction
import pymel.core


def set_camera_post_scale(ratio):
    cam = None

    try:
        cam = pymel.core.selected().pop().getShape()
    except:
        pass

    if cam and cam.postScale.get() == 1.0:
        cam.postScale.set(ratio)
    else:
        raise Exception('--> Camera already has post scale!')


def set_osc_resolution(pixels=10):
    rendersettings = pymel.core.PyNode('defaultResolution')
    res_x_plate = rendersettings.width.get()
    res_y_plate = rendersettings.height.get()
    image_ratio = Fraction(res_x_plate, res_y_plate)

    res_y_overscan = res_y_plate + (pixels * 2)
    overscan_scale = Fraction(res_y_overscan, res_y_plate)
    cam_postscale = Fraction(res_y_plate, res_y_overscan)

    res_x_overscan_float = float(res_x_plate / cam_postscale)
    res_x_overscan = int(round(res_x_overscan_float))

    set_camera_post_scale(float(cam_postscale))

    rendersettings.width.set(res_x_overscan)
    rendersettings.height.set(res_y_overscan)

    # return (res_x_overscan, res_y_overscan)
    return (res_x_plate,
            res_y_plate,
            res_x_overscan,
            res_y_overscan,
            res_x_overscan_float,
            overscan_scale,
            cam_postscale,
            image_ratio,
    )



def main(**kwargs):
    osc = set_osc_resolution(pixels=kwargs.get('pixels', 50))

    print('--> overscan res rounded: {0} x {1}'.format(osc[2], osc[3]))
    print('--> camera post scale: {0}'.format(osc[5]))
    print('plate resolution: {0} x {1}'.format(osc[0], osc[1]))
    print('overscan resolution: {0} x {1}'.format(osc[4], osc[3]))
    print('image ratio: {0}'.format(float(osc[7])))
    print('resolution difference: {0} x {1}'.format(osc[2] - osc[0], osc[3] - osc[1]))
    print('overscan scale: {0}'.format(osc[5]))



def tests():
    import setoverscan_tests

    try:
        reload(setoverscan_tests)
    except:
        import importlib

        importlib.reload(setoverscan_tests)

    setoverscan_tests.main()
