"""
bake selected object
to world space
"""


try:
    import pymel.core as pm
except:
    pm = None


def main():
    source = pm.selectedNodes()[0]
    sourcenode = pm.PyNode(source)
    bakednode = sourcenode.duplicate()[0]
    pm.parent(bakednode, world=True)
    constraint = pm.parentConstraint(sourcenode, bakednode)
    pm.bakeResults(bakednode, t=(1, 120))
    pm.delete(constraint)
    bakednode.scaleX.set(1)
    bakednode.scaleY.set(1)
    bakednode.scaleZ.set(1)