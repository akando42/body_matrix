import numpy as np

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