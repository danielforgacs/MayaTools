#! python2

__author__      = 'forgacs.daniel@gmail.com'


"""
create and constrain a locator
to a vertex with an expression

todo:
    - name locator as vertex: locator_at_sphere_vtx123
    - name expression as vertex: expression_locator_at_sphere_vtx123
"""


import pymel.core


def constrain_loc_to_vtx():
    selection = pymel.core.selected(
            long=True,
            absoluteName=True,
            flatten=True,
            head=2,
        )
    vtx = selection.pop(0)
    mesh = pymel.core.PyNode(vtx).getParent()
    # mesh = pymel.core.PyNode(vtx).getParent().getTransform()
    locator = pymel.core.spaceLocator()
    locator = locator.rename('locator_vertexConstrained')
    expression = (
            """// Next line is old code. some attribute enquery\n"""
            """// should be put there what evaluates constantly\n"""
            """// so the expression refreshes on transforming\n"""
            """// the object and not only on frame change\n"""
            """float $BBoxSize = `getAttr {mesh}.boundingBoxMinX`;\n\n"""
            """$vertexWorldPos = `pointPosition -world {vtx}`;\n\n"""
            """setAttr {locator}.translateX $vertexWorldPos[0];\n"""
            """setAttr {locator}.translateY $vertexWorldPos[1];\n"""
            """setAttr {locator}.translateZ $vertexWorldPos[2];"""
        )
    expression = expression.format(mesh=mesh, vtx=str(vtx), locator=locator)
    pymel.core.expression(name=locator.name(), string=expression)


def test():
    import constrainLoc2vtx_tests
    reload(constrainLoc2vtx_tests)

    constrainLoc2vtx_tests.main()
