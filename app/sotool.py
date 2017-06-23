# coding:utf-8

from os import path
import tornado.web
import tornado.ioloop
from tornado import httpclient
import config
import motor
from handlers import MainHandler, TORRHandler, PICHandler, TRANSHandler

db = motor.motor_tornado.MotorClient(config.MGO_CONN)[config.MGO_DB]
application = tornado.web.Application(
    [
        (r"/", MainHandler),
        (r'/searchTORR', TORRHandler),
        (r'/searchPIC', PICHandler),
        (r'/translink', TRANSHandler)
    ],
    debug=config.DEBUG,
    static_path=path.join(path.dirname(path.abspath(__file__)), 'static'),
    template_path=path.join(path.dirname(path.abspath(__file__)), 'templates'),
    cookie_secret=config.COOKIE_SECRET,
    xsrf_cookies=config.XSRF,
    db=db
)

if __name__ == "__main__":
    application.listen(config.LISTEN_PORT)
    tornado.ioloop.IOLoop.instance().start()
