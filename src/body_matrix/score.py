import numpy as np

# def calculate_SHA_score(SHA_keypoints):
# 	sL = measures[0]
# 	hL = measures[1]
# 	bL = measures[2]
# 	lL = measures[3]

# 	score = (hL * lL) / (sL * bL)
# 	hs_score = int(hL/sL*1000) 
# 	lb_score = int(lL/bL*1000)

# 	return int(score), hs_score, lb_score

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

def find_best_score(array, value):

	return score

