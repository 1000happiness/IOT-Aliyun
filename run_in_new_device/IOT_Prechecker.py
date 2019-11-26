from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkiot.request.v20180120.QueryDeviceRequest import QueryDeviceRequest
from aliyunsdkiot.request.v20180120.RegisterDeviceRequest import RegisterDeviceRequest

from json import loads, dumps
from time import sleep

class IOT_Prechecker:
    #aliyun_property
    aliyun_property = {}

    def __init__(self, aliyun_property):
        self.aliyun_property = aliyun_property
        
    def check(self):
        if("IotId" in self.aliyun_property):
            return True
        else:
            return False
    
    def register(self, model):
        client = AcsClient(self.aliyun_property["user_authentication"]["accessKey_id"], self.aliyun_property["user_authentication"]["accessKey_secert"], self.aliyun_property["region"])
        
        #get device_number
        request = QueryDeviceRequest()
        request.set_accept_format("json")
        request.set_ProductKey(self.aliyun_property["product_key"])
        while(True):
            response = client.do_action_with_exception(request)
            response = loads(str(response, encoding="utf-8"))
            # print(response)
            if(response["Success"]):
                break
            else:
                sleep(3)
        device_number = len(response["Data"]["DeviceInfo"])
        
        #register
        request = RegisterDeviceRequest()
        request.set_accept_format("json")
        request.set_ProductKey(self.aliyun_property["product_key"])
        request.set_DeviceName("test_device_" + str(1 + device_number))
        request.set_Nickname("监视设备_"+ str(1 + device_number))
        while(True):
            response = client.do_action_with_exception(request)
            response = loads(str(response, encoding="utf-8"))
            if(response["Success"]):
                break
            else:
                sleep(3)
        IotId = response["Data"]["IotId"]
        self.aliyun_property["IotId"] = IotId
        sender_property = {
            "link_authentication": {
                "host_name" : self.aliyun_property["region"],
                "product_key" : self.aliyun_property["product_key"],
                "device_name" : response["Data"]["DeviceName"],
                "device_secret" : response["Data"]["DeviceSecret"],
            },
            "internal_time": 300
        }

        return self.aliyun_property, sender_property