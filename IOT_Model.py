from array import array

class IOT_Model:
    #device property in json
    device_property_datatype = {}

    #device property sended to cloud
    device_property_tocloud = {}


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
                        return 2, "device value type error"
                else: 
                    return 3, "device_name error"
            else:
                return 3, "device_name error"

        else:
            if(device_name in self.device_property_tocloud):
                if(str(type(value))[8:-2] == self.device_property_datatype[device_name]["type"]):
                    if(eval(self.device_property_datatype["device_name"]["specs"]["min"]) <= value <= eval(self.device_property_datatype["device_name"]["specs"]["max"])):
                        self.device_property_tocloud[device_name] = value
                        return 0, ""
                    else:
                        return 1, "device value range error"
                else:
                    return 2, "device value type error"
            else:
                return 3, "device_name error"
    
    def get_property(self):
        return self.device_property_tocloud