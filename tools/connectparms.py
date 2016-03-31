"""
connects selected nodes all
attributes to the node
with the same name and a prefix
"""


try:
    import pymel.core as pm
except:
    pm = None


DEBUG = True


def connect_parms(node, new_node):
    for parm in node.listAttr(connectable=True, keyable=True):
        parmname = parm.attrName(longName=True, includeNode=False)

        try:
            pm.connectAttr(parm, new_node.attr(parmname))
        except:
            pass


def connect_selection(prefix):
    selection = pm.ls(selection=True)

    if DEBUG:
        selection = [pm.PyNode(k) for k in ['pCube1']]

    for node in selection:
        new_node = pm.PyNode(prefix + node.name())

        connect_parms(node, new_node)


def main(**kwargs):
    prefix = kwargs.get('prefix', '')

    connect_selection(prefix)




if __name__ == '__main__':
    pass