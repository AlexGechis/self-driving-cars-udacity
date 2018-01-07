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


### Files Submitted & Code Quality

My project includes the following files:
* model.py containing the script to create and train the model
* drive.py for driving the car in autonomous mode
* model.h5 containing a trained convolution neural network 
* readme.md summarizing the results
* run.mp4 video for one loop of driving car in autonomous mode with the model

### Model Architecture and Training Strategy

As suggested in the course I used NVidia architecture for this project.
![Model][image2]

My model uses RELU activations, and the data is normalized in the model using a Keras lambda layer (code line 116). 

The model contains dropout layers in order to reduce overfitting (model.py line 136). I tried different approaches for dropout (add in different places and with different keep probability) and ended up with only one dropout before the last layel, which gives me possibility to reduce overfitting and performs good results at testing. 

The model was trained and validated on different data sets to ensure that the model was not overfitting (code line 159). To get validation data I simply get 5 random percent of the data as validation and use the rest 95% as training data. The model was tested by running it through the simulator and ensuring that the vehicle could stay on the track.

The model used an adam optimizer, so the learning rate was not tuned manually (model.py line 141).

Training data was chosen to keep the vehicle driving on the road. I used combination of Udacity data and data captured by my own. To create my own data I recorded 2 loops of driving and 5-10 times recording of some possible hard places for the model (bridge and place with no borders).

I used only videos captured from front camera of the vechice, because when I tried to use three images car behavior was not so confident on the track as only with one.
![Front camera][image2]

For every image I added flipped horisontally image with steering angle * -1 to make model more universal.

One important thing was to make angles distribution more normal: for some angles there were a lot of images, while for others just few. If I used raw dataset, angles with a lot of images could negatively affect the model and it would be fitted more for this angles and may fail in cases where stronger steering angle is required. Here was raw angle distribution:
```angle -0.94: 5
angle -0.86: 6
angle -0.79: 4
angle -0.71: 7
angle -0.63: 9
angle -0.55: 35
angle -0.48: 89
angle -0.4: 113
angle -0.32: 367
angle -0.24: 391
angle -0.17: 791
angle -0.09: 855
angle -0.01: 7871
angle 0.07: 543
angle 0.15: 595
angle 0.22: 147
angle 0.3: 181
angle 0.38: 33
angle 0.46: 33
angle 0.53: 12
angle 0.61: 7
angle 0.69: 4
angle 0.77: 0
angle 0.84: 0
angle 0.92: 2
```
And after removing some of the images distribution looks better:
```
angle -0.94: 5
angle -0.86: 6
angle -0.79: 4
angle -0.71: 7
angle -0.63: 9
angle -0.55: 35
angle -0.48: 89
angle -0.4: 113
angle -0.32: 367
angle -0.24: 391
angle -0.17: 791
angle -0.09: 855
angle -0.01: 758
angle 0.07: 543
angle 0.15: 558
angle 0.22: 147
angle 0.3: 181
angle 0.38: 33
angle 0.46: 33
angle 0.53: 12
angle 0.61: 7
angle 0.69: 4
angle 0.77: 0
angle 0.84: 0
angle 0.92: 2```

I used 10 epochs for training the model.

### Notes

The overall strategy was to use NVidia architecture.

The only things I added were:
* Dropouts to reduce overfitting
* Activation functions (I tried different approaches and ended up with RELU)
* Lambda normalization layer before the model

The vehicle was able to drive autonomously around the track without leaving the road from the first try. All further changes were focused on making vechicle move more smooth, looking at what changes in the behaviour and playing with the challenge. 

