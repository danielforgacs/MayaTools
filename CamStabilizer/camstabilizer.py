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

try:
    import maya.cmds as cmds
except ImportError:
    maya = None


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
$pos =`python "{module_}.get_normalized_screen_position('{pos}','{camtransform}',fov_h, fov_v,aperture_h,aperture_v)"`;
setAttr "{camshape}.horizontalFilmOffset" $pos[2];
setAttr "{camshape}.verticalFilmOffset" $pos[3];
"""
    expression = expression.format(
            camshape=cam.fullPathName(),
            pos=pos,
            camtransform=cam,
            module_=__name__
            )

    return expression


def setup_expression_node(expression, camname, **kwargs):
    if kwargs.get('task', None) is 'create':
        nodename = camname + '_stabilizer'

        if pymel.core.objExists(nodename):
            raise Exception('--> camera is already stabilized...')

        expression_node = pymel.core.expression()
        expression_node.rename(nodename)
        expression_node.setExpression(expression)

        return expression_node


def get_normalized_screen_position  (point, camera, fieldOfView_h, fieldOfView_v, aperture_h, aperture_v):
    from math import tan, radians

    _pointWorldPos = cmds.xform (point, query = True, worldSpace = True, translation = True)
    _camWorldInverseMatrix = cmds.getAttr (camera + '.worldInverseMatrix')

    _posX = _pointWorldPos[0] * _camWorldInverseMatrix[0] + _pointWorldPos[1] * _camWorldInverseMatrix[4] + _pointWorldPos[2] * _camWorldInverseMatrix[8] + 1 * _camWorldInverseMatrix[12]
    _posY = _pointWorldPos[0] * _camWorldInverseMatrix[1] + _pointWorldPos[1] * _camWorldInverseMatrix[5] + _pointWorldPos[2] * _camWorldInverseMatrix[9] + 1 * _camWorldInverseMatrix[13]
    _posZ = _pointWorldPos[0] * _camWorldInverseMatrix[2] + _pointWorldPos[1] * _camWorldInverseMatrix[6] + _pointWorldPos[2] * _camWorldInverseMatrix[10] + 1 * _camWorldInverseMatrix[14]

    _screenPosX = (_posX / -_posZ) / tan (radians (fieldOfView_h / 2)) / (2.0) + 0.5
    _screenPosY = (_posY / -_posZ) / tan (radians (fieldOfView_v / 2)) / (2.0) + 0.5

    _cameraFilmOffsetX = (_screenPosX - 0.5) * aperture_h
    _cameraFilmOffsetY = (_screenPosY - 0.5) * aperture_v

    # _screenPos is the normalized position in 2D camera space
    # export it to get 2D tracks for compositing softwares
    return [_screenPosX, _screenPosY, _cameraFilmOffsetX, _cameraFilmOffsetY]


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
        pymel.core.inViewMessage(
                assistMessage ='camera is stabilized, turn off for renders!',
                pos='midCenter',
                fade=True,
                fadeOutTime=2
            )

    elif kwargs['task'] == 'clear':
        pymel.core.inViewMessage(
                assistMessage ='cam stab turned off...',
                pos='midCenter',
                fade=True,
                fadeOutTime=2
            )
