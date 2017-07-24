# coding:utf-8
from lxml import etree
import json
import base64
from tornado import gen
from common.navigate import Navigate
import config


# TODO把标题和pagination处理好, 组合成json就可以返回了
# 把传过来的google搜索的结果进行处理, 然后json结构返回到调用方, 返回的json结构中含有原始网页中的linker都被base64编码过了
def ggpicWrapper(html_content, cblinker):
    urlbase = "https://www.google.com"
    try:
        html = etree.HTML(html_content)
        titles = [(e.text.strip(), e.attrib['href'])
                  for e in html.xpath('//h3[@class="r"]/a')
                  if e.attrib['href'].startswith("http")]
        paginations = [
            (e.find('span').tail,
             (cblinker % (base64.b64encode(urlbase + e.attrib["href"]),
                          'ggpic')))
            for e in html.xpath('//div[@id="navcnt"]//a[@class="fl"]')
        ]
    except Exception as e:
        print(__name__ + e.message)
        return {}

    return json.dumps({'titles': titles, "paginations": paginations})


# TODO编写bt搜索网站的wrapper
# 这个函数的调用者需要包装在tornado.gen.coroutine里面, 然后使用yield来操作, 主要是因为这里我使用了异步请求
@gen.coroutine
def btsoWrapper(html_content, cblinker):
    urlbase = "https://btso.pw"
    html = etree.HTML(html_content)
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
    linkers = [e for e in html.xpath('//div[@class="data-list"]//a/@href')]
    torrents = []
    for l in linkers:
        hc = yield navi.goforword(l)
        if hc == '':
            continue
        h = etree.HTML(hc)
        name = h.xpath('//div[@class="container"]//h3[1]')[0].text
        magnetl = h.xpath(
            '//div[@class="container"]//textarea[@id="magnetLink"]')[0].text
        torrents.append({'name': name, 'magnet': magnetl})
    paginations = [
        (e.text, cblinker % (base64.b64encode(urlbase + e.attrib["href"]),
                             'btso'))
        for e in html.xpath(
            '//ul[@class="pagination pagination-lg"]/li/a[@name="numbar"]')
    ]
    raise gen.Return(
        json.dumps({
            'torrents': torrents,
            'paginations': paginations
        }))


WRAPPER = {'ggpic': ggpicWrapper, 'btso': btsoWrapper}


def GenWrapper(name):
    return WRAPPER.get(name, False)


@gen.coroutine
def main():
    navi = Navigate()
    html_content = yield navi.goforword('https://xxx.xx/xxxxx/xxx')
    if html_content == '':
        print('connect failed!')
        return
    r = btsoWrapper(html_content, 'http://127.0.0.1/trans?r=%s&m=%s')
    import tornado
    if isinstance(r, tornado.concurrent.Future):
        content = yield r
    import codecs
    with codecs.open('finnal', 'w', encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    from tornado import ioloop
    ioloop.IOLoop.current().run_sync(main)
