import random
import pymel.core as pm


def key_translate_on_frange(node, fend):
    value = lambda x: ((random.random() * 2) - 1) * x
    max_ = 0.17

    for f in range(1, fend, 5):
        node.translateX.setKey(time=f, value=value(max_), respectKeyable=True)
        node.translateY.setKey(time=f, value=value(max_), respectKeyable=True)
        node.translateZ.setKey(time=f, value=value(max_), respectKeyable=True)


def key_rotate_on_frange(node, fend):
    value = lambda x: ((random.random() * 2) - 1) * x
    max_ = 35

    for f in range(1, fend, 5):
        node.rotateX.setKey(time=f, value=value(max_), respectKeyable=True)
        node.rotateY.setKey(time=f, value=value(max_), respectKeyable=True)
        node.rotateZ.setKey(time=f, value=value(max_), respectKeyable=True)


def main(**kwargs):
    sel = pm.selected()
    frange = kwargs.get('frange', 240)

    for node in sel:
        print '-- node: ', node
        key_translate_on_frange(node, frange)
        key_rotate_on_frange(node, frange)