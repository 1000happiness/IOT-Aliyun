from json import load, dumps
from time import sleep
from threading import Thread

from IOT_Prechecker import IOT_Prechecker
from IOT_Model import IOT_Model
from IOT_Localserver import IOT_Localserver
from IOT_Sender import IOT_Sender

aliyun_property_path = "Aliyun_property.json"
device_property_path = "device_property.json"
sender_property_path = "sender_property.json"
localserver_property_path = "localserver_property.json"

def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper

def readjson(path):
    file = open(path, "r")
    fileJson = load(file)
    file.close()
    return fileJson

@async
def begin_sender(sender):
    
    sender.begin_property_post()

def main():
    model = IOT_Model(readjson(device_property_path))
    prechecker = IOT_Prechecker(readjson(aliyun_property_path))

    if(not prechecker.check()):
        print("begin to register")
        aliyun_property, sender_property = prechecker.register(model)
        blank_string = 20 * [(" " * 100 + "\n")]
        
        file = open(aliyun_property_path, "w")
        file.writelines(blank_string)
        file.seek(0,0)
        file.write(dumps(aliyun_property))
        file.close()

        file = open(sender_property_path, "w")
        file.writelines(blank_string)
        file.seek(0,0)
        file.write(dumps(sender_property))
        file.close()

    sender = IOT_Sender(readjson(sender_property_path), model)
    localserver = IOT_Localserver(readjson(localserver_property_path), model)
    
    print("Connect to Aliyun")
    sender.connect()
    i = 0
    while(True):
        state = sender.get_state()
        print("The IOT_sender state is", state)
        if(sender.ready()):
            break
        sleep(1)
        i = i + 1 
        if(i == 10):
            break
    if(i == 10):
        print("IOT_sender: can not connect to ALiyun timeout error")
        return
    else:
        print("Begin send property to Aliyun")

    begin_sender(sender)

    print("if you want to stop the programe please input \"ctrl + c\"")

    localserver.run()
    
    print("end")

main()
    
