# encoding:utf-8
# date:2020-11-30
# author: x.l.eric
# function: dp utils

import cv2

def show_video(path):
    video_ = cv2.VideoCapture(path)

    while True:
        ret, frame = video_.read()

        if ret:
            cv2.namedWindow("target",0)
            cv2.imshow("target",frame)
            if cv2.waitKey(1) ==27:
                break
        else:
            break

    video_.release()
    cv2.destroyAllWindows()
