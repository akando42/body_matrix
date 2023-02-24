## Human Body Measurement via Video and Image
### Install the Package
```
$ pip install body-matrix
```

### Package Usage

```

#### LOAD VIDEO, Keypoints and Segmentation Model

from body_matrix import load, infer, process, measure, draw, export

video_path = "/content/drive/MyDrive/Body_Matrix/Raw_Vids/vinmart_customers.mp4"
video_rotate = -90
device = "cuda"
font_path = "/content/drive/MyDrive/Body_Matrix/Roboto-Bold.ttf"

keypoints_model, keypoints_transform = load.keypoints_model(device)
segment_model, segment_transform = load.segment_model(device)

video, frame_counts, fps, sample_frame = load.video(
    video_path=video_path, 
    rotate_angle=video_rotate,
    frame_position=1
)

sample_frame


#### Measure and Visualize Every frame
from body_matrix import score
from torchvision.transforms.functional import to_pil_image

measure_frames = []
measures = []

for index, vid_frame in enumerate(video):
    frame = to_pil_image(vid_frame)
    frame = frame.rotate(video_rotate, expand=True)
    height, leg, hip, shoulder, markers = measure.find_real_measures(
        image_frame=frame,
        device=device,
        keypoints_model=keypoints_model,
        keypoints_transform=keypoints_transform,
        segment_model=segment_model,
        segment_transform=segment_transform
    )

    visualized_frame = draw.visualize_measures(
        height, leg, hip, shoulder, markers, 
        frame, font_path
    )

    measure_frames.append(visualized_frame)
    measures.append(height)


mean, median, minim, maxim = score.best_scores(
    measures,
    100, 
    200
)

best_score, frame_index = score.find_nearest(
    measures, 
    median
)

#### Export Instagram Video with Measures
export.generate_instagram_vid(
    vid_name="instameasures_vinmart_girl.mp4", 
    vid_width = sample_frame.width, 
    vid_height = sample_frame.height, 
    pil_images = measure_frames, 
    stop_index=frame_index, 
    fps=fps, 
    repeat_rate=2, 
    slow_motion_rate=1
)

```