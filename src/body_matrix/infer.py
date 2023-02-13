import torch
import numpy as np
from torchvision.utils import draw_segmentation_masks
from torchvision.transforms.functional import to_pil_image, pil_to_tensor
from . import measure
from . import score

##########################################################
### Detect all Humans in Frames with High Probability ####
##########################################################
def detect_targets(frame, device, min_accuracy, kp_model, kp_transforms):

    ### Make Predictions on Frame
    body_matrix = kp_transforms(frame)
    predictions = kp_model([body_matrix.to(device)])

    ### Extract Boxes, Scores and Keypoints from frame
    boxes = predictions[0]['boxes']
    keypoints = predictions[0]['keypoints']
    scores = predictions[0]['scores']

    ### Filter for the main Bounding Box and Keypoints
    idx = torch.where(scores > min_accuracy)
    main_boxes = torch.squeeze(boxes[idx], dim=0)

    return main_boxes

###################################
### Detect Main Person in Frame ###
###################################
def detect_main_target(frame, device, min_accuracy, kp_model, kp_transforms):   

    ### Make Predictions on Frame
    body_matrix = kp_transforms(frame)
    predictions = kp_model([body_matrix.to(device)])

    ### Extract Boxes, Scores and Keypoints from frame
    boxes = predictions[0]['boxes']
    keypoints = predictions[0]['keypoints']
    scores = predictions[0]['scores']
    
    ### Filter for the main Bounding Box and Keypoints
    idx = torch.where(scores > min_accuracy)
    main_boxes = torch.unsqueeze(boxes[idx], dim=1)
    index = 0
    min_area = 0
    max_distance = frame.width/2

    print("Found ", len(main_boxes), " person in the frame")

    distances = []
    areas = []
    focuses = []
    bboxes = []
    
    for selector, box in enumerate(main_boxes):
        bbox = [
            box[0][0].item(), 
            box[0][1].item(),
            box[0][2].item(),
            box[0][3].item()
        ]
        
        distance, area = measure.distance_from_vertical_line(frame, bbox) 
        
        focuses.append(area/distance)
        distances.append(distance)
        areas.append(area)
        bboxes.append(bbox)

    print("Distances: ",distances)
    print("Areas: ", areas)
    print("FOCUSES: ", focuses)

    distance_score, distance_index = score.find_nearest(distances, 0)
    focus_score, focus_index = score.find_largest(focuses, 0)
    
    print("Select keypoint index", focus_index)
    selected_bbox = bboxes[focus_index] 
    selected_keypoints = torch.squeeze(keypoints[idx][focus_index], dim=0)
    # SHApoints = getSHAPositions(kp)
    # labels = ["ls","rs","lw", "rw", "lh","rh","la","ra"]
    # points_image = drawMarkers(labels, SHApoints, frame)
    return selected_bbox, selected_keypoints

###############################################
### Segment Selected Person from Background ###
###############################################
def segment_selected_target(frame, device, selected_bbox, segment_min_accuracy, segment_model, segment_transforms):
    ### Run Predicion Model to find Mask
    input_image = segment_transforms(frame)
    predictions = segment_model([input_image.to(device)])
    masks = predictions[0]['masks']
    scores = predictions[0]['scores']
    boxes = predictions[0]['boxes']
    idx = torch.where(scores > segment_min_accuracy)
    main_boxes = torch.unsqueeze(boxes[idx], dim=1)

    print("Found ", len(main_boxes), " person in the frame")
    # index = len(main_boxes) - 1
    
    distances = []
    for selector, box in enumerate(main_boxes):
        bbox = [
            box[0][0].item(), 
            box[0][1].item(),
            box[0][2].item(),
            box[0][3].item()
        ]
        
        distance_from_selected = measure.two_boxes_distance(bbox, selected_bbox)
        distances.append(distance_from_selected)
            
    print(distances)
    distance, index = score.find_nearest(distances, 0)
    print(distance, index)
    
    mask = torch.squeeze(masks[index][0], dim=1)
    mask_image = to_pil_image(mask)
    
    ### Find the Minimum Pixel Threshold for Mask
    numpy_mask = mask.detach().cpu().numpy()
    counts, values = np.histogram(numpy_mask, bins=10)
    min_counts = np.min(counts)
    idx = np.where(counts == min_counts)
    thresholds = sorted(values[idx]) 
    numpy_bool_mask = numpy_mask > thresholds[0]
    bool_mask = torch.tensor(numpy_bool_mask)
    
    return mask, mask_image, bool_mask