# IOT_Aliyun

该脚本主要负责将硬件信息上传至云端，实现方式为：首先该脚本先根据配置文件检测该设备是否在Aliyun上进行注册，如果没有，则进行注册，之后在硬件本地的一个端口运行一个服务器，硬件可以随时访问服务器，将最新的硬件信息通过http连接上传至本地服务器，而该服务器（local server）会根据硬件的信息实时更新本地物模型（model）上的数据；同时该脚本在本地会运行数据发送模块，每隔一段时间向阿里云服务器发送物模型上的数据

## architecture
IOT_Prechecker.py注册验证脚本

IOT_Localserver.py本地服务器

IOT_model.py物模型

IOT_Sender.py向阿里云发送数据的模块

这四个文件请不要进行任何更改，如果怀疑此处python脚本出现问题请与刘千禧（13162008952）联系

## 配置文件
Aliyun_property.json 阿里云账号配置文件，用于设备注册

Device_proeprty.json 设备发送给阿里云的数据类型和名称，用于设备初始化

Localserver_property.json 设备本地服务器的信息，包含服务器运行的端口

Sender_property.json 设备认证文件和发送消息的间隔，该文件在新硬件上并不存在，在脚本第一运行，注册设备后会自动生成

## 使用方式

```json
// POST /property
// request
{
    "device_name":"Camera_1",
    "value": 1
}
// success response
{
    "success": true
}
// error response 
{
    "success": false,
    "errmsg": ""
}

// POST /plate_number
// request
{
    "PlateNumber": "苏A -00000"
}
// success response
{
    "success": true
}
// error response 
{
    "success": false,
    "errmsg": ""
}

// POST /flush
// request
{}
// success response
{
    "success": true
}
// error response never happned
{
    "success": false,
    "errmsg": ""
}

// POST /picture
// request
the sender wiil send the picture to Aliyun immidiately
{
    "device_name":"Camera_1", // must be "Camera" or "Camera_XXX" 
    "picture" : "12323121231212sdkvkjawehlkajnvkjeauihesdnvkjabgkwaef" // base64 string
}
// success response
{
    "success": true
}
// error response 
{
    "success": false,
    "errmsg": ""
}
```
usage example

curl -X POST -i http://localhost:8093/property --data '{
    "device_name":"camera_1",
    "value":2
}'


## about device name

设备名是访问的服务器的一个重要参数，对于本地服务器而言相当于标识。如果某一个设备在系统中只有一个（例如温度计），其命名为device_property.json中identifier的值，例如”Shake”；如果某一个设备在系统中出现多次，其命名为device_property.json中的identifier的值加上从0开始计数的设备编号，两者用下划线隔开，例如”Camera_1”

## somethine more
请查阅 IOT脚本使用方式.docx
