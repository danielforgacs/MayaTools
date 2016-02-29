"""
calculate and set camera values
for overscan in one camera setup

overscan is not uniform. It matches
image proportions - rounded

if the selected camera has post scale
you get an error - no duplaicate overscan

default overscan:
    50 / 50 pixels :: top / bottom

Select camera, call: main(); main(pixels=30)
for tests call: tests()
"""


from fractions import Fraction
import decimal

try:
    import pymel.core
except:
    pm = None


# def set_camera_post_scale_OBSOLTET(ratio):
#     cam = None

#     try:
#         cam = pymel.core.selected().pop().getShape()
#     except:
#         pass

#     if cam and cam.postScale.get() == 1.0:
#         cam.postScale.set(ratio)
#     else:
#         raise Exception('--> Camera already has post scale!')


# def set_osc_resolution_OBSOLETE(pixels=10):
#     rendersettings = pymel.core.PyNode('defaultResolution')
#     res_x_plate = rendersettings.width.get()
#     res_y_plate = rendersettings.height.get()
#     image_ratio = Fraction(res_x_plate, res_y_plate)

#     res_y_overscan = res_y_plate + (pixels * 2)
#     overscan_scale = Fraction(res_y_overscan, res_y_plate)
#     cam_postscale = Fraction(res_y_plate, res_y_overscan)

#     res_x_overscan_float = float(res_x_plate / cam_postscale)
#     res_x_overscan = int(round(res_x_overscan_float))

#     set_camera_post_scale(float(cam_postscale))

#     rendersettings.width.set(res_x_overscan)
#     rendersettings.height.set(res_y_overscan)

#     # return (res_x_overscan, res_y_overscan)
#     return (res_x_plate,
#             res_y_plate,
#             res_x_overscan,
#             res_y_overscan,
#             res_x_overscan_float,
#             overscan_scale,
#             cam_postscale,
#             image_ratio,
#     )


def get_osc_values(resx, resy, pixels):
    x = decimal.Decimal(resx)
    y = decimal.Decimal(resy)
    resy_osc = y + (pixels * 2)
    osc_scale = resy_osc / y
    postscale = 1 / osc_scale
    resx_osc = x * osc_scale

    return {
            'x_osc': int(round(resx_osc)),
            'y_osc': int(resy_osc),
            'postscale': postscale,
            'x': resx,
            'y': resy,
            'x_osc_float': resx_osc,
            'osc_scale': osc_scale,
            'ratio': resx / resy,
            }



def main(**kwargs):
    resx = kwargs.get('resx', 2048)
    resy = kwargs.get('resy', 1152)
    pixels = kwargs.get('pixels', 50)

    values = get_osc_values(resx, resy, pixels)

    # osc = set_osc_resolution(pixels=kwargs.get('pixels', 50))

    print('\n--> overscan res (rounded): {0} x {1}'.format(values['x_osc'], values['y_osc']))
    print('--> camera post scale: {0}'.format(values['postscale']))
    print('\nplate resolution: {0} x {1}'.format(values['x'], values['y']))
    print('overscan resolution: {0} x {1}'.format(values['x_osc_float'], values['y_osc']))
    print('overscan scale: {0}'.format(values['osc_scale']))
    print('image ratio: {0}'.format(values['ratio']))
    print('resolution difference: {0} x {1}'.format(values['x_osc'] - values['x'], values['y_osc'] - values['y']))



def tests():
    import setoverscan_tests

    try:
        reload(setoverscan_tests)
    except:
        import importlib

        importlib.reload(setoverscan_tests)

    setoverscan_tests.main()


if __name__ == '__main__':
    main()