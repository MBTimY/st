# conding:utf-8

from tornado import httpclient, gen
import pycurl
import chardet

httpclient.AsyncHTTPClient.configure(
    "tornado.curl_httpclient.CurlAsyncHTTPClient")


def prepare_curl_socks5(curl):
    curl.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5)


class Navigate(object):
    def __init__(self, proxyaddr='', proxyport=None, header={}):
        self.proxy = (proxyaddr, proxyport)
        self.header = header
        # print self.proxy

    @gen.coroutine
    def goforword(self, url):
        client = httpclient.AsyncHTTPClient()
        request = httpclient.HTTPRequest(
            url,
            headers=self.header,
            prepare_curl_callback=prepare_curl_socks5,
            proxy_host=self.proxy[0],
            proxy_port=self.proxy[1])
        try:
            response = yield client.fetch(request)
        except Exception as e:
            print e.message
            raise gen.Return('')

        respEncode = chardet.detect(response.body).get("encoding", "utf-8")
        raise gen.Return(response.body.decode(respEncode, 'ignore'))




@gen.coroutine
def main():
    n = Navigate()
    r = yield n.goforword("http://github.com/")
    print('*' * 30 + "\n")
    print(r)
    print('-' * 30 + "\n")


if __name__ == '__main__':
    import tornado.ioloop
    tornado.ioloop.IOLoop.instance().run_sync(main)
