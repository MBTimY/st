# coding:utf-8
import tornado.concurrent as concurrent
import tornado.web
from tornado import gen
import sys
sys.path.append('..')
import wrapper
from common.navigate import Navigate
import config
import base64

# TODO这个作为一个被wrapper调用的路由, 主要是拿来重新访问我们的包装网页的
# 这个handler是wrapper的回调link
class TRANSHandler(tornado.web.RequestHandler):
    
    @gen.coroutine
    def get(self):
        redirect = self.get_argument('r', '')
        method_name = self.get_argument('m', '')
        if redirect == '' and method_name == '':
            self.finish('error input!')
            return
        wp = wrapper.GenWrapper(method_name)
        header = {
            "accept":
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "accept-encoding":
            "gzip, deflate, sdch, br",
            "accept-language":
            "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
            "cache-control":
            "no-cache",
            "user-agent":
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }

        navi = Navigate(config.SPROXY_ADDR, config.SPROXY_PORT, header)
        url = base64.b64decode(redirect)
        html_content = yield navi.goforword(url)
        if html_content == '':
            self.clear()
            self.set_status(404)
            self.finish('<html><p>website request failed!</p></html>')
            return
        r = wp(html_content, config.CB_LINKER)
        if isinstance(r, concurrent.Future):
            ret = yield r
        else:
            ret = r
        self.finish(ret)
