# IOT_Aliyun

该脚本主要负责将硬件信息上传至云端，实现方式为：首先该脚本在硬件本地的一个端口运行一个服务器，硬件可以随时访问服务器，将最新的硬件信息通过http连接上传至本地服务器，而该服务器（local server）会根据硬件的信息实时更新本地物模型（model）上的数据；同时该脚本在本地会运行数据发送模块，每隔一段时间向阿里云服务器发送物模型上的数据

## architecture
IOT_Localserver.py本地服务器
IOT_model.py物模型
IOT_Sender.py向阿里云发送数据的模块
这三个文件请不要进行任何更改，如果怀疑此处python脚本出现问题请与刘千禧（13162008952）联系

## usage

```json
// POST /property
// request
{
    device_name:"camera_1",
    value: 1
}
// success response
{
    success: true
}
// error response 
{
    success: false,
    errmsg: ""
}
```
usage example
curl -X POST -i http://localhost:8092/property --data '{
    "device_name":"camera_1",
    "value":2
}'


## about device name

设备名是访问的服务器的一个重要参数，对于本地服务器而言相当于标识。如果某一个设备在系统中只有一个（例如温度计），其命名为device_property.json中identifier的值；如果某一个设备在系统中出现多次，其命名为device_property.json中的identifier的值加上从0开始计数的设备编号，两者用下划线隔开，例如”camera_1”
