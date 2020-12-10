# encoding:utf-8
# date:2020-11-30
# author: x.l.eric
# function: dp client

import os
import requests
import base64
import cv2
import json
import numpy as np
import time
import traceback
import random
from pupdb.core import PupDB # 数据库
from dp_utils import *

def create_task_id():
    d_ = []
    for i in range(5):
        d_.append(chr(random.randint(97, 122)))
    d_ = "".join(d_)
    str_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    task_id = "task_{}_{}_{}".format(d_,random.randint(0,65535),str_time)
    return task_id

if __name__ == "__main__":
    #--------------------------------------------------- 步骤 1 创建任务，发起服务请求
    task_id = create_task_id()
    print("task_id",task_id)

    file_path = "./video/NBA.mp4"

    files = {"file": open(file_path, "rb")};
    data = {'task_id': task_id,
        "pattern": "video",
        }

    host = "http://127.0.0.1:"
    port = "6666"

    request_url = host + port + "/task"

    print("\n----->>>step 1 ： start task\n")
    r = requests.post(request_url,data=data,files=files)
    msg = r.json()

    for k_ in msg.keys():
        print(" {} : {}".format(k_,msg[k_]))

    #----------------------------------------------------- 步骤 2 查询任务状态
    print("\n----->>>step 2 ： get task state\n")
    request_url = host + port + "/task_state"
    flag_break = False
    while True:


        st_ = time.time()
        time.sleep(1)
        r = requests.get(request_url, data = {"task_id":task_id})
        et_ = time.time()
        msg = r.json()
        for k_ in msg.keys():
            print("{} : {}".format(k_,msg[k_]))
            if msg[k_] =="done":
                flag_break = True
                break
        if flag_break:
            break

    #------------------------------------------------------ 步骤 3 获取算法可视化结果 图像
    print("\n----->>>step 3 ： get image_target_file \n")
    request_url = host + port + "/target_image_file"
    st_ = time.time()
    r = requests.get(request_url, data={"task_id":task_id},timeout=600)
    et_ = time.time()

    if not os.path.exists('./target_image'):
        os.mkdir('./target_image')
    target_file = "./target_image/target_{}.jpg".format(task_id)
    with open(target_file, 'wb') as file_:
        print("save image target file ~")
        file_.write(r.content)

    img_ = cv2.imread(target_file)
    cv2.namedWindow("image",0)
    cv2.imshow("image",img_)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #------------------------------------------------------ 步骤 4 获取算法可视化结果 视频
    print("\n----->>>step 4 ： get video_target_file \n")
    request_url = host + port + "/target_video_file"
    st_ = time.time()
    r = requests.get(request_url, data={"task_id":task_id},timeout=600)
    et_ = time.time()

    if not os.path.exists('./target_video'):
        os.mkdir('./target_video')
    target_file = "./target_video/target_{}.mp4".format(task_id)
    with open(target_file, 'wb') as file_:
        print("save video target file ~")
        file_.write(r.content)

    #----------------------------------------------------- 步骤 5 本地显示结果文件 - 视频
    print("\n----->>>step 5 ： show target file \n")
    show_video(target_file)
