# README
## Language used
* python2.7

## Libraries used:
* numpy, openCV

## How to run the code :-
* python main.py

## Input : 
Input images is provided in “data/” folder in same directory. And the ground truth size/length of object(pen) is taken as label in file name.
### E.g :- 
Images named “image1_14_500.jpg”  “image2_14_500.jpg”, “image3_15_233.jpg” have actual length as 14.500 cm, 14.500 cm and 15.233 cm
respectively.

### Output :
Size of the object is given as output.

## Technique used :
* Before taking the input images , we first find out the intrinsic matrix for the camera. Intrinsic matrix is 3 by 3 matrix by camera calibration.
* After getting the intrinsic matrix, we use for undistortion of the input images.
* We use a known size paper(21.0 x 29.7cm(A4)) as background on which object(to be measured) is placed. This paper also provides good background for object segmentation. Since the paper and object are very close to each other, thus the error due to depth difference can be neglected. We use the dimension of paper as the ground truth of scale and in turn, it also remove the problem of the scaling due to varying position of camera.
* For segmentation, we use canny edge detector and then use corner detection for finding out the corners.
* First the corners of the paper is found, and then it is rescaled to given size using homography matrix.
* Now in the region of interest, we again find corners of the object.
* Among the corners, the furthest corners around the object is taken as the endpoints of the object and used to determine length of the object.
