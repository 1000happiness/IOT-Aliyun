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
                self.device_property_tocloud[it["identifier"]] = [None] * eval(it["dataType"]["specs"]["size"])
            else:
                self.device_property_tocloud[it["identifier"]] = None
    
    #update: update data in model
    def update_property(self, device_name, value):
        if('0' <= device_name[-1] <= '9'):
            name_index = device_name.split("_", 1)
            if(name_index.len() == 2):
                if(self.device_property_tocloud.has_key(name_index[0])):
                    self.device_property_tocloud[name_index[0]][eval(name_index[1])] = value
        else:
            if(self.device_property_tocloud.has_key(device_name)):
                self.device_property_tocloud[device_name] = value
    
    def get_property(self):
        return self.device_property_tocloud