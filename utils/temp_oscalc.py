#! Python

from fractions import Fraction

# original plate resolution
res_x_plate = 2048
res_y_plate = 1152

# overscan in pixels on one side
# SET THIS TO CHANGE OVERSCAN:
overscan_px_top = 50

res_y_overscan = res_y_plate + (2 * overscan_px_top)
overscan_scale = Fraction(res_y_overscan, res_y_plate)
post_scale = Fraction(res_y_plate, res_y_overscan)
post_scale_b = 1 / overscan_scale
res_x_overscan = float(res_x_plate / post_scale)
res_x_overscan_rounded = int(round(res_x_overscan))
difference_x = res_x_overscan - res_x_plate
difference_y = res_y_overscan - res_y_plate

print 'plate resolution: ', res_x_plate, 'x', res_y_plate
print 'overscan resolution: ', res_x_overscan, 'x', res_y_overscan
print 'overscan resolution(rounded): ', res_x_overscan_rounded, 'x', res_y_overscan
print 'resolution difference: ', difference_x, 'x', difference_y
print 'overscan scale: ', float(overscan_scale)
print 'post scale: ', float(post_scale)
print 'post scale (different calc method): ', float(post_scale_b)
