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

        if isinstance(selection[0], pymel.core.nodetypes.Camera):
            raise Exception(error_message)

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

    return camera_shape


def get_position_object():
    selection = get_selection()
    transform = selection[0]
    locator = False
    vertex = False

    if hasattr(transform, 'getShape'):
        locator = type(transform.getShape()) is pymel.core.nodetypes.Locator

    else:
        vertex = type(transform) is pymel.core.general.MeshVertex

    if not (locator or vertex):
        raise Exception("--> can't retrieve transform...")

    return transform


def create_expression(cam, pos):
    expression = """
// {camshape}
// {pos}
python "import maya.cmds as cmds";
python "fov_h = cmds.camera ('{camshape}', query = True, horizontalFieldOfView = True)";
python "fov_v = cmds.camera ('{camshape}', query = True, verticalFieldOfView = True)";
python "aperture_h = cmds.camera ('{camshape}', query = True, horizontalFilmAperture = True)";
python "aperture_v = cmds.camera ('{camshape}', query = True, verticalFilmAperture = True)";
$pos =`python "fstab.get_normalized_screen_position('{pos}','{camtransform}',fov_h, fov_v,aperture_h,aperture_v)"`;
setAttr "{camshape}.horizontalFilmOffset" $pos[2];
setAttr "{camshape}.verticalFilmOffset" $pos[3];
"""
    expression = expression.format(
            camshape=cam.fullPathName(),
            pos=pos,
            camtransform=cam,
            )

    return expression


def setup_expression_node(expression, camname, **kwargs):
    if kwargs.get('task', None) is 'create':
        expression_node = pymel.core.expression()
        expression_node.rename(camname + '_stabilizer')

        return expression_node

    else:
        pass


def stabilize():
    log.debug('--> Start stabilize...')

    camera = get_camera()
    log.debug('--> camera ok...')

    transform = get_position_object()
    log.debug('--> transform ok...')

    expression = create_expression(camera, transform)
    log.debug('--> transform ok...')

    expression_node = setup_expression_node(expression, camera.name(), task='create')
    log.debug('--> expression node ok...')

    return (transform, camera, expression, expression_node)


def main(**kwargs):
    if kwargs['task'] == 'stabilize':
        stabilize()
        pymel.core.inViewMessage(assistMessage ='camera stabilized',
                                pos='midCenter',
                                fade=True,
                                fadeOutTime=2
                            )

    elif kwargs['task'] == 'clear':
        pymel.core.inViewMessage(assistMessage ='cam stab turned off...',
                                pos='midCenter',
                                fade=True,
                                fadeOutTime=2
                            )
