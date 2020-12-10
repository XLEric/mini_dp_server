# mini_dp_server  

## client 客户端 (dp_client.py)  
 步骤1：发任务请求，传输文件。  
 步骤2：查询任务状态 （默认：ready,processing,done）。  
 步骤3：任务状态为 "done"，返回文件或是信息。  

## server 服务端 (dp_server.py)  
 步骤1：开启任务，接受文件。  
 步骤2：根据客户端请求返回任务状态。  
 步骤3：根据客户端请求且完成任务，回传文件。  

##  模型 (model_inference.py)  
 独立进程，模型进程与服务端通过小型db数据库通信。  

##  db数据库   
 关键字：  
 task_id + "_state"：状态  
 task_id + "_task_file" : 客户端请求文件路径  
 task_id + "_target_file": 算法服务输出文件路径   

##  同时开启例子脚本 (run.py)   
 同时开启脚本包括：dp_server.py && dp_client.py && model_inference.py   
 (注意：对于多进程管理建议使用 supervisor)   
