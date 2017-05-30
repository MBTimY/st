# coding:utf-8

import tornado.web
from tornado import gen
import os
import sys
import random
import string
import urlparse
sys.path.append('..')
from wrapper import ggpicWrapper
from common.navigate import Navigate
import config


# 此路由接收的参数为imgurl, 或者如果使用post提交,那么接收一个图片资源
class PICHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        imgurl = self.get_argument('imgurl', '')
        if imgurl == '':
            self.write("sorry, argument input error!")
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
        google_img_search_url = 'https://www.google.com/searchbyimage?image_url=' + imgurl
        nav = Navigate(config.SPROXY_ADDR, config.SPROXY_PORT, header)
        html_content = yield nav.goforword(google_img_search_url)
        if html_content == '':
            self.clear()
            self.set_status(404)
            self.finish('not found anyting!')
            return
        ret_json = ggpicWrapper(html_content, config.CB_LINKER)
        self.finish(ret_json)

    @gen.coroutine
    def post(self):
        try:
            file1 = self.request.files[0]
            original_fname = file1['filename']
            extension = os.path.splitext(original_fname)[1]
            fname = ''.join(
                random.choice(string.ascii_lowercase + string.digits)
                for x in range(6))
            final_filename = fname + extension
            with open(
                    os.path.join(config.WORK_DIR + "static/uploads/") +
                    final_filename, 'w') as output_file:
                output_file.write(file1['body'])
            imgurl = urlparse.urljoin(config.DOMAIN_BASE + '',
                                    '/static/uploads/' + final_filename)

            nav = Navigate(config.SPROXY_ADDR, config.SPROXY_PORT)
            google_img_search_url = 'https://www.google.com/searchbyimage?image_url=' + imgurl
            html_content = yield nav.goforword(google_img_search_url)
            ret_json = ggpicWrapper(html_content, config.CB_LINKER)
            self.finish(ret_json)
        except Exception as e:
            print e.message
            self.finish({})
