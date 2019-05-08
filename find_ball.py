from imutils.video import VideoStream
import numpy as np
import cv2
import imutils
import time


class FindBall():
    BUFFER_SIZE = 64

    def __init__(self, camera_num):
        self.greenLower = (53, 55, 58)
        self.greenUpper = (86, 160, 219)
        # self.pts = deque(maxlen=FindBall.BUFFER_SIZE)
        self.vs = VideoStream(src=camera_num).start()

        # we might not want to put it here
        time.sleep(2.0)

    def get_x_location(self):
        frame = self.vs.read()
        # resize the frame, blur it, and convert it to the HSV
        # color space
        frame = imutils.resize(frame, width=600)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        # construct a mask for the color "green", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, self.greenLower, self.greenUpper)
        mask = cv2.erode(mask, None, iterations=2)
        # find contours in the mask and initialize the current
        mask = cv2.dilate(mask, None, iterations=2)
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None
        x = None
        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # only proceed if the radius meets a minimum size
            if radius > 10:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),
                           (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
        # show the frame to our screen
        cv2.imshow("Frame", frame)
        return x
