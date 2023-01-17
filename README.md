## Human Body Measurement via Video and Image
### Install Package
```
$ pip install body-matrix

```

### Package Usage
Load Segmentation Model

```
from body_matrix import load
segmentation_model, segmentation_transforms = load.segmentation_model("cpu")
```

Load Keypoints Model
```
from body_matrix import load
keypoints_model, keypoints_transforms = load.segmentation_model("cpu")

```


Load Video
```
from body_matrix import load
video, frames_counts, fps, smaple_frame = load.video("/Users/troydo42/Desktop/dt.mov", 90, 1)
print(frames_counts)
```


Load Image
```
from body_matrix import load
frames_path = load.image_frames("/Users/troydo42/Desktop/instagram")
print(frames_path)

```
