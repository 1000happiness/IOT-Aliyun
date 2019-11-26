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

        self.lk.thing_setup()
        
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
        retry_count = 1
        while(self.ready):
            if(self.lk.check_state() == linkkit.LinkKit.LinkKitState.CONNECTED):
                # send property
                retry_count = 1
                rc, request_id = self.lk.thing_post_property(self.IOT_model.get_property())
                if(rc == 0):
                    print("SEND ", self.IOT_model.get_property(), " SUCCESS")
                else:
                    print("SEND FAIL")
                for i in range(self.internal_time):
                    if(self.ready):
                        if(not self.IOT_model.get_update_flag()):
                            sleep(1)
                        else:
                            self.IOT_model.set_update_flag(False)
                            break
                    else:
                        break
            else:
                if(retry_count < 10):
                    print("disconnect from aliyun accidently, trying to connect again:", retry_count)
                    if(self.lk.check_state() != linkkit.LinkKit.LinkKitState.CONNECTING):
                        self.lk.connect_async()
                    retry_count = retry_count + 1
                    sleep(pow(2,retry_count))
                else:
                    print("disconnect from aliyun accidently, the programme can not connect again")
                    break

            if(self.lk.check_state() == linkkit.LinkKit.LinkKitState.CONNECTED):
                # send picture
                picture = self.IOT_model.get_picture()
                if(picture != ""):
                    rc, request_id = self.lk.publish_topic(self.lk.to_full_topic("user/picture"), picture)
                    if(rc == 0):
                        print("SEND PICTURE SUCCESS")
                        self.IOT_model.set_picture_direct("")
                        # print(self.IOT_model.get_picture())
                    else:
                        print("SEND FAIL")
            else:
                if(retry_count < 10):
                    print("disconnect from aliyun accidently, trying to connect again:", retry_count)
                    if(self.lk.check_state() != linkkit.LinkKit.LinkKitState.CONNECTING):
                        self.lk.connect_async()
                    retry_count = retry_count + 1
                    sleep(pow(2,retry_count))
                else:
                    print("disconnect from aliyun accidently, the programme can not connect again")
                    break
            
    