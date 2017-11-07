# **Finding Lane Lines on the Road** 

The goals / steps of this project are the following:
* Make a pipeline that finds lane lines on the road
* Reflect on your work in a written report

### 1. Pipeline

My general approach was to create a pipeline that will detect ALL lane lines on the image, that are in the region of interest. 
It is important at least for the following scenarious:
1. On the road there is a temporary lane line for construction purposes. So, all: regular and temporary lane lines should be detected.
2. Lane lines should be correctly detected during line switch.
3. Bike lane lines should be detected

My pipeline consisted of following steps:
1. Read in an image.
2. Grayscale an image. 
3. Do Gaussain smoothing.
4. Do Canny transformation.
5. Apply mask with the region of interest.
6. Detect lines with Hough transform in the region of interest.
7. Create array of vectors that are oriented from bottom of the image to top of the image from lines.
8. Filter vectors by angle and length to remove horizontal lines and noise. Noise removal is also done on step 6, but I repeat it here to guarantee the behaviour. Horizontal lines may describe lane lines on crosses, but are not interesting for this project.
9. Sort vectors by angle and length by their start points from bottom to top of the image. This step helps to work with curved lane lines.
10. Group vectors into similar groups by linear average. One group should describe one possible lane line (left or right). In fact it could be lines with noise, shadows and other. Amount of outcome groups could be more than 2.
11. Filter out groups that describes not a lane lines by length and fillrate of the lane line (see details in the notebook).
12. Calculate lane lines for each group with weighted average.
13. Print lane lines on the image. If lane line is closed to bottom, extrapolate to bottom of the image.
14. Output the image.

draw_lines function takes array of lane lines, extrapolates them to the bottom if they are closed to it and draws on an image.

Pipeline is well described in the notebook itself.

### 2. Potential shortcomings

1. Grayscaling could potentially kill important information. Grayscaling algorithm should be selected and tested very carefully. I use function from lectures, but because it is 256x256x256 -> 256 transformation it may happen that we loose some cases where we can see a line on coloured image, but do not see on a grayscale. Probably the best solution will be running this Canny transformation on three levels: R,G and B and then sum results. 
2. Detects shorter lane lines on road turns, but this will be probably fixed in advaced lane line detection project.
3. Will recognize long shadow on the road and road repairs (long black lines after renewing part of the asphalt) as lane lines.
4. I have a general feeling that test images and videos are taken in "ideal conditions". When it comes to a tricky situation, like night/snow on the road/old road/.., current pipeline may perform not well.

### 3. Possible improvements
1. There are small dots in between lane lines that helps to define not solid lane lines. I do not use them at all, but they possibly could be useful. For example, sometimes pipeline does not extrapolate lane lines to the bottom because pipeline thinks they are too far from the bottom. This dots could be used to fix that. 
2. Rewrite lane lines detection given some lane lines shape properties. For example, every lane line should contains of two almost parallel lines, that are closed to each other and with beginning and end on one y. We could also check color of detected line from source image: should be white or yellow.
3. Add level of confidence to output, so system in self driving car will understand should it trust results of lane line detection or not.
4. Add type of the line (double, solid, dash line,..) and color of the line to the output.
5. Solve the challenge - I did not manage to detect all the yellow lane line in sunny area (only around 2-3 meters far from the car)
6. Should be tested on bigger amount of test videos.
7. Adjust parameters for better performance. Run job in parallel for all possible parameters on set of test videos to detect better values.
