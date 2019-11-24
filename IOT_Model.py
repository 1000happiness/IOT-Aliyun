from array import array
from json import dumps

class IOT_Model:
    #device property in json
    device_property_datatype = {}

    #device property sended to cloud
    device_property_tocloud = {}

    #update_flag
    update_flag = False

    #picture
    picture = ""

    #init: initailize device_property_tocloud by device_property_json
    def __init__(self, device_property_json):
        # self.device_property_datatype = device_property_json
        property_list = device_property_json["properties"]
        for it in property_list:
            self.device_property_datatype[it["identifier"]] = it["dataType"]
            if(it["dataType"]["type"] == "array"):
                self.device_property_tocloud[it["identifier"]] = (None,) * eval(it["dataType"]["specs"]["size"])
            else:
                self.device_property_tocloud[it["identifier"]] = None
    
    #update: update data in model
    def update_property(self, device_name, value):
        if('0' <= device_name[-1] <= '9'):
            name_index = device_name.split("_", 1)
            if(len(name_index) == 2):
                if(name_index[0] in self.device_property_tocloud):
                    if(str(type(value))[8:-2] == self.device_property_datatype[name_index[0]]["specs"]["item"]["type"]):
                        temp_list = list(self.device_property_tocloud[name_index[0]])
                        temp_list[eval(name_index[1])] = value
                        self.device_property_tocloud[name_index[0]] = tuple(temp_list)
                        return 0, ""
                    else:
                        return 1, "device value type error"
                else: 
                    return 2, "device_name error"
            else:
                return 2, "device_name error"

        else:
            if(device_name in self.device_property_tocloud):
                if(str(type(value))[8:-2] == self.device_property_datatype[device_name]["type"]) or (str(type(value))[8:-2] == "str" and self.device_property_datatype[device_name]["type"] == "text" or (str(type(value))[8:-2] == "int" and self.device_property_datatype[device_name]["type"] == "float")):
                    self.device_property_tocloud[device_name] = value
                    return 0, ""
                else:
                    return 1, "device value type error"
            else:
                return 2, "device_name error"
    
    def get_property(self):
        return self.device_property_tocloud

    def get_update_flag(self):
        return self.update_flag
    
    def set_update_flag(self, new_flag):
        self.update_flag = new_flag

    def get_picture(self):
        return self.picture

    def set_picture(self, new_picture_args):
        if("device_name" in new_picture_args):
            if(new_picture_args["device_name"].find("Camera") != -1):
                self.picture = dumps(new_picture_args)
                return 0, ""
            else:
                return 2, "not Camera"
        else:
            return 3, "device_name error"

    def set_picture_direct(self, new_picture):
        self.picture = new_picture
        