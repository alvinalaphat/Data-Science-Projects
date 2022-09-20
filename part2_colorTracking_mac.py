from turtle import color
import cv2
import numpy as np

cam = cv2.VideoCapture(0)

while (True):
    retval, img = cam.read()

    res_scale = 0.5
    img = cv2.resize(img, (0,0), fx = res_scale, fy = res_scale)

    lower = np.array([161, 197, 51])
    upper = np.array([183, 218, 105])
    objmask = cv2.inRange(img, lower, upper)

    lower2 = np.array([97, 206, 229])
    upper2 = np.array([107, 216, 238])
    objmask2 = cv2.inRange(img, lower2, upper2)

    lower3 = np.array([185, 77, 68])
    upper3 = np.array([207, 99, 82])
    objmask3 = cv2.inRange(img, lower3, upper3)

    def find_objects(objmask):

        kernel = np.ones((5,5), np.uint8)
        objmask = cv2.morphologyEx(objmask, cv2.MORPH_CLOSE, kernel=kernel)
        objmask = cv2.morphologyEx(objmask, cv2.MORPH_DILATE, kernel=kernel)
        cv2.imshow("Image after morphological operations", objmask)

        cc = cv2.connectedComponents(objmask)
        ccimg = cc[1].astype(np.uint8)

        # Find contours of these objects
        contours, hierarchy = cv2.findContours(ccimg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
        minObjectSize = 100;

        if contours:

            # use the biggest object to draw a rectangle
            c = sorted(contours, key = cv2.contourArea, reverse=True)
            x, y, w, h = cv2.boundingRect(c[0])

            # TIP: you want to get bounding boxes of ALL contours (not only the first one)
            if w > minObjectSize or h > minObjectSize:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,0), 3)
                cv2.putText(img,            # image
                "Object detected",          # text
                (x, y-10),                  # start position
                cv2.FONT_HERSHEY_SIMPLEX,   # font
                0.7,                        # size
                (0, 255, 0),                # BGR color
                1,                          # thickness
                cv2.LINE_AA)                # type of line

    find_objects(objmask)
    find_objects(objmask2)
    find_objects(objmask3)

    cv2.imshow("Live WebCam", img)
    action = cv2.waitKey(1)
    if action==27:
        break
    
cam.release()
cv2.destroyAllWindows()