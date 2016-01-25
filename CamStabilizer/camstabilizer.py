"""
camera viewport stabilizer
for Maya for matchmovers

refactored code of stabilizer / fstab

select one anything with transform.
geo, locator, geo components...
activate pane with camera
or add a camera to the selection
"""

import logging

import pymel.core


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




def get_camera():
    active_pane = pymel.core.getPanel(withFocus=True)
    selection = pymel.core.selected()
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
            pymel.core.warning('--> Select a transform and a camera or click in a pane and select a transform')

            return None

    log.debug(camera)
    log.debug(camera_shape)

    return camera


def stabilize():
    camera = get_camera()

    return [camera]


def main(**kwargs):
    if kwargs['task'] == 'stabilize':
        stabilize()
