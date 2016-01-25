import logging

import pymel.core


formatter = logging.Formatter('--> %(levelname)s'
                                ': %(name)s'
                                ': %(module)s'
                                ': %(funcName)s'
                                ': %(lineno)s'
                                ' --> %(message)s')
log = logging.getLogger(__name__)
log.handlers = []
ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.setLevel(logging.INFO)
log.addHandler(ch)




def get_camera():
    active_pane = pymel.core.getPanel(withFocus=True)
    camera = pymel.core.modelPanel(active_pane, camera=True, query=True)

    log.debug(active_pane)
    log.debug(type(active_pane))
    log.debug(camera)

    return camera


def stabilize():
    camera = get_camera()


def main(**kwargs):
    if kwargs['task'] == 'stabilize':
        stabilize()
