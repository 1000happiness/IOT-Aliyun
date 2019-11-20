from array import array

class IOT_Model:
    #device property in json
    device_property_json = {}

    #device property sended to cloud
    device_property_tocloud = {}


    #init: initailize device_property_tocloud by device_property_json
    def __init__(self, device_property_json):
        self.device_property_json = device_property_json
        property_list = self.device_property_json["properties"]
        for it in property_list:
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
                    temp_list = list(self.device_property_tocloud[name_index[0]])
                    temp_list[eval(name_index[1])] = value
                    self.device_property_tocloud[name_index[0]] = tuple(temp_list)
        else:
            if(device_name in self.device_property_tocloud):
                self.device_property_tocloud[device_name] = value
    
    def get_property(self):
        return self.device_property_tocloud