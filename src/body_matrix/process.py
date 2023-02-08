import torch
from PIL import ImageColor
from torchvision.transforms.functional import pil_to_tensor, to_pil_image
from . import score
from . import measure

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
	print(x, y)
	positions = []
	for x, y in zip(y, x):
		positions.append([x.item(), y.item(), x.item()*y.item()])

	return positions


# Human Segmentation Contour
def segmentation_contour(sample_image, bool_mask):
	tensor_image = pil_to_tensor(sample_image)
	mask = torch.squeeze(bool_mask, 0)
	img_to_draw = tensor_image.detach().clone()
	color = ImageColor.getrgb('blue')
	tensor_color = torch.tensor(color, dtype=torch.uint8)
	img_to_draw[:, mask] = tensor_color[:, None]
	colored = to_pil_image(img_to_draw)
	x, y = torch.where(
		(img_to_draw[2] == 255)
		&(img_to_draw[0] == 0)
		&(img_to_draw[1] == 0)
	)

	def check_if_contours(point, colored):
		[x, y] = point[0].item(), point[1].item()
		surrounding_pixels = [
			(x-1, y-1),(x, y-1),(x+1, y-1),
			(x-1, y), (x+1, y),
			(x-1, y+1), (x, y+1), (x+1, y+1)
		]
		checked = 0
		
		for pixel in surrounding_pixels:
			color = colored.getpixel(pixel)
			if color != (0, 0, 255):
				checked = checked + 1
				
		return checked

	contours = []
	for x, y in zip(y, x):
		result = check_if_contours(
			(x, y), 
			colored
		)
		
		if result != 0:
			contours.append([x.item(), y.item()])

	return contours


# Find Shoulder Points
def find_shoulder_points(ls, rs, segment_area):
	shoulder_alpha, shoulder_beta = score.two_points_linear_constant(ls, rs)

	if shoulder_alpha == None or shoulder_beta == None:
		return None

	shoulder_lines = score.find_segment_line(
	    segment_area, 
	    shoulder_alpha, 
	    shoulder_beta
	)

	if ls[0] < rs[0]:
		shoulder_kps = {
			'left_shoulder': shoulder_lines[0],
			'right_shoulder': shoulder_lines[-1]
		}
	elif ls[0] > rs[0]:
		shoulder_kps = {
			'left_shoulder': shoulder_lines[-1],
			'right_shoulder': shoulder_lines[0]
		}
	return shoulder_kps


# Find Hip Points with Hip Line Coordinate
def find_hip_points_HLC(lh, rh, lw, rw, segment_area):
	hip_alpha, hip_beta = score.two_points_linear_constant(lh, rh)

	if hip_alpha == None or hip_beta == None:
		return None

	hip_line_coordinates = score.find_segment_line(
		segment_area, 
		hip_alpha, 
		hip_beta
	)

	middle_hip = measure.find_middle_point(lh, rh)

	if rw[1] < rh[1] and lw[1] < lh[1]:
		hip_kps = {
			'left_hip': hip_line_coordinates[0],
			'right_hip': hip_line_coordinates[-1]
		}

		print(
			"both hand high", hip_kps,
			"\nLeft: ", lw, lh, 
			"\nRight: ", rw, rh
		)
		return hip_kps

	elif rw[1] > rh[1] and lw[1] > lh[1]:
		hip_kps = {}
		print(
			"both hand low", hip_kps,
			"\nLeft hand: ", lw[1], lh[1], 
			"\nRight: ", rw[1], rh[1]
		)

	elif int(lw[1]) >= int(lw[0] * hip_alpha + hip_beta)*0.9:
		precise_rh = hip_line_coordinates[-1]
		precise_lhX = 2 * middle_hip[0] - rh[0]
		precise_lhY = hip_alpha * precise_lhX + hip_beta
		precise_lh = [int(precise_lhX), int(precise_lhY)]
		hip_kps = {
			'left_hip': precise_lh,
			'right_hip': precise_rh
		}
		print(
			"low left hand", hip_kps, 
			"\n Left Wrist", lw,
			"\n Left Hip: ", lh)
		return hip_kps
		
		
	elif int(rw[1]) >= int(rw[0] * hip_alpha + hip_beta)*0.9:
		precise_lh = hip_line_coordinates[0]
		precise_rhX = 2 * middle_hip[0] - precise_lh[0]
		precise_rhY = hip_alpha * precise_rhX + hip_beta
		precise_rh = [int(precise_rhX), int(precise_rhY)] 
		
		hip_kps = {
			'left_hip': precise_lh,
			'right_hip': precise_rh
		}
		print(
			"low right hand", hip_kps,
			"\n Right Wrist: ", rw,
			"\n Right Hip: ", rh
		)
		return hip_kps


# Find Hip Points with Segmentation Area
def find_hip_points(lh, rh, lw, rw, segment_area):
	lhX = lh[0]
	lhY = lh[1]

	rhX = rh[0]
	rhY = rh[1]

	hip_alpha, hip_beta = score.two_points_linear_constant(lh, rh)

	if hip_alpha == None or hip_beta == None:
		return None

	hip_line_coordinates = score.find_segment_line(
		segment_area, 
		hip_alpha, 
		hip_beta
	)

	middle_hip = measure.find_middle_point(lh, rh)
	lThreshold = middle_hip[0] - measure.two_points_distance(
		measure.find_middle_point(lh, rh), lh
	) * 1.8

	rThreshold = middle_hip[0] + measure.two_points_distance(
		measure.find_middle_point(lh, rh), rh
	) * 1.8

	for idx, position in enumerate(segment_area):
		expectedY = hip_alpha * position[0] + hip_beta

		if int(position[1]) == int(expectedY) and position[0] > lThreshold and position[0] < middle_hip[0]:
			lhY = position[1]

			if position[0] < lhX:
				lhX = position[0]

		elif int(position[1]) == int(expectedY) and position[0] < rThreshold and position[0] > middle_hip[0]:
			rhY = position[1]
			if position[0] > rhX:
				rhX = position[0]

	if lh[0] < rh[0]:
		hip_kps = {
			'left_hip': (lhX, lhY), 
			'right_hip': (rhX, rhY)
		}

		return hip_kps

	elif  lh[0] > rh[0]:
		hip_kps = {
			'left_hip': (rhX, rhY), 
			'right_hip': (lhX, lhY)
		}
		return hip_kps
		

# Find Top Head Points
def find_tophead_point(le, re, ls, rs, segment_positions):

	return tophead_pt

