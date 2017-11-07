# **Finding Lane Lines on the Road** 

The goals / steps of this project are the following:
* Make a pipeline that finds lane lines on the road
* Reflect on your work in a written report

### 1. Pipeline

My general approach was to create a pipeline that will detect ALL lane lines on the image, that are in the region of interest. 
It is important for two cases:
1. On the road there is a temporary lane line for construction purposes. So, all: regular and temporary lane lines should be detected.
2. Lane lines should be correctly detected during line switch.

My pipeline consisted of following steps:
1. Read in an image.
2. Grayscale an image. 
3. Do Gaussain smoothing.
4. Do Canny transformation.
5. Apply mask with the region of interest.
6. Detect lines with Hough transform in the region of interest.
7. Create array of vectors that are oriented from bottom of the image to top of the image from lines.
8. Filter vectors by angle and length to remove horizontal lines and noise. Noise removal is also done on step 6, but I repeat it here to guarantee behaviour. Horizontal lines may describe lane lines on crosses, but are not interesting for this project.
9. Sort vectors by angle and length by their start points from bottom to top of the image. This step helps to detect curved lane lines.
10. Group vectors into similar groups by linear average. One group should describe one possible lane line (left or right). In fact it could be lines with noise, shadows and other. Amount of outcome groups could be more than 2.
11. Filter out groups that describes not a lane lines by length and fillrate of the lane line (see details in the notebook).
12. Calculate lane lines for each group with weighted average.
13. Print lane lines on the image. If lane line is closed to bottom, extrapolate to bottom of the image.
14. Output the image.

draw_lines function takes array of lane lines, extrapolates them to the bottom if they are closed to it and draws on an image.

Pipeline is well described in the notebook itself.

### 2. Potential shortcomings

1. Grayscaling could potentially kill important information. Grayscaling algorithm should be selected and tested very carefully. I use function from lectures, but because it is 256x256x256 -> 256 transformation it may happen that we loose some cases where we can see a line on coloured image, but do not see on a grayscale. 
2. Could be a lot, should be tested but amount of test videos

### 3. Possible improvements

1. Adjust parameters for better performance. Run job in parallel for all possible parameters on set of test videos to detect possible problems.
2. There are small dots between lane lines that helps to define the lane. I do not use them at all, but they could be useful. For example, sometimes pipeline does not extrapolate lane lines to the bottom because pipeline thinks they are too far from the bottom
3. Solve the challenge - I did not manage to detect all the yellow lane line in sunny area (only around 2-3 miters far from the car)