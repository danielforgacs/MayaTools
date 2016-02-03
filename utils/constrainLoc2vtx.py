#! python2

__author__      = 'forgacs.daniel@gmail.com'


"""
create and constrain a locator
to a vertex with an expression
"""


import pymel.core


def constrain_loc_to_vtx():
    selection = pymel.core.selected(long=True, absoluteName=True, flatten=True, head=2)
    vtx = selection.pop(0)
    geo = pymel.core.PyNode(vtx.node())
    locator = pymel.core.spaceLocator()
    locator = locator.rename('locator_vertexConstrained')
    expression = (
            """float $BBoxSize = test_cube.boundingBoxMinX;"""
            """\n\n$vertexWorldPos = `pointPosition -world test_cube.vtx[1]`;"""
            """\nlocator_vertexConstrained.translateX = $vertexWorldPos[0];"""
            """\nlocator_vertexConstrained.translateY = $vertexWorldPos[1];"""
            """\nlocator_vertexConstrained.translateZ = $vertexWorldPos[2];"""
            )
    expression = expression.format()
    pymel.core.expression(name=locator.name(), string=expression)
