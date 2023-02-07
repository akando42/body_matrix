## Human Body Measurement via Video and Image
### Install the Package
```
$ pip install body-matrix
```

### Package Usage
#### Load Models, Video and Image Frames***

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

#### Infer
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


video, frame_counts, fps, sample_frame = load.video("04_01.mp4", -90, 1)
segment_model, segment_transform = load.segment_model("cpu")
keypoints_model, keypoints_transform = load.keypoints_model("cpu")

selected_box, keypoint = infer.detect_main_target(
	sample_frame, "cpu", 0.8, keypoints_model, keypoints_transform
)

mask, mask_image, bool_mask = infer.segment_selected_target(
	sample_frame, "cpu", selected_box, 0.99, segment_model, segment_transform
)
```

#### Filter
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
Segmentation_Contour
```
from body_matrix import load
from body_matrix import infer
from body_matrix import process

video, frame_counts, fps, sample_frame = load.video(
    "/content/drive/MyDrive/Body_Matrix/Raw_Vids/VID_20230102_171936~2.mp4", 
    -90, 
    2
)

keypoints_model, keypoints_transform = load.keypoints_model("cuda")
selected_box, keypoints = infer.detect_main_target(
    sample_frame, "cuda", 0.8, keypoints_model, keypoints_transform
)

selected_kps = process.keypoints_filter(
    ['nose','left_shoulder','right_shoulder'], 
    keypoints
)

segment_model, segment_transform = load.segment_model("cuda")
mask, mask_image, bool_mask = infer.segment_selected_target(
    sample_frame, "cuda", selected_box, 0.99, segment_model, segment_transform
)

segment_area = process.segmentation_area(
    sample_frame, 
    bool_mask
)

segment_contours = process.segmentation_contour(
    sample_frame, 
    bool_mask
)

```

Segmentation_Intersection - TO be DONE

Filter_Segmentation_Intersection - TO be DONE

#### Draw
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
    coordinates=selected_kps,
    image=sample_frame, 
    label_font="/path/Roboto-Bold.ttf"
)

output
```

Circle_Label
```
from body_matrix import draw

middle_back = (309.86787033081055, 699.3268127441406)
updated_sample = draw.circle_label(
    image=output, 
    central_point=middle_back,
    radius=100,
    background_color = "#FF0000", 
    label = "21", 
    label_size = 100,
    label_font="/path/Roboto-Bold.ttf", 
    label_color ="#FAFF00"
)
```

Rectangle_Label
```
from body_matrix import draw
from body_matrix import load

video, frame_counts, fps, sample_frame = load.video(
    "/Users/troydo42/Desktop/TorchVision/INFER_VIDS/Nov30/00_01.mp4", 
    -90, 
    30
)

rect_sample = draw.fixed_rectangle_label(
    image=sample_frame, 
    anchor_point=[sample_frame.width/2, 100], 
    label_text="Lottee Mart",
    label_size=30, 
    label_font="/Users/troydo42/Desktop/Body_Matrixes/Roboto-Bold.ttf", 
    label_color ="#FFFFFF",
    background_color = "#11114A"
)

rect_sample
```

Connecting_Line

```
from body_matrix import draw
from body_matrix import load

video, frame_counts, fps, sample_frame = load.video(
    "/Users/troydo42/Desktop/TorchVision/INFER_VIDS/Nov30/00_01.mp4", 
    -90, 
    30
)

keypoints_model, keypoints_transform = load.keypoints_model("cpu")
boxes, keypoints = infer.detect_main_target(
    sample_frame, "cpu", 0.8, keypoints_model, keypoints_transform
)

selected_kps = process.keypoints_filter(
    [
        'left_shoulder','right_shoulder',
        'left_hip','right_hip', 
        'left_wrist','right_wrist',
        'left_ankle', 'right_ankle'
    ], 
    keypoints
)

new_sample = draw.connecting_line(
    image=rect_sample, 
    pointA=selected_kps['right_shoulder'],
    pointB=selected_kps['left_hip'],
    line_color="white", 
    line_width=12
)

new_sample

```
Floating Label
```
from body_matrix import load
from body_matrix import measure 
from body_matrix import draw
from body_matrix import infer
from body_matrix import process

video, frame_counts, fps, sample_frame = load.video(
    "/Users/troydo42/Desktop/TorchVision/INFER_VIDS/Nov30/00_01.mp4", 
    -90, 
    30
)

keypoints_model, keypoints_transform = load.keypoints_model("cpu")
boxes, keypoints = infer.detect_main_target(
    sample_frame, "cpu", 0.8, keypoints_model, keypoints_transform
)

selected_kps = process.keypoints_filter(
    [
        'left_shoulder','right_shoulder',
        'left_hip','right_hip', 
        'left_wrist','right_wrist',
        'left_ankle', 'right_ankle'
    ], 
    keypoints
)

middle_hip = measure.find_middle_point(
    selected_kps['left_hip'], 
    selected_kps['right_hip']
)

middle_shoulder = measure.find_middle_point(
    selected_kps['left_shoulder'], 
    selected_kps['right_shoulder']
)

middle_back = measure.find_middle_point(
    middle_shoulder, 
    middle_hip
)

float_sample = sample_frame
for key, value in selected_kps.items():
    print(key, value)
    float_sample = draw.floating_rectangle_label(
        image=float_sample, 
        longitude_coordinate=middle_back[0],
        point=value, 
        label_text=key, 
        label_size=16, 
        label_color="#ffffff", 
        label_font="/Users/troydo42/Desktop/Body_Matrixes/Roboto-Bold.ttf",
        background_color="#11114A"
    )    

float_sample
```

Draw Segmentation_Contour 
```
from body_matrix import load
from body_matrix import infer
from body_matrix import process
from body_matrix import process
from body_matrix import draw

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

updated_contours = process.segmentation_contour(
    sample_frame, 
    bool_mask
)

contoured_image = draw.segmentation_contour(
    contour_pixels = updated_contours, 
    contour_color = "#ffffff",
    contour_size=2,
    font="/content/drive/MyDrive/Body_Matrix/Roboto-Bold.ttf", 
    image=sample_frame
)

contoured_image
```

#### Measure
Box_Center_Coordinate
```
from body_matrix import load
from body_matrix import infer
from body_matrix import measure 

video, frame_counts, fps, sample_frame = load.video(
    "/Users/troydo42/Desktop/Body_Matrixes/samples/man_03.mp4", 
    -90, 
    30
)

keypoints_model, keypoints_transform = load.keypoints_model("cpu")
box, keypoints = infer.detect_main_target(
    sample_frame, "cpu", 0.8, keypoints_model, keypoints_transform
)

box

center = measure.box_center_coordinate(box)
```

Two_Boxes_Distance
```
from body_matrix import load
from body_matrix import infer
from body_matrix import measure
from torchvision.transforms.functional import to_pil_image

sample_frame_index = 30
video, frame_counts, fps, sample_frame = load.video(
    "/path/sample01.mp4", 
    -90, 
    sample_frame_index
)

keypoints_model, keypoints_transform = load.keypoints_model("cpu")
box, keypoints = infer.detect_main_target(
    frame=sample_frame, 
    device="cpu",
    min_accuracy=0.8,
    kp_model=keypoints_model, 
    kp_transforms=keypoints_transform 
)

next_frame = to_pil_image(video[sample_frame_index+1])
next_frame = next_frame.rotate(-90, expand=True)
next_box, keypoints = infer.detect_main_target(
    frame=next_frame, 
    device="cpu",
    min_accuracy=0.8,
    kp_model=keypoints_model, 
    kp_transforms=keypoints_transform 
)

moved_distance = measure.two_boxes_distance(box, next_box)
moved_distance
```

Box_Distance_From_Vertical_Line
```
from body_matrix import load
from body_matrix import infer
from body_matrix import measure
from torchvision.transforms.functional import to_pil_image

sample_frame_index = 30
video, frame_counts, fps, sample_frame = load.video(
    "/path/sample01.mp4", 
    -90, 
    sample_frame_index
)

keypoints_model, keypoints_transform = load.keypoints_model("cpu")
box, keypoints = infer.detect_main_target(
    frame=sample_frame, 
    device="cpu",
    min_accuracy=0.8,
    kp_model=keypoints_model, 
    kp_transforms=keypoints_transform 
)

distance, area = measure.distance_from_vertical_line(
    pic=sample_frame, 
    bbox=box
)
```

Box_Distance_From_Center
```
from body_matrix import load
from body_matrix import infer
from body_matrix import measure

sample_frame_index = 10
video, frame_counts, fps, sample_frame = load.video(
    "/path/sample01.mp4", 
    -90, 
    sample_frame_index
)

keypoints_model, keypoints_transform = load.keypoints_model("cpu")

box, keypoints = infer.detect_main_target(
    sample_frame, 
    device="cpu", 
    min_accuracy=0.8, 
    kp_model=keypoints_model, 
    kp_transforms=keypoints_transform
)

distance, area = measure.box_distance_from_center(sample_frame, box)

```

Two_Points_Distance
```
from body_matrix import load
from body_matrix import infer
from body_matrix import measure

sample_frame_index = 10
video, frame_counts, fps, sample_frame = load.video(
    "/path/sample01.mp4", 
    -90, 
    sample_frame_index
)

keypoints_model, keypoints_transform = load.keypoints_model("cpu")

box, keypoints = infer.detect_main_target(
    sample_frame, 
    device="cpu", 
    min_accuracy=0.8, 
    kp_model=keypoints_model, 
    kp_transforms=keypoints_transform
)

distance = measure.two_points_distance(keypoints[0], keypoints[1])
distance

```

Find_Middle_Point
```
from body_matrix import load
from body_matrix import infer
from body_matrix import measure

sample_frame_index = 10
video, frame_counts, fps, sample_frame = load.video(
    "/path/sample01.mp4", 
    -90, 
    sample_frame_index
)

keypoints_model, keypoints_transform = load.keypoints_model("cpu")

box, keypoints = infer.detect_main_target(
    sample_frame, 
    device="cpu", 
    min_accuracy=0.8, 
    kp_model=keypoints_model, 
    kp_transforms=keypoints_transform
)

x, y = measure.find_middle_point(keypoints[0], keypoints[1])
print(x.item(), y.item())
```

Box_Distance_From_Horizontal_Line
```
from body_matrix import load
from body_matrix import infer
from body_matrix import measure

sample_frame_index = 10
video, frame_counts, fps, sample_frame = load.video(
    "/path/sample01.mp4", 
    -90, 
    sample_frame_index
)

keypoints_model, keypoints_transform = load.keypoints_model("cpu")

box, keypoints = infer.detect_main_target(
    sample_frame, 
    device="cpu", 
    min_accuracy=0.8, 
    kp_model=keypoints_model, 
    kp_transforms=keypoints_transform
)

distance = measure.distance_from_horizon_line(
    sample_frame, 
    box
)
distance
```

Find_Border_Length - TO be DONE
```
```

Find_Polygon_Area - TO be DONE
```
```

#### Score
Two_Points_Linear_Constants
```
from body_matrix import load
from body_matrix import infer
from body_matrix import process
from body_matrix import score

video, frame_counts, fps, sample_frame = load.video(
    "/Users/troydo42/Desktop/Body_Matrixes/samples/man_01.mp4", 
    90, 
    1
)

keypoints_model, keypoints_transform = load.keypoints_model("cpu")
selected_box, keypoints = infer.detect_main_target(
    sample_frame, "cpu", 0.8, keypoints_model, keypoints_transform
)
selected_kps = process.keypoints_filter(
    [ 'left_ankle', 'right_ankle'], 
    keypoints
)

la = selected_kps['left_ankle']
ra = selected_kps['right_ankle']

alpha, beta = score.two_points_linear_constant(la, ra)
print(alpha, beta)

```

Find_Segment_Line
```
from body_matrix import load
from body_matrix import infer
from body_matrix import process

video, frame_counts, fps, sample_frame = load.video(
    "/Users/troydo42/Desktop/Body_Matrixes/samples/man_01.mp4", 
    90, 
    1
)

keypoints_model, keypoints_transform = load.keypoints_model("cpu")
selected_box, keypoints = infer.detect_main_target(
    sample_frame, "cpu", 0.8, keypoints_model, keypoints_transform
)
selected_kps = process.keypoints_filter(
    [
        'left_shoulder','right_shoulder', 
        'left_hip', 'right_hip',  
        'left_elbow','right_elbow',
        'left_wrist', 'right_wrist',
        'left_ankle', 'right_ankle'], 
    keypoints
)

segment_model, segment_transform = load.segment_model("cpu")
mask, mask_image, bool_mask = infer.segment_selected_target(
    sample_frame, "cpu", selected_box, 0.9, segment_model, segment_transform
)

segment_area = process.segmentation_area(
    sample_frame, 
    bool_mask
)

ls = selected_kps['left_shoulder']
rs = selected_kps['right_shoulder']

alpha, beta = two_points_linear_constant(ls, rs)
shoulder_line_coordinates = find_segment_line(segment_area, alpha, beta)

```

SHA_Score
```
from body_matrix import score

shoulder_length = 239.0083680543424
hip_length = 222.02026934494066
back_length = 287.0339701150371
leg_length = 431.9036764558864

score = score.SHA_score(
    shoulder_length, 
    hip_length, 
    back_length, 
    leg_length
)
```


video_SHA_Scores
```
### Load Video
from body_matrix import load, score
video, frames_counts, fps, sample_frame = load.video(
    "/content/drive/MyDrive/Body_Matrix/Raw_Vids/VID_20230105_174258.mp4", 
    rotate_angle=-90, 
    frame_position=1
)
print(frames_counts)
sample_frame

### Load Keypoints Model
segment_model, segment_transform = load.segment_model("cuda")
keypoints_model, keypoints_transform = load.keypoints_model("cuda")

### Iterate Over Video Frame for SHA Score
SHA_frames, SHA_scores = score.video_SHA_score(
    vid=video,
    device="cuda", 
    font_dir="/content/drive/MyDrive/Body_Matrix/Roboto-Bold.ttf",
    segment_model=segment_model,
    segment_transform=segment_transform, 
    keypoints_model=keypoints_model, 
    keypoints_transform=keypoints_transform
)

index = int(len(SHA_scores)/2)
print(SHA_scores[index])
SHA_frames[index]

```

Find_Nearest_Value
```
```

Find_Largest_Value
```
```

Find_Best_Score
```
```

#### Export
Generate_Video_From_Images
```
from body_matrix import load, score, export

video, frames_counts, fps, sample_frame = load.video(
    "/content/drive/MyDrive/Body_Matrix/Raw_Vids/VID_20230109_114329~2.mp4", 
    rotate_angle=-90, 
    frame_position=1
)
print(frames_counts)
sample_frame

### Load Keypoints Model
segment_model, segment_transform = load.segment_model("cuda")
keypoints_model, keypoints_transform = load.keypoints_model("cuda")

### Iterate Over Video Frame for SHA Score
SHA_frames, SHA_scores = score.video_SHA_score(
    vid=video,
    device="cuda", 
    font_dir="/content/drive/MyDrive/Body_Matrix/Roboto-Bold.ttf",
    segment_model=segment_model,
    segment_transform=segment_transform, 
    keypoints_model=keypoints_model, 
    keypoints_transform=keypoints_transform
)

vid_width = sample_frame.width
vid_height = sample_frame.height
vid_output = "visualized.mp4"

export.generate_video_from_pil_images(
    pil_images=SHA_frames, 
    output=vid_output, 
    width=vid_width,
    height=vid_height
)
```

Generate_Seeking_Video_From_Images
```
```

Generate_Instagram_Video_From_Images
```
```

Generate_Youtube_Video_From_Images
```
```

