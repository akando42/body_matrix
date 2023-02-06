import numpy as np
from . import measure

def two_points_linear_constant(a, b):
    aX = a[0]
    aY = a[1]
    bX = b[0]
    bY = b[1]
    alpha = (bY - aY)/(bX - aX)
    beta = (bX * aY - bY * aX)/(bX - aX)
    return alpha, beta


def find_segment_line(segment_area, alpha, beta):
    line_coordinates = []
    for idx, position in enumerate(sorted(segment_area)):
        expectedY = alpha * position[0] + beta
        if position[1] == int(expectedY):
            line_coordinates.append(
                [position[0], position[1]]
            )
    return line_coordinates


def SHA_score(ls, rs, lh, rh, la, ra):
    sL = measure.two_points_distance(ls, rs)
    hL = measure.two_points_distance(lh, rh)
    ms = measure.find_middle_point(ls, rs)
    mh = measure.find_middle_point(lh, rh)
    ma = measure.find_middle_point(la, ra)
    bL = measure.two_points_distance(ms, mh)
    lL = measure.two_points_distance(mh, ma)
    score = int((hL * lL) / (sL * bL) * 1000)
    # hs_score = int(hL/sL*1000) 
    # lb_score = int(lL/bL*1000)
    return score


def find_nearest(array, value):
	np_scores = np.array(array)
	distance_array = np.abs(np_scores - value)
	idx = distance_array.argmin()
	return array[idx], idx


def find_largest(array, value):
	np_scores = np.array(array)
	distance_array = np.abs(np_scores - value)
	idx = distance_array.argmax()
	return array[idx], idx




