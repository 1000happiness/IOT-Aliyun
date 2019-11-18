from json import load
from time import sleep
from threading import Thread
import signal

from IOT_Model import IOT_Model
from IOT_Localserver import IOT_Localserver
from IOT_Sender import IOT_Sender

device_property_path = "device_property.json"
device_authentication_path = "sender_property.json"
localserver_property_path = "localserver_property.json"

def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper

def readjson(path):
    file = open(path, "r")
    fileJson = load(file)
    return fileJson

# print(readjson(device_property_path))
# print(readjson(device_authentication_path))
# print(readjson(localserver_property_path))

@async
def run_sender(sender):
    print("Connecting to Aliyun")
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
        print("IOT_sender: timeout error")
    else:
        print("Begin post property to Aliyun")
        sender.begin_property_post()

def sig_exit(signum, sender):
    pass

def main():
    model = IOT_Model(readjson(device_property_path))
    sender = IOT_Sender(readjson(device_authentication_path), model)
    localserver = IOT_Localserver(readjson(localserver_property_path), model)
    
    run_sender(sender)

    print("if you want to stop the programe please input \"ctrl + c\"")

    #localserver.run()
    sleep(3)
    sender.disconnect()
    print("end")

main()
    