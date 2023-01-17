import torch

def detect_main_target(frame, kp_transforms, kp_model):
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