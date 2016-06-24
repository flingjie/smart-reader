# coding=utf8
from __future__ import absolute_import

import logging
import time
import scrapy
from scrapy import signals


logger = logging.getLogger()


class GrowingSpider(scrapy.Spider):
    name = "gh"
    allowed_domains = ["growthhackers.com/"]
    start_urls = [
        "http://growthhackers.com/page/1"
    ]

    def __init__(self):
        self.host = "http://growthhackers.com"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(GrowingSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        pass

    def parse(self, response):
        links = response.xpath('//div[@class="post-content"]/h3/a')
        for i in links:
            item = {
                'title': i.xpath("text()").extract(),
                'href': "{}{}".format(self.host, i.xpath("@href").extract()),
                'read': False
            }
            yield item

        time.sleep(1)
        next = response.xpath('//a[@rel="next"]')
        if next:
            url = "{}{}".format(self.host, next.xpath("@href").extract())
            logger.info("get {} ...".format(url))
            yield scrapy.Request(url=url, callback=self.parse)
