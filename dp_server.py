# encoding:utf-8
# date:2020-11-30
# author: x.l.eric
# function: dp service

import os
import base64
from flask import request, Flask, Response, send_file
import requests
import cv2
import numpy as np
import json
import time
from pupdb.core import PupDB # 数据库

app = Flask(__name__)

#接受任务请求
@app.route("/task", methods=['POST','GET'])
def get_task():
    global db_
    task_id = request.form["task_id"]
    pattern = request.form["pattern"]
    file_video = request.files['file_video']
    file_image = request.files['file_image']
    video_name = file_video.filename
    image_name = file_image.filename
    print("   task_id : {}, pattern : {}, video_name : {}, image_name : {}".format(task_id,pattern,video_name,image_name))
    #
    if not os.path.exists('./server_video'):
        os.mkdir('./server_video')
    # 视频文件写入磁盘
    path_file = './server_video/'+video_name
    file_video.save(path_file)
    db_.set("{}_task_video_file".format(task_id),path_file)

    if not os.path.exists('./server_image'):
        os.mkdir('./server_image')
    # 视频文件写入磁盘
    path_file = './server_image/'+image_name
    file_image.save(path_file)
    db_.set("{}_task_image_file".format(task_id),path_file)

    db_.set("{}_state".format(task_id),"ready")


    resp = {
        "task_id":task_id,
        "pattern":pattern,
        "video_name":video_name,
        "image_name":image_name,
        "state": "ready" ,
        }
    return Response(json.dumps(resp),  mimetype='application/json')

#查询任务状态
@app.route("/task_state", methods=['POST','GET'])
def get_task_state():
    global db_
    task_id = request.form["task_id"]
    state_= db_.get("{}_state".format(task_id))

    resp = {task_id:state_}

    return Response(json.dumps(resp),  mimetype='application/json')

#任务完成返回文件 video
@app.route("/target_video_file", methods=['POST','GET'])
def send_video_target_file():
    task_id = request.form["task_id"]

    target_file_path = db_.get("{}_target_video_file".format(task_id))

    print("target_video_path".format(target_file_path))
    return send_file(target_file_path)

#任务完成返回文件 image
@app.route("/target_image_file", methods=['POST','GET'])
def send_image_target_file():
    task_id = request.form["task_id"]

    target_file_path = db_.get("{}_target_image_file".format(task_id))

    print("target_image_path".format(target_file_path))
    return send_file(target_file_path)

if __name__ == "__main__":
    #多进程或多线程只能选择一个，不能同时开启
    # threaded=True
    # processes=True
    # 如果需要在通过flask 在不同计算机进行通信， host 需要设置为 0.0.0.0
    print("/*************** video algorithm service start****************/")
    if not os.path.exists('./db'):
        os.mkdir('./db')
    global db_
    db_ = PupDB('./db/db.json')
    app.run(
        host = "127.0.0.1",
        port= 6666,
        debug = True,
        threaded = True,
        )
