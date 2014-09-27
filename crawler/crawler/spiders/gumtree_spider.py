# -*- coding: utf-8 -*-

import datetime
import pytz
import scrapy

from scrapy.exceptions import CloseSpider
from scrapy.http import Request
from scrapy.xlib.pydispatch import dispatcher

from crawler import settings

from crawler.exceptions import OldItemException
from crawler.items import CrawlerItem


def handle_old_item(item, response, exception, spider):
    if isinstance(exception, OldItemException):
        spider.old_item_reached = True


class GumtreeSpider(scrapy.Spider):
    name = 'gumtree'
    allowed_domains = ['www.gumtree.pl']
    start_urls = [
        'http://www.gumtree.pl/fp-parking-i-garaz/warszawa/c9071l3200008?AdType=2&maxPrice=1000',
    ]

    def __init__(self, *args, **kwargs):
        super(GumtreeSpider, self).__init__(*args, **kwargs)
        self.old_item_reached = False
        self._set_date_limit()

    def parse(self, response):
        for sel in response.xpath('//tr[re:test(@id, "resultRow\d")]'):
            if self.old_item_reached:
                raise CloseSpider('Reached too old item')

            left_element = sel.xpath('td[1]')
            mid_element = sel.xpath('td[2]')
            right_element = sel.xpath('td[3]')
            item = CrawlerItem()
            non_image_left = left_element.xpath('div[@class="ar-text-wrap clearfix"]')
            item['title'] = non_image_left.xpath('div[@class="ar-title"]/a/text()').extract()
            item['link'] = non_image_left.xpath('div[@class="ar-title"]/a/@href').extract()
            item['desc'] = non_image_left.xpath('div[@class="ar-descr"]/span/text()').extract()
            item['price'] = mid_element.xpath('div[@class="ar-price"]/strong/text()').extract()
            item['time_posted'] = right_element.xpath('div/div/div[@class="ar-date"]/ul/li[2]/text()').extract()
            item['source'] = ['gumtree']
            yield item

        for items_page_link in response.xpath('//a[@class="prevNextLink"]'):
            try:
                link_text = items_page_link.xpath('text()').extract()[0]
            except IndexError:
                print 'WARNING: missing text in items_page_link on page %s' % response.url
            else:
                if link_text.startswith(u'Następne'):
                    url = items_page_link.xpath('@href').extract()[0]
                    yield Request(url, callback=self.parse)

    def _set_date_limit(self):
        try:
            newest_item = CrawlerItem.django_model.objects.filter(source=self.name).order_by('-time_posted')[0]
            self.date_limit = newest_item.time_posted - datetime.timedelta(minutes=settings.CRAWLING_MINUTE_MARGIN)
        except IndexError:
            timezone = pytz.timezone(settings.TIMEZONE)
            now = datetime.datetime.now(timezone)
            self.date_limit = now - datetime.timedelta(hours=settings.DEFAULT_RESULT_HOURS_LIMIT)

        print 'New crawling will start for items laster than %s' % self.date_limit

    def get_date_limit(self):
        return self.date_limit

    dispatcher.connect(handle_old_item, scrapy.signals.item_dropped)
