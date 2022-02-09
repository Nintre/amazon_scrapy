# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import time

import random
import requests
from scrapy import signals


# useful for handling different item types with a single interface
from scrapy.downloadermiddlewares.retry import RetryMiddleware, get_retry_request
from scrapy.exceptions import NotConfigured
from scrapy.utils.response import response_status_message


class AmazonDemoSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class AmazonDemoDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.
        # 头部信息，可以在setting中设置
        # request.headers['user-agent'] = 'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)'

        # 代理ip
        # f = open('/Users/hutaiyi/Desktop/amazon_demo/amazon_demo/proxy_ip.txt', encoding='utf-8')
        # proxy_pool = []
        # while True:
        #     line = f.readline()
        #     if line:
        #         ip = 'http://' + line
        #         proxy_pool.append(ip)
        #     else:
        #         break
        # f.close()
        # ips = random.choice(proxy_pool)
        # print(ips)
        # request.meta['proxy'] = ips

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class AmazonProxyDownloaderMiddlewareMIPU:
    def __init__(self):
        self.url = 'https://proxyapi.mimvp.com/api/fetchsecret?orderid=869070911099100423&result_fields=1,2,3'
        self.proxy_ip = ''
        self.proxy_list = []
        self._get_proxy_ip()

    def _get_proxy_ip(self):
        req = requests.get(self.url)
        content = req.content
        proxy_list_origin = content.decode().split("\n")
        for proxy in proxy_list_origin:
            proxy = proxy.split(',', 1)[0]
            self.proxy_list.append(proxy)
        print(self.proxy_list)

    def process_request(self, spider, request):
        self.proxy_ip = 'http://2d16b65369cc:41dc31a201@' + random.choice(self.proxy_list)
        print(self.proxy_ip)
        request.meta['proxy'] = self.proxy_ip

    def process_response(self, request, response, spider):
        if response.status != 200:
            self.proxy_ip = 'http://2d16b65369cc:41dc31a201@' + random.choice(self.proxy_list)
            print(self.proxy_ip)
            request.meta['proxy'] = self.proxy_ip
            return request
        else:
            return response


class AmazonProxyDownloaderMiddleware:
    def __init__(self):
        self.proxy_url = 'http://webapi.http.zhimacangku.com/getip?num=1&type=2&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions='
        self.proxy_ip = ''
        self._get_proxy_ip()

    def _get_proxy_ip(self):
        res = requests.get(self.proxy_url)
        if res.status_code == 200:
            res = res.json()
            # print(res)
            ip = res['data'][0]['ip']
            port = res['data'][0]['port']
            proxy_ip = 'http://' + ip + ':' + str(port)
            self.proxy_ip = proxy_ip
            return proxy_ip
        else:
            time.sleep(2)
            self._get_proxy_ip()

    def process_request(self, spider, request):
        # proxy_ip = self._get_proxy_ip()
        # print(self.proxy_ip)
        request.meta['proxy'] = self.proxy_ip

    def process_response(self, request, response, spider):
        if response.status != 200:
            time.sleep(2)
            self.proxy_ip = self._get_proxy_ip()
            # print(self.proxy_ip)
            request.meta['proxy'] = self.proxy_ip
            return request
        else:
            return response

    def process_exception(self, request, exception, spider):
        self.proxy_ip = self._get_proxy_ip()
        # print(self.proxy_ip)
        request.meta['proxy'] = self.proxy_ip
        return request


class MyRetryMiddleware(RetryMiddleware):

    def __init__(self, settings):
        super(MyRetryMiddleware, self).__init__(settings)
        self.proxy_url = 'http://http.tiqu.letecs.com/getip3?num=1&type=2&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=&gm=4'

    def _get_proxy_ip(self, request):
        res = requests.get(self.proxy_url)
        if res.status_code == 200:
            res = res.json()
            print(res)
            ip = res['data'][0]['ip']
            port = res['data'][0]['port']
            proxy_ip = 'http://' + ip + ':' + str(port)
            request.meta['proxy'] = proxy_ip
            return proxy_ip
        else:
            time.sleep(1)
            self._get_proxy_ip(request)

    # def process_response(self, request, response, spider):
    #     if request.meta.get('dont_retry', False):
    #         return response
    #     if response.status in self.retry_http_codes:
    #         reason = response_status_message(response.status)
    #         self._get_proxy_ip(request)
    #         time.sleep(1)
    #         return self._retry(request, reason, spider) or response
    #     return response
    #
    # def process_exception(self, request, exception, spider):
    #     if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
    #             and not request.meta.get('dont_retry', False):
    #         self._get_proxy_ip(request)
    #         time.sleep(1)
    #         time.sleep(1)
    #         return self._retry(request, exception, spider)

    # def record_failed(self, path, request, exception, failed_meta):
    #     retries = request.meta.get('retry_times', 0) + 1
    #     print('retries time is %s %d' % (retries, retries))
    #     print('max_retry_times is %d' % self.max_retry_times)
    #     if retries > self.max_retry_times:
    #         failed_list = request.meta.get(failed_meta, [])
    #         failed_list = [x.strip() for x in failed_list]
    #         print('recording failed list %s' % '\t'.join(failed_list))
    #         of = open(path, 'a')
    #         of.write('%s\n' % '\t'.join(failed_list))
    #         of.close()

    def process_exception(self, request, exception, spider):
        to_return = RetryMiddleware.process_exception(self, request, exception, spider)
        retries = request.meta.get('retry_times', 0) + 1
        print('retries time is %s %d' % (retries, retries))
        print('max_retry_times is %d' % self.max_retry_times)
        if retries > self.max_retry_times:
            request.meta['url'] = request.url
            self._get_proxy_ip(request)
        # customize retry middleware by modifying this

        return to_return




# import base64
# from urllib.parse import unquote, urlunparse
# from urllib.request import getproxies, proxy_bypass
#
# from scrapy.exceptions import NotConfigured
# from scrapy.utils.httpobj import urlparse_cached
# from scrapy.utils.python import to_bytes
#
# class HttpProxyMiddleware:
#
#     def __init__(self, auth_encoding='latin-1'):
#         # 暂时不需要认证的形式
#         # self.auth_encoding = auth_encoding
#         self.proxies = {}
#         for type_, url in getproxies().items():
#             try:
#                 self.proxies[type_] = self._get_proxy(url, type_)
#             # some values such as '/var/run/docker.sock' can't be parsed
#             # by _parse_proxy and as such should be skipped
#             except ValueError:
#                 continue
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         if not crawler.settings.getbool('HTTPPROXY_ENABLED'):
#             raise NotConfigured
#         auth_encoding = crawler.settings.get('HTTPPROXY_AUTH_ENCODING')
#         return cls(auth_encoding)
#
#     def _basic_auth_header(self, username, password):
#         user_pass = to_bytes(
#             f'{unquote(username)}:{unquote(password)}',
#             encoding=self.auth_encoding)
#         return base64.b64encode(user_pass)
#
#     def _get_proxy(self, url, orig_type):
#         proxy_type, user, password, hostport = self._parse_proxy(url)
#         proxy_url = urlunparse((proxy_type or orig_type, hostport, '', '', '', ''))
#
#         if user:
#             creds = self._basic_auth_header(user, password)
#         else:
#             creds = None
#
#         return creds, proxy_url
#
#     def _parse_proxy(self):
#         proxy_type, user, password, hostport = ''
#         return proxy_type, user, password, hostport
#
#     def process_request(self, request, spider):
#         # ignore if proxy is already set
#         if 'proxy' in request.meta:
#             if request.meta['proxy'] is None:
#                 return
#             # extract credentials if present
#             creds, proxy_url = self._get_proxy(request.meta['proxy'], '')
#             request.meta['proxy'] = proxy_url
#             if creds and not request.headers.get('Proxy-Authorization'):
#                 request.headers['Proxy-Authorization'] = b'Basic ' + creds
#             return
#         elif not self.proxies:
#             return
#
#         parsed = urlparse_cached(request)
#         scheme = parsed.scheme
#
#         # 'no_proxy' is only supported by http schemes
#         if scheme in ('http', 'https') and proxy_bypass(parsed.hostname):
#             return
#
#         if scheme in self.proxies:
#             self._set_proxy(request, scheme)
#
#     def _set_proxy(self, request, scheme):
#         creds, proxy = self.proxies[scheme]
#         request.meta['proxy'] = proxy
#         if creds:
#             request.headers['Proxy-Authorization'] = b'Basic ' + creds
