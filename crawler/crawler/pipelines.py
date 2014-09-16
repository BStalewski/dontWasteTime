# -*- coding: utf-8 -*-
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re

from scrapy.exceptions import DropItem

from crawler.items import CrawlerItem


class PaidLinksFilterPipeline(object):
    def process_item(self, item, spider):
        if not item['added'] or not item['price']:
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
