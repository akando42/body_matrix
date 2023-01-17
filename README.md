## Human Body Measurement via Video and Image
### Install Package
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
video, frames_counts, fps, smaple_frame = load.video("/Users/troydo42/Desktop/dt.mov", 90, 1)
print(frames_counts)
```

Load Image
```
from body_matrix import load
frames_path = load.image_frames("/Users/troydo42/Desktop/instagram")
print(frames_path)
```

***Infer***
Detect_Human_Keypoints - TO be DONE
Segment_Human_Body - TO be DONE
Detect_Main_Target
Segment_Selected_Target


***Filter***
Keypoints_Filter
Human_Segmentation_Positions
Find_Segmentation_Intersection
Find_Segmentation_Contour - TO be DONE
Filter_Segmentation_Intersection

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

***Visualize***
Draw_Keypoint_Markers
Draw_Circle_Label
Draw_Rectangle_Label
Draw_Connecting_Line

***Score***
Find_Nearest_Value
Find_Largest_Value
Find_Best_Score

***Export***
Generate_Video_From_Images
Generate_Seeking_Video_From_Images
Generate_Instagram_Video_From_Images
Generate_Youtube_Video_From_Images
