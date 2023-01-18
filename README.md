## Human Body Measurement via Video and Image
### Install the Package
```
$ pip install body-matrix
```

### Package Usage
***Load Models, Video and Image Frames***
Load Segmentation Model to CPU
```
from body_matrix import load
segmentation_model, segmentation_transforms = load.segmentation_model("cpu")
```

Load Segmentation Model to GPU
```
from body_matrix import load
segmentation_model, segmentation_transforms = load.segmentation_model("cuda")
```

Load Keypoints Model to CPU
```
from body_matrix import load
keypoints_model, keypoints_transforms = load.segmentation_model("cpu")
```

Load Keypoints Model to GPU
```
from body_matrix import load
keypoints_model, keypoints_transforms = load.segmentation_model("cuda")
```

Load Video
```
from body_matrix import load
video, frames_counts, fps, sample_frame = load.video("/Desktop/dt.mov", 90, 1)
print(frames_counts)
```

Load Image
```
from body_matrix import load
frames_path = load.image_frames("/Desktop/instagram")
print(frames_path)
```

***Infer***
Detect_Main_Target
```
from body_matrix import infer
from body_matrix import load

keypoints_model, keypoints_transform = load.keypoints_model("cpu")
video, frame_counts, fps, sample_frame = load.video("04_01.mp4", -90, 1)

selected_box, keypoint = infer.detect_main_target(
	sample_frame, "cpu", 0.8, keypoints_model, keypoints_transform
)
```

Segment_Selected_Target
```
from body_matrix import infer
from body_matrix import load

segment_model, segment_transform = load.segment_model("cpu")
video, frame_counts, fps, sample_frame = load.video("04_01.mp4", -90, 1)

selected_box, keypoint = infer.detect_main_target(
	sample_frame, "cpu", 0.8, keypoints_model, keypoints_transform
)

mask, mask_image, bool_mask = infer.segment_selected_target(
	sample_frame, "cpu", selected_box, 0.99, segment_model, segment_transform
)
```

***Filter***
Keypoints_Filter

```
from body_matrix import load
from body_matrix import infer
from body_matrix import process

video, frame_counts, fps, sample_frame = load.video(
	"sample02.mp4", 
	-90, 
	1
)

keypoints_model, keypoints_transform = load.keypoints_model("cpu")
boxes, keypoints = infer.detect_main_target(
	sample_frame, "cpu", 0.8, keypoints_model, keypoints_transform
)

selected_kps = process.keypoints_filter(
	['nose','left_shoulder','right_shoulder'], 
	keypoints
)

print(selected_kps[nose])

```
Human_Segmentation_Area

```
from body_matrix import load
from body_matrix import infer
from body_matrix import process

video, frame_counts, fps, sample_frame = load.video(
	"sample02.mp4", 
	-90, 
	1
)

keypoints_model, keypoints_transform = load.keypoints_model("cpu")
selected_box, keypoints = infer.detect_main_target(
	sample_frame, "cpu", 0.8, keypoints_model, keypoints_transform
)

selected_kps = process.keypoints_filter(
	['nose','left_shoulder','right_shoulder'], 
	keypoints
)

segment_model, segment_transform = load.segment_model("cpu")
mask, mask_image, bool_mask = infer.segment_selected_target(
	sample_frame, "cpu", selected_box, 0.99, segment_model, segment_transform
)

segment_area = process.segmentation_area(
	sample_frame, 
	bool_mask
)

```
Find_Segmentation_Intersection - TO be DONE
Find_Segmentation_Contour - TO be DONE
Filter_Segmentation_Intersection - TO be DONE

***Draw***
Keypoint_Markers
```
from body_matrix import load
from body_matrix import infer
from body_matrix import process
from body_matrix import draw

video, frame_counts, fps, sample_frame = load.video(
	"sample02.mp4", 
	-90, 
	1
)

keypoints_model, keypoints_transform = load.keypoints_model("cpu")
boxes, keypoints = infer.detect_main_target(
	sample_frame, "cpu", 0.8, keypoints_model, keypoints_transform
)

selected_kps = process.keypoints_filter(
	['nose','left_shoulder','right_shoulder'], 
	keypoints
)

output = draw.keypoint_markers(
	coordinate=selected_kps,
	image=sample_frame, 
	label_font="/Users/troydo42/Desktop/Body_Matrixes/Roboto-Bold.ttf"
)

output


```
Circle_Label
Rectangle_Label
Connecting_Line

***Measure***
Get_Box_Center_Coordinate
Two_Boxes_Distance
Box_Distance_From_Vertical_Line
Box_Distance_From_Horizontal_Line
Box_Distance_From_Center
Two_Points_Distance
Find_Middle_Point
Find_Border_Length - TO be DONE
Find_Polygon_Area - TO be DONE

***Score***
Find_Nearest_Value
Find_Largest_Value
Find_Best_Score

***Export***
Generate_Video_From_Images
Generate_Seeking_Video_From_Images
Generate_Instagram_Video_From_Images
Generate_Youtube_Video_From_Images
