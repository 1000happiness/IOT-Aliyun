from tornado import ioloop
from tornado import web

class PropertyHandler(web.RequestHandler):
    def initialize(self, IOT_model):
        self.IOT_model = IOT_model

    def post(self):
        device_name = self.get_argument("device_name")  # 获取url的参数值
        value = self.get_attribute("value")
        self.IOT_model.update_property(device_name, value)

class IOT_Localserver:
    #localserver_property
    localserver_property = {}

    #IOT_model
    IOT_model = {}

    def __init__(self, localserver_property, IOT_model):
        self.localserver_property = localserver_property
        self.IOT_model = IOT_model

    def run(self):
        print("The local server is running in %s port" , self.localserver_property["port"])
        app = web.Application([
            (r"/property", PropertyHandler, {"IOT_model": self.IOT_model}),  # 注册路由
        ])
        app.listen(self.localserver_property["port"])
        ioloop.IOLoop.current().start()

    def stop(self):
        ioloop.IOLoop.current().stop()


    
