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


class OtodomSpider(scrapy.Spider):
    name = 'otodom'
    allowed_domains = ['www.otodom.pl']
    start_urls = [
        'http://otodom.pl/index.php?mod=listing&source=context&objSearchQuery.OfferType=rent&objSearchQuery.ObjectName=Garage&objSearchQuery.Country.ID=1&objSearchQuery.Province.ID=7&objSearchQuery.District.ID=197&objSearchQuery.CityName=Warszawa&objSearchQuery.Distance=0&objSearchQuery.QuarterName=&objSearchQuery.StreetName=&objSearchQuery.LatFrom=0&objSearchQuery.LatTo=0&objSearchQuery.LngFrom=0&objSearchQuery.LngTo=0&objSearchQuery.PriceFrom=&objSearchQuery.PriceTo=1+000&objSearchQuery.PriceCurrency.ID=1&objSearchQuery.AreaFrom=&objSearchQuery.AreaTo=&objSearchQuery.CreationDate=&objSearchQuery.Description=&objSearchQuery.offerId=&objSearchQuery.Orderby=default&resultsPerPage=100&Search=Search&Location=',
    ]

    def __init__(self, *args, **kwargs):
        super(OtodomSpider, self).__init__(*args, **kwargs)
        self.old_item_reached = False
        self._set_date_limit()

    def parse(self, response):
        for sel in response.xpath('//article[@class="od-listing_item  "]'):
            if self.old_item_reached:
                raise CloseSpider('Reached too old item')

            title_element = sel.xpath('div[1]/h1/a')
            data_element = sel.xpath('div[3]')
            time_element = sel.xpath('a/p[@class="od-listing_item-date_icons"]/time')
            item = CrawlerItem()
            item['title'] = title_element.xpath('text()').extract()
            item['link'] = title_element.xpath('@href').extract()
            item['desc'] = data_element.xpath('a/p[@class="od-listing_item-summary"]/text()').extract()
            item['price'] = data_element.xpath('div[@class="od-listing_item-numbers"]/strong[@class="od-listing_item-price"]/text()').extract()
            item['time_posted'] = time_element.xpath('text()').extract()
            item['source'] = ['otodom']

            yield item

        for items_page_link in response.xpath('//div[@class="od-pagination"]/a'):
            try:
                link_text = items_page_link.xpath('span[@class="od-icon-label"]/text()').extract()[0]
            except IndexError:
                # this is link in the upper part of page
                pass

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
