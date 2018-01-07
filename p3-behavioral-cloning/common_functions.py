def preprocess_image(img, scheme):
    import cv2

    #crop
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