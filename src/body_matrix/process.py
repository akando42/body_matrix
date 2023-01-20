import torch
from PIL import ImageColor
from torchvision.transforms.functional import pil_to_tensor

# Keypoints_Filter
def keypoints_filter(selected_kpoints, detected_kpoints):
	kp_positions = {}
	coco_keypoints = [
		"nose", "left_eye", "right_eye", "left_ear", "right_ear",
		"left_shoulder", "right_shoulder", "left_elbow", "right_elbow",
		"left_wrist", "right_wrist", "left_hip", "right_hip",
		"left_knee", "right_knee", "left_ankle", "right_ankle",
	]

	for index, keypoint in enumerate(coco_keypoints):
		if keypoint in selected_kpoints:
			kp_positions[keypoint] = [
				detected_kpoints[index][0].item(), 
				detected_kpoints[index][1].item()
			] 
			# print(kp_positions[keypoint])

	return kp_positions

# Human Segmentation Area
def segmentation_area(sample_image, bool_mask):
	tensor_image = pil_to_tensor(sample_image)
	mask = torch.squeeze(bool_mask, 0)
	img_to_draw = tensor_image.detach().clone()
	color = ImageColor.getrgb('blue')
	tensor_color = torch.tensor(color, dtype=torch.uint8)
	img_to_draw[:, mask] = tensor_color[:, None]
	x, y = torch.where(
		(img_to_draw[2] == 255)
		&(img_to_draw[0] == 0)
		&(img_to_draw[1] == 0)
	)
	positions = []
	for x, y in zip(y, x):
		positions.append([x.item(), y.item(), x.item()*y.item()])

	return positions


# Find Shoulder Points
def find_shoulder_points(ls, rs, segment_positions):
	lsX = ls[0]
	lsY = ls[1]
	rsX = rs[0]
	rsY = rs[1]
	
	alpha = (rsY - lsY)/(rsX - lsX)
	beta = (rsX * lsY - rsY * lsX)/(rsX - lsX)

	line_coordinates = []
	for idx, position in enumerate(segment_positions):
		expectedY = alpha * position[0] + beta
		if position[1] == expectedY:
			line_coordinates.append(
				[position[0], position[1]]
			)

	if lsX < rsX:
	    shoulder_kps = {
	        'left_shoulder': line_coordinates[0],
	        'right_shoulder': line_coordinates[-1]
	    }
	elif lsX > rsX:
	    shoulder_kps = {
	        'left_shoulder': line_coordinates[-1],
	        'right_shoulder': line_coordinates[0]
	    }
	return shoulder_kps


def find_hip_points(lh, rh, lw, rw, segment_positions):
	return lefthip_pt, righthip_pt

def find_tophead_point(le, re, ls, rs, segment_positions):
	return tophead_pt

# Find_Segmentation_Contour 

