# coding:utf-8

from os import path
import tornado.web
import tornado.ioloop
from tornado import httpclient
import config
from handlers import MainHandler, TORRHandler, PICHandler, TRANSHandler


application = tornado.web.Application(
    [
        (r"/", MainHandler),
        (r'/searchTORR', TORRHandler),
        (r'/searchPIC', PICHandler),
        (r'/translink', TRANSHandler)
    ],
    debug=config.DEBUG,
    static_path=path.join(path.dirname(path.abspath(__file__)), 'static'),
    template_path='templates',
    cookie_secret=config.COOKIE_SECRET,
    xsrf_cookies=config.XSRF
)

if __name__ == "__main__":
    httpclient.AsyncHTTPClient.configure(
        "tornado.curl_httpclient.CurlAsyncHTTPClient")
    application.listen(config.LISTEN_PORT)
    tornado.ioloop.IOLoop.instance().start()
