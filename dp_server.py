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
    path_task = "./task_files/"
    if not os.path.exists(path_task):
        os.mkdir(path_task)

    task_id = request.form["task_id"]
    pattern = request.form["pattern"]

    print("   task_id : {}, pattern : {}".format(task_id,pattern))
    dict_task_file = {}
    for key_ in request.files:
        filename_ = request.files[key_].filename
        file_ = request.files[key_]

        print("get_task : {},{},{}".format(key_,filename_,file_))# key_ ：文件对应的字典关键字 ，filename_ :文件名字， file_ : 文件

        dict_task_file[key_] = filename_
        path_file = path_task + filename_
        file_.save(path_file)
        db_.set("{}_{}".format(task_id,key_),path_file)


    db_.set("{}_state".format(task_id),"ready")


    resp = {
        "task_id":task_id,
        "pattern":pattern,
        "task_file":dict_task_file,
        "state": "ready" ,
        }
    return Response(json.dumps(resp),  mimetype='application/json')

#查询任务状态
@app.route("/task_state", methods=['POST','GET'])
def get_task_state():
    global db_
    task_id = request.form["task_id"]
    state_= db_.get("{}_state".format(task_id))
    cost_time= db_.get("{}_cost_time".format(task_id))

    resp = {task_id:state_,
        "cost_time":cost_time,
        }

    return Response(json.dumps(resp),  mimetype='application/json')

#任务完成返回文件 video
@app.route("/target_video_file", methods=['POST','GET'])
def send_video_target_file():
    global db_
    task_id = request.form["task_id"]

    target_file_path = db_.get("{}_target_video_file".format(task_id))

    print("target_video_path: {}".format(target_file_path))
    return send_file(target_file_path)

#任务完成返回文件 image
@app.route("/target_image_file", methods=['POST','GET'])
def send_image_target_file():
    task_id = request.form["task_id"]

    target_file_path = db_.get("{}_target_image_file".format(task_id))

    print("target_image_path: {}".format(target_file_path))
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
