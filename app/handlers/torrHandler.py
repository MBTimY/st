# coding:utf-8

import tornado.web
import sys
sys.path.append('..')
from wrapper import btsoWrapper
from common.navigate import Navigate
import config
from tornado import gen


# TODO首页的路由handler, 返回给前端调用一个json结构
# 这个handler拿来处理种子文件的搜索
class TORRHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        keyword = self.get_argument('k', '')
        if keyword == '':
            self.finish('argument input error!')
            return

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
        html_content = yield navi.goforword('https://btso.pw/search/' + keyword)
        if html_content == '':
            self.clear()
            self.set_status(404)
            self.finish('<html><p>Not found anyting!</p></html>')
            return
        ret_json = yield btsoWrapper(html_content, config.CB_LINKER)
        self.finish(ret_json)
