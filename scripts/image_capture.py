#!/usr/bin/env python3.6
''' /usr/local/bin/image_capture is a hard link from ~/chessmate/image_capture.py
to make it globally accessible as an executable
'''

import cv2
import sys
import argparse
import os
import numpy as np
import datetime

from pathlib import Path
from matplotlib import pyplot as plt

def main():

    #  Allowing definition of an output path for captured images
    parser = argparse.ArgumentParser(description="capturing images from csi camera module")
    parser.add_argument("outputpath", nargs='?', default="")
    args = parser.parse_args(sys.argv[1:])

    # If output path doesn't exist or is not empty exit application
    print(args.outputpath)
    if not os.path.exists(args.outputpath) and not args.outputpath=="":
        print("Output directory {} does not exist.".format(args.outputpath))
        sys.exit()
    
    os.chdir(args.outputpath)
    cam=cv2.VideoCapture(4)
    backendname = cam.getBackendName()
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cam.set(cv2.CAP_PROP_FPS, 90)
    
    print(cam.isOpened())
    ret, frame = cam.read()
    if not ret:
        print("Failed to grab initial frame. Fix camera!")
        sys.exit()

    img_counter = 0
    time = datetime.datetime.now()
    while True:
        t_delta = datetime.datetime.now() - time
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame.")
            break
        rgb_img_cropped = frame[0:640, 0:640]
        cv2.imshow("view", rgb_img_cropped)

        k = cv2.waitKey(1)
        if k%256 == 27:
            print("Escape pressed, closing...")
            break
        elif k%256 == 32:
            now = datetime.datetime.now()
            timestring = "{}_{}_{}_{}_{}".format(now.day,now.month,now.hour,now.minute,now.second)
            img_name = "juggleball_{}.jpg".format(timestring)
            cv2.imwrite(img_name, rgb_img_cropped)
            print("img from time {} written".format(timestring))
        elif t_delta.microseconds / 1000 >= 250:
            now = datetime.datetime.now()
            timestring = "{}_{}_{}_{}_{}".format(now.day,now.month,now.hour,now.minute,now.second)
            img_name = "juggleball_{}.jpg".format(timestring)
            cv2.imwrite(img_name, rgb_img_cropped)
            print("img from time {} written".format(timestring))
            time = datetime.datetime.now()


    cam.release()

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
