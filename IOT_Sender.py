from linkkit import linkkit
from time import sleep


class IOT_Sender:
    #link to ALiyun
    lk = None

    #IOT_model
    IOT_model = {}

    #internal_time
    internal_time = 300

    #ready
    ready = False

    #init: initailize lk by linkkit
    def __init__(self, sender_property, IOT_model):
        
        self.lk = linkkit.LinkKit(
            host_name=sender_property["link_authentication"]["host_name"],
            product_key=sender_property["link_authentication"]["product_key"],
            device_name=sender_property["link_authentication"]["device_name"],
            device_secret=sender_property["link_authentication"]["device_secret"]
        )

        self.lk.thing_setup("device_property.json")

        self.IOT_model = IOT_model

        self.internal_time = sender_property["internal_time"]
        
    def connect(self):
        self.lk.connect_async()
        self.lk.start_worker_loop()

    def disconnect(self):
        self.ready = False
        if(self.get_state() == linkkit.LinkKit.LinkKitState.CONNECTED):
            self.lk.disconnect()
        else:
            print("the link is not connected!!")
    
    def get_state(self):
        return self.lk.check_state() 

    def ready(self):
        if(self.lk.check_state() == linkkit.LinkKit.LinkKitState.CONNECTED):
            self.ready = True
            return True
        else:
            return False

    def begin_property_post(self):
        while(self.ready):
            print("POST ", self.IOT_model.get_property())
            # self.lk.thing_post_property(self.IOT_model.get_property())
            for i in range(100):
                if(self.ready):
                    sleep(self.internal_time / 100.0)
                else:
                    break
    
    