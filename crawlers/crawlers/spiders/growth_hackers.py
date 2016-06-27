# coding=utf8
from __future__ import absolute_import

import logging
import time
import scrapy
from scrapy import signals


logger = logging.getLogger()


class GrowingSpider(scrapy.Spider):
    name = "gh"
    allowed_domains = ["growthhackers.com"]
    start_urls = [
        "http://growthhackers.com/page/1"
    ]

    def __init__(self):
        self.host = "http://growthhackers.com"

    def parse(self, response):
        links = response.xpath('//div[@class="post-content"]/h3/a')
        for i in links:
            item = {
                'title': i.xpath("text()").extract()[0],
                'href': "{}{}".format(self.host, i.xpath("@href").extract()[0]),
                'read': False,
                'visit5w333333': False,
            }
            yield item

        time.sleep(1)
        next_page = response.xpath('//a[@rel="next"]')
        if next_page:
            url = "{}{}".format(self.host, next_page.xpath("@href").extract()[0])
            logger.info("get {} ...".format(url))
            yield scrapy.Request(url=url, callback=self.parse)
