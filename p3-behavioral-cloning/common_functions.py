# all preprocessing is moved to an external function to guarantee the same preprocessing in training and driving
def preprocess_image(img, scheme):
    import cv2

    # crop
    # I know it could be done in Keras with Cropping2D function, but I want to guarantee same cropping
    # in both model.py and drive.py (training and driving)
    res = img[50:140,:,:] 
    
    # convert to YUV
    if scheme == "BGR":
        res = cv2.cvtColor(res, cv2.COLOR_BGR2YUV)
    if scheme == "RGB":
        res = cv2.cvtColor(res, cv2.COLOR_RGB2YUV)

    # resize to model first layer
    res = cv2.resize(res,(200, 66), interpolation = cv2.INTER_AREA)

    # remove noise
    res = cv2.GaussianBlur(res, (5,5), 0) 
 
    return res 