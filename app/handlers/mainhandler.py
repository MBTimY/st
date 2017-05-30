# coding:utf-8

import tornado.web


#   TODO首页的路由handler, 返回给用户的是一个html页面
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')
