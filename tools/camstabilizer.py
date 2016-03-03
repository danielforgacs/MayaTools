#! Python2.7


"""
camera viewport stabilizer
for Maya for matchmovers

refactored code of stabilizer / fstab

select vertex or locator activate pane with camera
or add a camera to the selection

>>> get_screen_pos() returns
geo mormalized screen positions for 2D transforms
"""

import logging

try:
    import pymel.core
    import maya.cmds as cmds
except:
    pm = None
    cmds = None


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
        message = ('--> Select a transform and a camera'
                    ' or click in a pane and select a transform')

        raise Exception(message)

    offset_h = camera_shape.getHorizontalFilmOffset() != 0
    offset_v = camera_shape.getVerticalFilmOffset() != 0

    if offset_h or offset_v:
        raise Exception('--> Camera Has Not Zero Offset Value...')

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
        raise Exception("--> can't get transform."
                        " Select vertex or locator..")

    return transform


def create_expression(cam, pos, pan=True):
    expression = (
        '\n// {camshape}'
        '\n// {pos}'
        '\n// {parm_h}'
        '\n// {parm_v}'
        '\npython "import maya.cmds as cmds";'
        '\npython "from {module_} import get_screen_pos";'
        '\npython "reload(get_screen_pos)";'
        '\npython "fov_h = cmds.camera (\'{camshape}\', query=True, horizontalFieldOfView=True)";'
        '\npython "fov_v = cmds.camera (\'{camshape}\', query=True, verticalFieldOfView=True)";'
        '\npython "aperture_h = cmds.camera (\'{camshape}\', query=True, horizontalFilmAperture=True)";'
        '\npython "aperture_v = cmds.camera (\'{camshape}\', query=True, verticalFilmAperture=True)";'
        '\n$pos =`python "get_screen_pos(\'{pos}\',\'{camtransform}\', fov_h, fov_v,aperture_h, aperture_v)"`;'
        '\nsetAttr "{camshape}.panZoomEnabled" 1;'
        '\nsetAttr "{camshape}.{parm_h}" ($pos[2]);'
        '\nsetAttr "{camshape}.{parm_v}" ($pos[3]);'
    )

    camparm_h = 'horizontalPan' if pan else 'horizontalFilmOffset'
    camparm_v = 'verticalPan' if pan else 'verticalFilmOffset'

    expression = expression.format(
                    camshape=cam.fullPathName(),
                    parm_h=camparm_h,
                    parm_v=camparm_v,
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


def get_screen_pos(point, camera, fieldOfView_h,
            fieldOfView_v, aperture_h, aperture_v):
    """
    called from camera expression

    PxScreen, PyScreen is the normalized position in 2D camera space
    export it to get 2D tracks for compositing softwares

    returns list:
        normalized x & y screen position for export to 2D transforms,
        camera shape film offset x & y
    """

    from math import tan, radians

    PPosWrld = cmds.xform(point, query=True,
            worldSpace=True, translation=True)
    camWrldInvMatrix = cmds.getAttr(camera+'.worldInverseMatrix')

    Px = PPosWrld[0]*camWrldInvMatrix[0]+PPosWrld[1] \
            *camWrldInvMatrix[4]+PPosWrld[2] \
            *camWrldInvMatrix[8]+1*camWrldInvMatrix[12]

    Py = PPosWrld[0]*camWrldInvMatrix[1]+PPosWrld[1] \
            *camWrldInvMatrix[5]+PPosWrld[2] \
            *camWrldInvMatrix[9]+1*camWrldInvMatrix[13]

    Pz = PPosWrld[0]*camWrldInvMatrix[2]+PPosWrld[1] \
            *camWrldInvMatrix[6]+PPosWrld[2] \
            *camWrldInvMatrix[10]+1*camWrldInvMatrix[14]

    PxScreen = (Px/-Pz)/tan(radians(fieldOfView_h/2))/(2.0)+0.5
    PyScreen = (Py/-Pz)/tan(radians(fieldOfView_v/2))/(2.0)+0.5

    FilmOffsetX = (PxScreen-0.5)*aperture_h
    FilmOffsetY = (PyScreen-0.5)*aperture_v

    return [PxScreen, PyScreen, FilmOffsetX, FilmOffsetY]


def stabilize():
    log.debug('--> Start stabilize...')

    camera = get_camera()
    log.debug('--> camera ok...')

    transform = get_position_object()
    log.debug('--> transform ok...')

    expression = create_expression(camera, transform)
    log.debug('--> transform ok...')

    expression_node = setup_expression_node(expression,
                                            camera.name(),
                                            task='create')
    log.debug('--> expression node ok...')

    return (transform, camera, expression, expression_node)


def clear_stabilizer_OBSOLETE():
    if not pymel.core.objExists('test_cameraShape_stabilizer'):
        raise Exception('--> Stabilizer is turned off...')

    else:
        expr_node = pymel.core.PyNode('test_cameraShape_stabilizer')
        campath = expr_node.getExpression().split('\n')[0][3:]
        pymel.core.delete('test_cameraShape_stabilizer')
        camera_shape = pymel.core.PyNode(campath)

        camera_shape.setHorizontalFilmOffset(0)
        camera_shape.setVerticalFilmOffset(0)


def clear_stabilizer():
    stabexpression = [node for node in pymel.core.ls(exactType=
            'expression') if 'stabilizer' in node.name()]

    if len(stabexpression) > 1:
        raise Exception('--> There are more than one'
                        ' stabilized camera in the scene...')

    for node in stabexpression:
        exprstring = node.expression.get()
        camname = exprstring.splitlines()[0][3:]
        camparm_h = exprstring.splitlines()[2][3:]
        camparm_v = exprstring.splitlines()[3][3:]
        cam = pymel.core.PyNode(camname)
        pymel.core.delete(node)
        # cam.horizontalFilmOffset.set(0)
        # cam.verticalFilmOffset.set(0)
        cam.setAttr(camparm_h, 0)
        cam.setAttr(camparm_v, 0)


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
        clear_stabilizer()
        pymel.core.inViewMessage(
                assistMessage ='cam stab turned off...',
                pos='midCenter',
                fade=True,
                fadeOutTime=2
            )


if __name__ == '__main__':
    pass