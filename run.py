# encoding:utf-8
# date:2020-12-6
# author: x.l.eric
# function: run server & client & model_inference

import os
import time
import threading
from threading import current_thread, Lock

def run_one_process(command,process_id):
    print("command : {}, process_id : {}".format(command,process_id))
    os.system(command)
if __name__ == "__main__":
    #--------------------------------------
    command_list = [
        "python ./dp_server.py 1>>log_server.txt",
        "python ./dp_client.py 1>>log_client.txt",
        "python ./model_inference.py 1>>log_model.txt",
        ]
    st_ = time.time()
    process_list = []
    for i in range(len(command_list)):
        # print(video_list[i])
        t = threading.Thread(target=run_one_process, args=(command_list[i],i))
        process_list.append(t)

    print(' start run ~ ')
    for i in range(len(process_list)):
        process_list[i].start()
        time.sleep(5)

    et_ = time.time()
    print(' time cost : {:.6f}'.format(et_-st_))


    for i in range(len(process_list)):
        process_list[i].join()# 设置主线程等待子线程结束

    del process_list

    print(' well done ~')
