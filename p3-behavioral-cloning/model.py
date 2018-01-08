import numpy as np    
import cv2                 
import csv
import tensorflow as tf
from sklearn.utils import shuffle

from keras.models import Sequential
from keras.layers.core import Dense, Flatten, Dropout, Lambda
from keras.layers.convolutional import Convolution2D
from keras.layers.pooling import MaxPooling2D
from keras.layers.advanced_activations import ELU
from keras.optimizers import Adam

from common_functions import preprocess_image

# data generator
def data_gen(paths, angles, batch_size=128):
    X = []
    y = []
    while True:       
        paths, angles = shuffle(paths, angles)
        for i in range(len(paths)):
            img = cv2.imread(paths[i])
            angle = angles[i]
            img = preprocess_image(img, "BGR")
            X.append(img)
            y.append(angle)
            X.append(cv2.flip(img, 1))
            y.append(angle*-1)

            if len(X) >= batch_size:
                # print("Data loaded(%): ",round(i*100/len(paths)))
                yield (np.array(X), np.array(y))
                X = []
                y = []

# parsing log file
def load_data(paths):
    img_paths = []
    angles = []

    for path in paths:
        with open(path + 'driving_log.csv', newline='') as f:
            reader = csv.reader(f, skipinitialspace=True, delimiter=',', quoting=csv.QUOTE_NONE)
            next(reader, None)
            log = list(reader)
            
            for record in log:
                # take only non zero speed to exclude possible wrong data
                if float(record[6]) > 0: 
                    # take only front camera image
                    img_path = record[1]
                    # add name of the directory to non absolute paths
                    if img_path[0] != '/':
                        img_path = path + img_path
                    angle = float(record[3])
                    img_paths.append(img_path)
                    angles.append(angle)

                    # adding left and right camera images
                    # img_path_left = record[0]
                    # if img_path_left[0] != '/':
                    #     img_path_left = path + img_path_left
                    # img_path_right = record[2]
                    # if img_path_right[0] != '/':
                    #     img_path_right = path + img_path_right
                    # img_paths.append(img_path_left)
                    # angles.append(angle + 0.2)
                    # img_paths.append(img_path_right)
                    # angles.append(angle - 0.2)

    return (np.array(img_paths), np.array(angles))

# print stats of the dataset
def print_stats(array, n_bins):
    hist, bins = np.histogram(array, n_bins)
    for i in range(len(hist)):
        print("angle {0}: {1}".format(round(bins[i],2), hist[i]))
 
# limit dataset to make angles distribution more normal
# limit amount of images with same angle to threshold value
# I don't like realization of this solution, but did not come up with better one
def truncate_data(paths, angles, threshold):
    paths, angles = shuffle(paths, angles)
    res_paths = []
    res_angles = []
    cnt_a = np.empty([0,2])
    for i in range(len(angles)):
        add = True
        current_cnt = 0
        tmp_cnt_a = np.empty([0,2])
        for cnt in cnt_a:
            if cnt[0] == angles[i]:
                current_cnt = cnt[1]
                if (current_cnt >= threshold):
                    add = False
                    tmp_cnt_a = np.concatenate((tmp_cnt_a, np.array([cnt])))
            else:
                tmp_cnt_a = np.concatenate((tmp_cnt_a, np.array([cnt])))

        if add:
            res_paths.append(paths[i])
            res_angles.append(angles[i])
            cnt_a = np.concatenate((tmp_cnt_a, np.array([[angles[i], current_cnt + 1]])))
    return (res_paths, res_angles)

# Split data to train and validation datasets
def split_data(X, y, val_percentage):
    X, y = shuffle(X, y)
    train_X = []
    valid_X = []
    train_y = []
    valid_y = []
    for i in range(len(X)):
        if (i*100/len(X) < val_percentage):
            valid_X.append(X[i])
            valid_y.append(y[i])
        else: 
            train_X.append(X[i])
            train_y.append(y[i])
    return (train_X, train_y, valid_X, valid_y)

# model definition (NVidia)
def get_model():
    model = Sequential()

    # normalize
    model.add(Lambda(lambda x: x/255 - 0.5, input_shape=(66,200,3)))

    # three 5x5 convolution layers
    model.add(Convolution2D(24, 5, 5, subsample=(2, 2), activation='relu'))
    model.add(Convolution2D(36, 5, 5, subsample=(2, 2), activation='relu'))
    model.add(Convolution2D(48, 5, 5, subsample=(2, 2), activation='relu'))

    # two 3x3 convolution layers
    model.add(Convolution2D(64, 3, 3, activation='relu'))
    model.add(Convolution2D(64, 3, 3, activation='relu'))

    # flatten
    model.add(Flatten())

    # three fully connected layers
    model.add(Dense(100))
    #model.add(Dropout(0.5))
    model.add(Dense(50))
    #model.add(Dropout(0.5))
    model.add(Dense(10))
    model.add(Dropout(0.5))

    # output layer
    model.add(Dense(1))

    model.compile(optimizer=Adam(lr=0.001), loss='mse')

    return model


epochs = 10
source_data = ['record data/', 'udacity data/']
# source_data = ['record data/']

img_paths, angles = load_data(source_data)

print("RAW data:")
print_stats(angles, n_bins = 25)

img_paths, angles = truncate_data(img_paths, angles, threshold = 200)
print("Truncated:")
print_stats(angles, n_bins = 25)

image_paths_train, angles_train, image_paths_val, angles_val = split_data(img_paths, angles, val_percentage = 5)
print('Train cnt:', len(image_paths_train))
print('Validate cnt:', len(image_paths_val))

model = get_model()

train_gen = data_gen(image_paths_train, angles_train)
val_gen = data_gen(image_paths_val, angles_val)

model.fit_generator(train_gen, validation_data=val_gen, nb_epoch=epochs, verbose=2, 
    samples_per_epoch=len(image_paths_train), nb_val_samples=len(image_paths_val))

print(model.summary())
model.save('./model.h5')
