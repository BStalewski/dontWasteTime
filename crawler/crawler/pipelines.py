# -*- coding: utf-8 -*-
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import datetime
import pytz
import re

from scrapy.exceptions import DropItem

from crawler.items import CrawlerItem


class PaidLinksFilterPipeline(object):
    def process_item(self, item, spider):
        if not item['time_posted'] or not item['price']:
            raise DropItem('PaidLinksFilterPipeline: paid link found with title: %s' % item['title'])
        else:
            return item


class ListsToValuesPipeline(object):
    def process_item(self, item, spider):
        cleaned_item = CrawlerItem()
        for key in item.keys():
            if len(item[key]) != 1:
                raise DropItem('ListsToValuesPipeline: field %s with %d elements in item with title: %s' %
                               (key, len(item[key]), item['title']))
            cleaned_item[key] = item[key][0]

        return cleaned_item


class PriceFormatPipeline(object):
    def process_item(self, item, spider):
        prices = re.findall('(\d+)', item['price'])
        if len(prices) != 1:
            raise DropItem('PricePipeline: %d occurences of price (price string %s) for item with title: %s' %
                           (len(prices), item['price'], item['title']))

        item['price'] = prices[0]
        return item


class PriceValidatorPipeline(object):
    def process_item(self, item, spider):
        price = item['price']
        try:
            item['price'] = int(price)
        except ValueError:
            raise DropItem('PriceValidatorPipeline: non-integer price %d for item with title: %s' %
                           (price, item['title']))

        if item['price'] == 0:
            raise DropItem('PriceValidatorPipeline: 0 price for item with title: %s' % item['title'])

        return item


class DateFormatPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'gumtree':
            processed_item = self.process_gumtree_item(item)

        return processed_item

    def process_gumtree_item(self, item):
        crawl_date = item['time_posted']
        no_whitespaces_crawl_date = crawl_date.strip()
        recent_date_match = re.match(r'< (\d+) godz. temu|< (\d+) min temu', no_whitespaces_crawl_date)
        timezone = pytz.timezone('Europe/Warsaw')
        if recent_date_match:
            if recent_date_match.group(1):
                hours_alive = int(recent_date_match.group(1))
                minutes_alive = 0
            else:
                hours_alive = 0
                minutes_alive = int(recent_date_match.group(2))
            now = datetime.datetime.now(timezone)
            time_posted = now - datetime.timedelta(hours=hours_alive, minutes=minutes_alive)
            item['time_posted'] = time_posted
        else:
            day, month, year = [int(date_part) for date_part in no_whitespaces_crawl_date.split('/')]
            item['time_posted'] = datetime.datetime(year, month, day, tzinfo=timezone)

        return item
