import os
import av 

from torchvision.models.detection import MaskRCNN_ResNet50_FPN_V2_Weights, maskrcnn_resnet50_fpn_v2
from torchvision.models.detection import keypointrcnn_resnet50_fpn, KeypointRCNN_ResNet50_FPN_Weights
from torchvision.io import read_video
from torchvision.transforms.functional import to_pil_image

### Load Human Segmentation Model
def segment_model(device):
	segment_weights = MaskRCNN_ResNet50_FPN_V2_Weights.COCO_V1
	segment_model = maskrcnn_resnet50_fpn_v2(weights=segment_weights)
	segment_transforms = segment_weights.transforms()
	segment_model.eval().to(device)
	return segment_model, segment_transforms


### Load Keypoints Detection Model
def keypoints_model(device):
	kp_weights = KeypointRCNN_ResNet50_FPN_Weights.COCO_V1
	kp_model =  keypointrcnn_resnet50_fpn(weights=kp_weights)
	kp_transforms = kp_weights.transforms()
	kp_model.eval().to(device)
	return kp_model, kp_transforms


### Load Video 
def video(video_path, rotate_angle, frame_position):
	video, audio, meta = read_video(
	    video_path,
	    pts_unit="sec",
	    output_format="TCHW"
	)

	frame_counts = len(video)
	fps = meta['video_fps']
	sample_index = frame_position
	sample_frame = to_pil_image(video[sample_index])
	sample_frame = sample_frame.rotate(rotate_angle, expand=True)
	return video, frame_counts, fps, sample_frame


### Load Images Directory
def image_frames(sample_dir):
	frames = sorted(os.listdir(sample_dir))
	total_frames = len(frames)
	#print("\nTotal Frames: ",total_frames)
	frames_path = ["" for x in range(total_frames)]
	#print("\nTotal Paths: ",len(frames_path))
	for frame_index, frame in enumerate(frames):     
		frames_path[frame_index] = os.path.join(sample_dir + "/" + frame)  
	return frames_path