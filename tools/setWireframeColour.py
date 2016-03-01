try:
    import pymel.core as pm
except:
    pm = None



def set_colour(name):
    codes = {'darkgreen': 0,
            'lightgrey': 3,
            'darkred': 4,
            'darkblue': 5,
            'lightblue': 6,
            'purple': 9,
            'brown': 10,
            'red': 13,
            'lightgreen': 14,
            'white': 16,
            'yellow': 17,
            'cyan': 18,
        }

    pm.ls(selection=1)

    for node in pm.ls(selection=1):
        node.overrideEnabled.set(1)
        node.overrideColor.set(codes[name])


def main(**kwargs):
    pass



if __name__ == '__main__':
    pass
