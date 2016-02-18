"""
calculate and set camera values
for overscan in one camera setup

overscan is not uniform. It matches
image proportions

default overscan:
    10 / 10 pixels :: left / right

without selection only the render
resolution is set!
render resolution is always set!
"""


from fractions import Fraction
import pymel.core


def set_camera_post_scale(ratio):
    cam = None

    try:
        cam = pymel.core.selected().pop().getShape()
    except:
        pass

    # assert cam.getAttr('postScale') == 1.0

    if cam and cam.getAttr('postScale') == 1.0:
        cam.setAttr('postScale', ratio)
    else:
        raise Exception('--> Camera already has post scale!')


def set_osc_resolution(pixels):
    rendersettings = pymel.core.PyNode('defaultResolution')
    res_x = rendersettings.getAttr('width')
    res_y = rendersettings.getAttr('height')
    image_ratio = Fraction(res_x, res_y)
    res_y_new = res_y+(pixels*2)
    postscale_ratio = Fraction(res_y, res_y_new)
    res_x_new = float(res_y_new * image_ratio)

    rendersettings.setAttr('width', res_x_new)
    rendersettings.setAttr('height', res_y_new)

    set_camera_post_scale(float(postscale_ratio))

    return (res_x_new, res_y_new)



def main(**kwargs):
    set_osc_resolution(pixels=kwargs.get('pixels', 10))



def test():
    import setoverscan_tests

    try:
        reload(setoverscan_tests)
    except:
        import importlib

        importlib.reload(setoverscan_tests)

    setoverscan_tests.main()
