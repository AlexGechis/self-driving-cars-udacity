**Behavioral Cloning Project**

The goals / steps of this project are the following:
* Use the simulator to collect data of good driving behavior
* Build, a convolution neural network in Keras that predicts steering angles from images
* Train and validate the model with a training and validation set
* Test that the model successfully drives around track one without leaving the road
* Summarize the results with a written report


[//]: # (Image References)

[image1]: ./img/example.jpg "Front camera image"
[image2]: ./img/model.png "Model"
[image3]: ./img/data_dist.png "Data distribution"


### Files Submitted & Code Quality

My project includes the following files:
* model.py - containing the script to create and train the model
* drive.py - for driving the car in autonomous mode
* model.h5 - containing a trained convolution neural network 
* readme.md - summarizing the results
* run.mp4 - video for one loop of driving car in autonomous mode with the model
* common_functions.py - preprocess image functions to guarantee same preprocess in training and driving

### Model Architecture and Training Strategy

#### Overall description
As suggested in the course I used NVidia architecture for this project. I think that for this simulator lighter model could be applied, but I wanted to see how NVidia model performs here and decided to use it.

![Model][image2]

My model uses RELU activations, and the data is normalized in the model using a Keras lambda layer (code line 128). 

The model contains dropout layers in order to reduce overfitting (model.py line 148). I tried different approaches for dropout (add in different places and with different keep probability) and ended up with only one dropout before the last layel, which gives me possibility to reduce overfitting and performs good results at testing. 

The model used an adam optimizer, so the learning rate was not tuned manually (model.py line 153).

The model was trained and validated on different data sets to ensure that the model was not overfitting (code line 171). To get validation data I simply get 5 random percent of the data as validation and use the rest 95% as training data. The model was tested by running it through the simulator and ensuring that the vehicle could stay on the track.

#### Training data

Training data was chosen to keep the vehicle driving on the road. I used combination of Udacity data and data captured by my own. To create my own data I recorded 2 loops of driving and 5-10 times recording of some possible hard places for the model (bridge and place with no borders).

I used only videos captured from front camera of the vechice, because when I tried to use three images car behavior was not so confident on the track as only with one. I think it is result of my driving style: my strategy is not to get to the center of the road, it is not to get out of the road. For example, for me is OK to be on 1/3 and drive forward without stearing. At this moments, one of the cameras, the one that is closer to the center of the road, had some steering angle, which was wrong. Also, we need to keep in mind that only one image from front camera is used in autonomous mode of the simulator. One more motivation not to use it was because I like how my model works only with front camera. So, I did not see any point in adding left and right camera images. I left code part that adds this images to show my approach in the code, see commented lines from line 60.

![Front camera][image1]

For every image I added flipped horisontally image with steering angle * -1 to make model more universal.

One important thing was to make angles distribution more normal: for some angles there were a lot of images, while for others just few. If I used raw dataset, angles with a lot of images could negatively affect the model and it would be fitted more for this angles and may fail in cases where stronger steering angle is required. Here was raw angle distribution (left) and after cleaning the data (right):

![Data distribution][image3]

I did not add any image augmentation for this project because in simulator lightning is normal during whole tracks.

#### Solution

Here is how my model creation works:

##### Load the data 
1. Read log and load list of angles and images to the dataset
2. Clean the dataset by normalizing distribution (limiting amount of images of every angle to some value)

##### Define the model
I used NVidia architecture for this model.

The only things I added were:
* Dropouts to reduce overfitting
* Activation functions (I tried different approaches and ended up with RELU)
* Lambda normalization layer before the model

##### Fit the model with data generator:

1. Preprocess the image:
* crop image to remove unused areas of the image without important information (information that does not have influence on driving)
* convert to YUV as suggested in NVidia paper
* make Guassian blur to remove noise

2. Load this image and mirrored with angle*-1 to the model

I used 10 epochs for training the model.

### Notes

The vehicle was able to drive autonomously around the track without leaving the road from the first try. All further changes were focused on making vechicle move more smooth, looking at what changes in the behaviour and playing with the challenge. 

