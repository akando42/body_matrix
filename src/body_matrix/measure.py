import math
from . import infer, process

### Get_Box_Center_Coordinate
def box_center_coordinate(bbox):
    center_x = (bbox[2] + bbox[0])/2
    center_y = (bbox[3] + bbox[1])/2
    center = [center_x, center_y]
    return center


### Two_Boxes_Distance
def two_boxes_distance(bbox1, bbox2):
    print(bbox1)
    print(bbox2)
    bbox1_center = box_center_coordinate(bbox1)
    bbox2_center = box_center_coordinate(bbox2)
    x_dif = bbox1_center[0] - bbox2_center[0]
    y_dif = bbox1_center[1] - bbox2_center[1]
    
    distance = math.sqrt(x_dif * x_dif + y_dif * y_dif)
    return distance

### Box_Distance_From_Vertical_Line
def distance_from_vertical_line(pic, bbox):
    pic_width = pic.width
    pic_height = pic.height
    pic_center = box_center_coordinate([0,0, pic_width, pic_height])
    bbox_center = box_center_coordinate(bbox)
    dfv = abs(bbox_center[0] - pic_center[0])
    x_dif = bbox_center[0] - pic_center[0]
    y_dif = bbox_center[1] - pic_center[1]
    bbox_width = bbox[2] - bbox[0]
    bbox_height = bbox[3] - bbox[1] 
    distance = math.sqrt(x_dif * x_dif + y_dif * y_dif)
    area = abs(bbox_width * bbox_height)
    return dfv, area


### Box_Distance_From_Horizontal_Line
def distance_from_horizon_line(pic, bbox):
    pic_width = pic.width
    pic_height = pic.height
    pic_center = box_center_coordinate([0,0, pic_width, pic_height])
    bbox_center = box_center_coordinate(bbox)
    dfh = abs(bbox_center[1] - pic_center[1])

    x_dif = bbox_center[0] - pic_center[0]
    y_dif = bbox_center[1] - pic_center[1]
    bbox_width = bbox[2] - bbox[0]
    bbox_height = bbox[3] - bbox[1] 
    distance = math.sqrt(x_dif * x_dif + y_dif * y_dif)
    area = abs(bbox_width * bbox_height)
    return dfh, area


### Box_Distance_From_Center
def box_distance_from_center(pic, bbox):
    pic_width = pic.width
    pic_height = pic.height
    
    pic_center = box_center_coordinate([0,0, pic_width, pic_height])
    bbox_center = box_center_coordinate(bbox)
    
    x_dif = bbox_center[0] - pic_center[0]
    y_dif = bbox_center[1] - pic_center[1]
    bbox_width = bbox[2] - bbox[0]
    bbox_height = bbox[3] - bbox[1] 
    distance = math.sqrt(x_dif * x_dif + y_dif * y_dif)
    area = abs(bbox_width * bbox_height)
    return distance, area


### Two_Points_Distance
def two_points_distance(pointA, pointB):
    x_dif = (pointA[0] - pointB[0])
    y_dif = (pointA[1] - pointB[1])
    dif = math.sqrt(x_dif * x_dif + y_dif * y_dif)
    return dif


### Find_Middle_Point
def find_middle_point(pointA, pointB):
    middleX = (pointA[0] + pointB[0])/2
    middleY = (pointA[1] + pointB[1])/2
    return middleX, middleY 


### Find Body Measures
def find_real_measures(image_frame, device, keypoints_model, keypoints_transform, segment_model, segment_transform):
    selected_box, keypoints = infer.detect_main_target(
        image_frame, device, 0.8, keypoints_model, keypoints_transform
    )

    mask, mask_image, bool_mask = infer.segment_selected_target(
        image_frame, device, selected_box, 0.99, segment_model, segment_transform
    )

    selected_kps = process.keypoints_filter(
        [
            'left_eye', 'right_eye',
            'left_ear', 'right_ear',
            'left_shoulder','right_shoulder',
            'left_wrist','right_wrist',
            'left_hip', 'right_hip',
            'left_ankle', 'right_ankle'
        ],  
        keypoints
    )
    
    segment_area = process.segmentation_area(
        image_frame, 
        bool_mask
    )
    
    shoulder_point = process.find_shoulder_points(
        selected_kps['left_shoulder'],
        selected_kps['right_shoulder'],
        segment_area
    )
    
    ac_shoulder_line = two_points_distance(
        shoulder_point['left_shoulder'],
        shoulder_point['right_shoulder']
    )
    
    hip_kps = process.find_hip_points(
        selected_kps['left_hip'], 
        selected_kps['right_hip'],
        selected_kps['left_wrist'],
        selected_kps['right_wrist'],
        segment_area
    )
    
    middle_ear = find_middle_point(
        selected_kps['left_ear'], 
        selected_kps['right_ear']
    )

    middle_hip = find_middle_point(
        selected_kps['left_hip'],
        selected_kps['right_hip']
    )

    hip_line = two_points_distance(
        hip_kps['left_hip'],
        hip_kps['right_hip']
    )

    ear_line = two_points_distance(
        selected_kps['left_ear'], 
        selected_kps['right_ear']
    )

    middle_shoulder = find_middle_point(
        selected_kps['left_shoulder'], 
        selected_kps['right_shoulder']
    )

    shoulder_line = two_points_distance(
        selected_kps['left_shoulder'], 
        selected_kps['right_shoulder']
    )

    middle_ear_shoulder = two_points_distance(
        middle_ear, 
        middle_shoulder
    )

    middle_shoulder_line = two_points_distance(
        selected_kps['left_shoulder'],
        selected_kps['right_shoulder']
    )

    chin_point = (
        middle_ear[0],
        middle_ear[1] + middle_ear_shoulder * ear_line /(ear_line + shoulder_line)
    )
    
    segment_contours = process.segmentation_contour(
        image_frame, 
        bool_mask
    )

    top_head = process.find_tophead_point(
        selected_kps['left_ear'],
        selected_kps['right_ear'],
        segment_contours
    )

    middle_ankle = find_middle_point(
        selected_kps['left_ankle'],
        selected_kps['right_ankle']
    )
    
    head_height = two_points_distance(
        top_head, chin_point
    )

    body_height = two_points_distance(
        top_head, middle_ankle
    )

    leg_height = two_points_distance(
        middle_hip, middle_ankle
    )
    
    real_height = 22 * body_height/head_height
    real_legline = 22 * leg_height/head_height
    real_hipline = 22 * hip_line/head_height
    real_shoulderline = 22 * ac_shoulder_line/head_height
    
    markers = {
        'top_head': top_head,
        'chin':chin_point, 
        'left_shoulder': shoulder_point['left_shoulder'],
        'right_shoulder': shoulder_point['right_shoulder'],
        'left_hip':hip_kps['left_hip'],
        'right_hip':hip_kps['right_hip'],
        'left_ankle':selected_kps['left_ankle'],
        'right_ankle':selected_kps['right_ankle'],
        'central':middle_ankle
    }
    
    return real_height, real_legline, real_hipline, real_shoulderline, markers, selected_kps
