import math

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
