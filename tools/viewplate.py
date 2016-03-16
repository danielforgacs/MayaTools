"""
previews footage from the selected
imagePlane in djv_view
"""


import subprocess
import pymel.core as pm


def main():
    imgplane = pm.selected()[0]
    seq = imgplane.imageName.get()
    # seq = '/jobs/fsb/shots/jtj/jtj_0250/work/camera/task01/3De/exports/fsb_jtj_0250_delensed_plate_v001/djv_view fsb_jtj_0250_delensed_plate_v001.1001.jpg'
    # seq = 'djv_view /jobs/fsb/shots/jtj/jtj_0250/work/camera/task01/3De/exports/fsb_jtj_0250_delensed_plate_v004/fsb_jtj_0250_delensed_plate_v004.1001.jpg'
    # seq = '/jobs/fsb/shots/jtj/jtj_0250/work/camera/task01/3De/exports/fsb_jtj_0250_delensed_plate_v004/fsb_jtj_0250_delensed_plate_v004.1001.jpg'
    # subprocess.Popen('djv_view')
    subprocess.Popen(['djv_view', seq])


if __name__ == '__main__':
    main()