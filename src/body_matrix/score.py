import numpy as np

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


def find_nearest(array, value):
	np_scores = np.array(array)
	distance_array = np.abs(np_scores - value)
	idx = distance_array.argmin()
	return array[idx], idx


def find_farthest(array, value):
	np_scores = np.array(array)
	distance_array = np.abs(np_scores - value)
	idx = distance_array.argmax()
	return array[idx], idx


# def find_best_score(array, value):
# 	return score

# def SHA_score(SHA_keypoints):
# 	sL = measures[0]
# 	hL = measures[1]
# 	bL = measures[2]
# 	lL = measures[3]

# 	score = (hL * lL) / (sL * bL)
# 	hs_score = int(hL/sL*1000) 
# 	lb_score = int(lL/bL*1000)

# 	return int(score), hs_score, lb_score
