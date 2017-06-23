# coding:utf-8
import tornado.web
import sys
sys.path.append('..')

from wrapper import btsoWrapper
from common.navigate import Navigate
import config
from tornado import gen
import re


# TODO首页的路由handler, 返回给前端调用一个json结构
# 这个handler拿来处理种子文件的搜索
class TORRHandler(tornado.web.RequestHandler):
    def NotFound(self):
        self.clear()
        self.set_status(404)
        self.finish('<html><p>Not found anyting!</p></html>')
        return

    @gen.coroutine
    def get(self):
        keyword = self.get_argument('k', '')
        pageNum = int(self.get_argument('pn', 1))
        if keyword == '':
            self.finish('argument input error!')
            return

        show_limit = 10
        regx_colname = re.compile(r"btso__\d+_\d+__handledetail")
        # regx_history = re.compile(r"history__y__btso__\d+_\d+")
        db = self.settings['db']
        cols = yield db.collection_names()
        items_matched = []
        total_count = 0
        remain_query = show_limit
        remain_skip = (pageNum - 1) * show_limit
        for col in cols:
            if regx_colname.match(col):
                cur = db[col].find({
                    "$text": {
                        "$search": keyword
                    }
                }, {"title": 1,
                    "magnet": 1,
                    "_id": 0})
                cur.skip(remain_skip)
                cur.limit(remain_query)
                try:
                    count = yield cur.count()
                    total_count += count

                    items = yield cur.to_list(None)
                    items_matched.extend(items)
                    if len(items_matched) >= show_limit:
                        break
                    remain_query = remain_query - len(items_matched)
                    remain_skip = remain_skip - count if remain_skip > count else 0
                except:
                    self.NotFound()
                    return

        if len(items_matched) == 0:
            self.NotFound()
            return

        totalPages = total_count / show_limit
        if total_count % show_limit != 0:
            totalPages += 1

        startPN = 1 if pageNum - 6 < 0 else pageNum - 6 + 1
        if totalPages - (pageNum + 4) > 0 and totalPages > 10:
            if pageNum + 4 <= 10:
                endPN = 10
            else:
                endPN = pageNum + 4
        else:
            endPN = totalPages

        ret_json = {
            "currentPN": pageNum,
            "startPN": startPN,
            "endPN": endPN,
            "list": items_matched,
        }
        self.finish(ret_json)
