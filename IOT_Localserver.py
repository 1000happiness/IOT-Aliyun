from tornado import ioloop
from tornado import web
from json import loads

class PropertyHandler(web.RequestHandler):
    def initialize(self, IOT_model):
        self.IOT_model = IOT_model

    def post(self):
        print(self.request.body.decode("utf-8"))
        args = loads(self.request.body.decode("utf-8"))
        print("body: ")
        print(args)

        self.IOT_model.update_property(args["device_name"], args["value"])

        print(self.IOT_model.get_property())
        self.write("{\"success\": true}")

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


    
