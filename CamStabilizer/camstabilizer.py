import pymel.core


def get_camera():
    panel = pymel.core.getPanel(withFocus=True)
    camera = 'cam1'

    return camera


def stabilize():
    camera = get_camera()


def main(**kwargs):
    if kwargs['task'] == 'stabilize':
        stabilize()
