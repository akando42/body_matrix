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
			    detected_kpoints[0][index][0].item(), 
			    detected_kpoints[0][index][1].item()
			] 
			# print(kp_positions[keypoint])

	return kp_positions

# Human_Segmentation_Positions
def segmentation_positions():

# Find_Segmentation_Intersection

# Filter_Segmentation_Intersection

# Find_Segmentation_Contour - TO be DONE