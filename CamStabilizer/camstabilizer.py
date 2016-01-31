#! Python2.7


"""
camera viewport stabilizer
for Maya for matchmovers

refactored code of stabilizer / fstab

select one anything with transform.
geo, locator, geo components...
activate pane with camera
or add a camera to the selection

Maya version: Maya 2015 Extension 1 + SP5
"""

import logging

try:
    import pymel.core
except ImportError:
    pymel = None


formatter = logging.Formatter('--> %(levelname)s'
                                # ': %(name)s'
                                # ': %(module)s'
                                ': %(funcName)s'
                                ': %(lineno)s'
                                ' --> %(message)s')
log = logging.getLogger(__name__)
log.handlers = []
ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.setLevel(logging.INFO)
# log.setLevel(logging.DEBUG)
log.addHandler(ch)



def get_selection():
    selection = pymel.core.selected()
    error_message = ('--> Select a transform and a camera'
                ' or click in a pane and select a transform')

    if len(selection) not in (1, 2):
        log.debug('selection not 1, 2')

        raise Exception(error_message)

    if type(selection[0]) != pymel.core.nodetypes.Transform:
        log.debug('selection is not transform type')

        if len(selection[0]) != 1:
            raise Exception(error_message)

    return selection


def get_camera():
    active_pane = pymel.core.getPanel(withFocus=True)
    selection = get_selection()
    camera = None
    camera_shape = None

    if len(selection) == 1:
        try:
            camera = pymel.core.modelPanel(active_pane, camera=True, query=True)
        except:
            pass

    if not camera and (len(selection) == 2):
        try:
            camera = selection[1]
        except:
            pass

    if camera:
        try:
            camera_shape = pymel.core.nt.Transform(camera).getShape()
        except:
            log.debug('cam shape error')
            pass

    if not isinstance(camera_shape, pymel.core.nodetypes.Camera):
        camera_shape = None

    if not camera_shape:
        message = '--> Select a transform and a camera or click in a pane and select a transform'

        raise Exception(message)

    log.debug(camera)
    log.debug(camera_shape)

    return camera


def get_position_object():
    selection = pymel.core.selected()

    if len(selection) not in (1, 2):
        message = '--> Select a transform and a camera or click in a pane and select a transform'

        raise Exception(message)

    transform = None

    transform = selection[0]

    return transform


def stabilize():
    log.debug('--> Start stabilize...')

    camera = get_camera()
    log.debug('--> camera ok...')

    aimtransform = get_position_object()
    log.debug('--> transform ok...')

    return [camera]


def main(**kwargs):
    print('/'*50)
    print('\\'*50)
    print('/'*50)

    if kwargs['task'] == 'stabilize':
        stabilize()
