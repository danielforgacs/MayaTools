import pymel.core


class NodeWrapper(object):
    def __init__(self, node):
        self.node = pymel.core.PyNode(node)

    def __getattr__(self, attr):
        return self.node.getAttr(attr)

    def __setattr__(self, attr, value):
        super(NodeWrapper, self).__setattr__(attr, value)