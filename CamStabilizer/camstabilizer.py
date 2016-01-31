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


###
###
###
pm.inViewMessage(
    assistMessage ='<MESSAGE COMES HERE',
    pos='midCenter',
    fade=True,
    fadeOutTime=2
    )

###
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
    expression = '// {0}'.format(cam.fullPathName())
    expression += '\n// {0}'.format(pos)
    expression += '\npython "import maya.cmds as cmds";'
    expression += ("""\npython "fov_h = cmds.camera"""
                    """ ('{0}', query = True,"""
                    """ horizontalFieldOfView = True)";""").format(cam.fullPathName())
    expression += ("""\npython "fov_v = cmds.camera"""
                    """ ('{0}',"""
                    """ query = True, verticalFieldOfView = True)";""").format(cam.fullPathName())



        # python "aperture_h = cmds.camera ('|test_locator|test_camera|test_cameraShape', query = True, horizontalFilmAperture = True)";
        # python "aperture_v = cmds.camera ('|test_locator|test_camera|test_cameraShape', query = True, verticalFilmAperture = True)";
        # $pos =`python "fstab.get_normalized_screen_position('|test_box.vtx[4]','|test_locator|test_camera',fov_h, fov_v,aperture_h,aperture_v)"`;
        # setAttr "|test_locator|test_camera|test_cameraShape.horizontalFilmOffset" $pos[2];
        # setAttr "|test_locator|test_camera|test_cameraShape.verticalFilmOffset" $pos[3];

    expression_node = pymel.core.expression()
    expression_node.rename('camera_stabilizer_' + cam.name())

    print('~@~'*5)
    print(expression)
    print('~@~'*5)

    return expression, expression_node


def stabilize():
    log.debug('--> Start stabilize...')

    camera = get_camera()
    log.debug('--> camera ok...')

    transform = get_position_object()
    log.debug('--> transform ok...')

    expression, expression_node = create_expression(camera, transform)
    log.debug('--> transform ok...')

    return (transform, camera, expression, expression_node)


def main(**kwargs):
    if kwargs['task'] == 'stabilize':
        stabilize()
