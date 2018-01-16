## Advanced Lane Finding
[![Udacity - Self-Driving Car NanoDegree](https://s3.amazonaws.com/udacity-sdc/github/shield-carnd.svg)](http://www.udacity.com/drive)


# Advance lane lines detection project

The goal of this project is to detect lane lines on the image taken from car front camera. For implementation details and more images please check Jupyter notebook or its html version in this repo.

Steps of this project are the following:
1. Compute the camera calibration matrix and distortion coefficients given a set of chessboard images. Apply a distortion correction to raw images.
2. Apply a perspective transform to rectify binary image ("birds-eye view").
3. Use color transforms, gradients, etc., to create a thresholded binary image.
4. Detect lane pixels and fit to find the lane boundary.
5. Determine the curvature of the lane and vehicle position with respect to center.
6. Warp the detected lane boundaries back onto the original image.
7. Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

## Image undistortion
As the first step of the image processing pipeline we need to undistort the image to remove camera distortion.

### 1. Calibrate camera
First of all, we need to calibrate the camera basing on images of the chess board taken on the flat surface. We will calculate image and object points - coordinates of inner corners of the chess board on the image and normalized coordinates.

I start by preparing "object points", which will be the (x, y, z) coordinates of the chessboard corners in the world. Here I am assuming the chessboard is fixed on the (x, y) plane at z=0, such that the object points are the same for each calibration image. Thus, `objp` is just a replicated array of coordinates, and `objpoints` will be appended with a copy of it every time I successfully detect all chessboard corners in a test image. `imgpoints` will be appended with the (x, y) pixel position of each of the corners in the image plane with each successful chessboard detection.

I then used the output `objpoints` and `imgpoints` to compute the camera calibration and distortion coefficients using the cv2.calibrateCamera() function.

Undistortion of the chess board:

![png](./output_images/output_11_7.png)

Undistortion of the image taken from front camera:


![png](./output_images/output_12_2.png)


## Bird-eye transformation
As the next step I want to apply image perspective transformation to make "bird eye" view. In this case lane lines become parallel and it would be easier to calculate shape of lane lines. 

In order to perform this transformation I took one photo from the front camera where lines are parallel and calculated the coefficients for image transformation by taking coordinates of the left and right line near the car and on some distance. Probably this method will work only on flat surface and not work on hills, so for smarter solution we need smth more advanced. 

During this transofrmation I also change size of the image to make it vertical so it will be easier for my pipeline to detect lane lines. If I keep origin size, line became much shorter and it is easier to fail their detection.

![png](./output_images/output_14_5.png)


## Thresholding
As the next step I apply different techniques to get a thresholded image where white pixels will represent lane lines and black will be all the rest.

### 1. Apply Sobel operator
The Sobel operator is the heart of the Canny edge detection algorithm. As soon as I apply it to warped "bird-eye" view image where my lane lines are located vertically, I can take gradients only in x direction.

To apply Sobel operator I convert the image to HLS space and apply it to lightness channel. I tried to apply it to other channels and apply to grayscaled image, but this approach gives more robust results.

### 2. Apply color thresholding
After applying Sobel operator I miss lane lines on some part of the road, where lighting of the surface is hight. To fix it I convert the image to HLS space and apply color thresholding to saturation channel. 

### 3. Clean noize
Some objects on the image could be concidered as not lane lines even now. I remove all white horisontal lines that are longer than width of lane line.

When I compare all the images I see that combination of saturation thresholded channel and lightness channel with edge detection gives me almost whole lane lines in most of the cases. 

On images we can see from left to right: original warped image, hue channel with Sobel operator, lightness channel with Sobel operator, saturation channel with Sobel operator, saturation channel with threshold applied, saturation thresholded channel with clean noize applied

![png](./output_images/output_22_1.png)

![png](./output_images/output_22_2.png)

### 4. Combine all together
Now I can combine all thresholded images and apply noize reduction

![png](./output_images/output_26_0.png)

## Lane lines detection
As soon as I have thresholded image with lane lines on it, I can detect them. As the result I return coefficients `A`, `B` and `C` of the curve function `f(y) = A*y**2 + B*y + C`

![jpg](color-fit-lines.jpg)

![png](./output_images/output_30_0.png)

### Apply on real images
I can apply my pipeline to images from camera now

![png](./output_images/output_34_1.png)
![png](./output_images/output_34_2.png)
![png](./output_images/output_34_5.png)


## Process video

For vdeo processing I use two tricks:

1. Find lane lines from previous. If lane line was detected, I can reuse this knowledge for the next image to faster search.
2. Define Lane class that will help to average lane lines on video by keeping last x lines.

## Discussion

My pipeline works good on provided videos, but there is still room for improvements.
First and main should be sanity checks for found lane lines. So far I do not perform any sanity checks, only on first search some histogram tricks like removing of borders and center and defining peaks with expected lane line with distance. Ideally on each step I should detect of lines are still parallel and size between the lines is same and if not, then fall down into histogram search again.