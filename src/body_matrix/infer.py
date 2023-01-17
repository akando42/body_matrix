import torch
import numpy as np
from torchvision.utils import draw_segmentation_masks
from torchvision.transforms.functional import to_pil_image, pil_to_tensor

### Detect Main Person in Frame
def detect_main_target(frame, kp_model, kp_transforms):
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

    for selector, box in enumerate(main_boxes):
        bbox = [
            box[0][0].item(), 
            box[0][1].item(),
            box[0][2].item(),
            box[0][3].item()
        ]
        
        distance, area = dfc(frame, bbox) 
        if distance < max_distance and area > min_area:
            min_area = area
            index = selector
            print(
                "Selected person "+ str(selector) 
                +" with area " + str(min_area) 
                + " and dfc " + str(distance)
            )
        else:
            print("Not selected", min_area, selector, distance)
      
    bx = torch.unsqueeze(boxes[idx][index], dim=0)
    kp = torch.unsqueeze(keypoints[idx][index], dim=0)
    
    # SHApoints = getSHAPositions(kp)
    # labels = ["ls","rs","lw", "rw", "lh","rh","la","ra"]
    # points_image = drawMarkers(labels, SHApoints, frame)

    return bx, kp

### Segment Selected Person from Background
def segment_selected_target(frame, selected_bbox):
    ### Run Predicion Model to find Mask
    input_image = segment_transforms(frame)
    predictions = segment_model([input_image.to(device)])
    masks = predictions[0]['masks']
    scores = predictions[0]['scores']
    boxes = predictions[0]['boxes']
    idx = torch.where(scores > segmentation_min_accuracy)
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
        
        distance_from_selected = dtb(bbox, selected_bbox)
        #print(distance_from_selected)
        
        distances.append(distance_from_selected)
            
    print(distances)
    distance, index = find_nearest(distances, 0)
    print(distance, index)
    
    mask = torch.squeeze(masks[index][0], dim=1)
    mask_image = to_pil_image(mask)
    
    ### Find the Minimum Pixel Threshold for Mask
    numpy_mask = mask.detach().cpu().numpy()
    counts, values = np.histogram(numpy_mask, bins=10)
    min_counts = np.min(counts)
    idx = np.where(counts == min_counts)
    threshold = values[idx] 
    numpy_bool_mask = numpy_mask > threshold
    bool_mask = torch.tensor(numpy_bool_mask)
    
    return mask, mask_image, bool_mask