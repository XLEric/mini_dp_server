# encoding:utf-8
# date:2020-11-30
# author: x.l.eric
# function: dp inference

import os
from pupdb.core import PupDB # 数据库
import time

def get_file_state(db):
    db_list = list(db.items())
    need_do_list = []

    for f in db_list:
        if ('_state' in f[0]):

            path_video = db_.get(f[0].replace("_state","_task_video_file"))
            path_image = db_.get(f[0].replace("_state","_task_image_file"))
            task_id = f[0].replace("_state","")
            print("   --->>> {} : {}".format(f[0],f[1]))
            print("          task_id ： {} ，model process video: {}, image : {}".format(task_id,path_video,path_image))

            if ('_state' in f[0]) and (f[1] == 'ready'):
                pass
                need_do_list.append((task_id,f[0],path_video,path_image))

    return need_do_list

if __name__ == "__main__":
    # todo 模型初始化
    db_ = PupDB('./db/db.json')
    while True:
        need_do_list = get_file_state(db_)

        for f_ in need_do_list:
            task_id,task_state,task_video_path,task_image_path = f_
            print("------------------->>> inference task_id :{}".format(task_id))
            db_.set("{}_state".format(task_id),"processing")
            time.sleep(5)
            # todo
            # step1: 模型 前向推断
            # step2: 保存模型输出文件（视频)
            # step3: 将输出文件路径(信息)回写 db数据库key： task_id + “_target_file”
            db_.set("{}_target_video_file".format(task_id),task_video_path)
            db_.set("{}_target_image_file".format(task_id),task_image_path)
            # step4：将输出文件路径回写 db数据库key：task_id + “_state” : "done"
            db_.set("{}_state".format(task_id),"done")

        time.sleep(1)
