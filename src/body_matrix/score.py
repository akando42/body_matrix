import numpy as np
import seaborn as sns
from torchvision.transforms.functional import to_pil_image
from . import load, infer, process, measure, draw

def two_points_linear_constant(a, b):
    aX = a[0]
    aY = a[1]
    bX = b[0]
    bY = b[1]
    if (bX-aX) != 0:
        alpha = (bY - aY)/(bX - aX)
        beta = (bX * aY - bY * aX)/(bX - aX)
    else:
        alpha = None
        beta = None
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
    measures = {
        'shoulder':sL,
        'hip':hL, 
        'back':bL,
        'leg':lL
    }

    return score, measures


def video_SHA_score(vid, device, font_dir,  segment_model, segment_transform, keypoints_model, keypoints_transform):
    SHA_frames = []
    SHA_scores = []
    SHA_measures = []
    
    for index, frame in enumerate(vid):
        image = to_pil_image(frame)
        image = image.rotate(-90, expand=True)
        selected_box, keypoints = infer.detect_main_target(
            image, device, 0.8, keypoints_model, keypoints_transform
        )

        mask, mask_image, bool_mask = infer.segment_selected_target(
            image, device, selected_box, 0.99, segment_model, segment_transform
        )

        selected_kps = process.keypoints_filter(
             [
                'left_ear', 'right_ear',
                'left_shoulder','right_shoulder',
                'left_wrist','right_wrist',
                'left_hip', 'right_hip',
                'left_ankle', 'right_ankle'
            ], 
            keypoints
        )
        
        segment_area = process.segmentation_area(
            image, 
            bool_mask
        )
        
        hip_kps = process.find_hip_points(
            selected_kps['left_hip'], 
            selected_kps['right_hip'],
            selected_kps['left_wrist'],
            selected_kps['right_wrist'],
            segment_area
        )
        
        shoulder_kps = process.find_shoulder_points(
            selected_kps['left_shoulder'], 
            selected_kps['right_shoulder'],
            segment_area
        )

        if hip_kps == None or shoulder_kps == None:
            print("KEYPOINT ERRORS")
            continue
        
        main_points = {}
        main_points.update(hip_kps)
        main_points.update(shoulder_kps)
        main_points.update(
            {
                'left_ankle':selected_kps['left_ankle'],
                'right_ankle':selected_kps['right_ankle']
            }
        )
        
        middle_hip = measure.find_middle_point(
            main_points['left_hip'],
            main_points['right_hip']
        )

        float_labeled_frame = image
        for key, value in main_points.items():
            print(key, value)
            float_labeled_frame = draw.floating_rectangle_label(
                image = float_labeled_frame, 
                longitude_coordinate = middle_hip[0], 
                point=value, 
                label_text=key, 
                label_size=16, 
                label_color="#ffffff", 
                label_font=font_dir, 
                background_color="#11114A"
            )    

       
        score, measures = SHA_score(
            ls=main_points['left_shoulder'], 
            rs=main_points['right_shoulder'],
            lh=main_points['left_hip'],
            rh=main_points['right_hip'],
            la=main_points['left_ankle'],
            ra=main_points['right_ankle']
        )
        
        SHA_frames.append(float_labeled_frame)

        SHA_scores.append(score)
        SHA_measures.append(measures)

        print("##############################")
        print("Finished Processing ", index, " with score ", score, "\nand measures ", measures)
        print("##############################")
        
    return SHA_frames, SHA_scores, SHA_measures


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


def best_scores(array, min_val, max_val):
    scores = []
    for x in array:
        if x > max_val or x <  min_val:
            pass
        else:
            scores.append(x)
            
    np_scores = np.array(scores)
    mean = np.mean(np_scores)
    median = np.median(np_scores)
    minim = np.min(np_scores)
    maxim = np.max(np_scores)
    histogram_scores = np.histogram(np_scores)
    print(mean, median)
    sns.distplot(np_scores, hist=True)
    
    return mean, median, minim, maxim




