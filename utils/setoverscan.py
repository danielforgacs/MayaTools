"""
calculate and set camera values
for overscan in one camera setup
"""


def set_camera_post_scale(ratio):
    postscale = None

    return postscale


def set_overscan(pixels=20):
    pass


def test():
    import setoverscan_tests

    try:
        reload(setoverscan_tests)
    except:
        import importlib

        importlib.reload(setoverscan_tests)

    setoverscan_tests.main()
