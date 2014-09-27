# -*- coding: utf-8 -*-

import datetime
import pytz
import re

import crawler.exceptions as exc
from crawler.items import CrawlerItem, CrawlerResult
from crawler import settings


class PaidLinksFilterPipeline(object):
    def process_item(self, item, spider):
        if not item['time_posted'] or not item['price']:
            raise exc.PaidLinkException('Paid link found with title: %s' % item['title'])
        else:
            return item


class ListsToValuesPipeline(object):
    def process_item(self, item, spider):
        cleaned_item = CrawlerItem()
        for key in item.keys():
            if len(item[key]) != 1:
                raise exc.IncorrectFormatException('Field %s with %d elements in item with title: %s' %
                                                   (key, len(item[key]), item['title']))
            cleaned_item[key] = item[key][0]

        return cleaned_item


class PriceFormatPipeline(object):
    def process_item(self, item, spider):
        prices = re.findall('(\d+)', item['price'])
        if len(prices) != 1:
            raise exc.IncorrectPriceException('%d occurences of price (price string %s) for item with title: %s' %
                                              (len(prices), item['price'], item['title']))

        item['price'] = prices[0]
        return item


class PriceValidatorPipeline(object):
    def process_item(self, item, spider):
        price = item['price']
        try:
            item['price'] = int(price)
        except ValueError:
            raise exc.InvalidPriceException('non-integer price %d for item with title: %s' %
                                            (price, item['title']))

        if item['price'] == 0:
            raise exc.InvalidPriceException('0 price for item with title: %s' % item['title'])

        return item


class DateFormatPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'gumtree':
            processed_item = self.process_gumtree_item(item)
        elif spider.name == 'otodom':
            processed_item = self.process_otodom_item(item)
        else:
            raise exc.UnknownSpiderException('Unknown spider: %s' % spider.name)

        return processed_item

    def process_gumtree_item(self, item):
        crawl_date = item['time_posted']
        no_whitespaces_crawl_date = crawl_date.strip()
        recent_date_match = re.match(r'< (\d+) godz. temu|< (\d+) min temu', no_whitespaces_crawl_date)
        timezone = pytz.timezone(settings.TIMEZONE)
        if recent_date_match:
            if recent_date_match.group(1):
                hours_alive = int(recent_date_match.group(1))
                minutes_alive = 0
            else:
                hours_alive = 0
                minutes_alive = int(recent_date_match.group(2))
            now = datetime.datetime.now()
            naive_datetime = now - datetime.timedelta(hours=hours_alive, minutes=minutes_alive)
        else:
            day, month, year = [int(date_part) for date_part in no_whitespaces_crawl_date.split('/')]
            naive_datetime = datetime.datetime(year, month, day)

        local_datetime = timezone.localize(naive_datetime)
        item['time_posted'] = local_datetime

        return item

    def process_otodom_item(self, item):
        crawl_date = item['time_posted']
        timezone = pytz.timezone(settings.TIMEZONE)
        naive_datetime = datetime.datetime.strptime(crawl_date, '%d.%m.%Y')
        local_datetime = timezone.localize(naive_datetime)
        item['time_posted'] = local_datetime
        return item


class DateValidatorPipeline(object):
    def process_item(self, item, spider):
        date_limit = spider.get_date_limit()
        if item['time_posted'] < date_limit:
            raise exc.OldItemException('Reached too old item')

        return item


class DescriptionValidatorPipeline(object):
    elements = [
        (u'.*\d+m2', 1), (u'.*wolnostojący', 2), (u'.*murowany', 2), (u'.*światło', 3),
        (u'.*prąd', 3), (u'.*elektryczna', 3), (u'.*gniazdko', 3),

        (u'.*apartamen', -1), (u'.*podziemny', -1), (u'.*parking', -2), (u'.*miejsce postojowe', -3),
        (u'.*miejsce garażowe', -3), (u'.*przezim', -3), (u'.*w garażu podziemnym', -3),
    ]

    def process_item(self, item, spider):
        desc = item['desc']
        matching_elements_ranks = [rank for (regex, rank) in self.elements if re.match(regex, desc, re.IGNORECASE)]
        ranking = sum(matching_elements_ranks)
        if ranking < settings.MIN_DESCRIPTION_RANKING:
            raise exc.NotinterestingItemException('Item not interesting')

        return item


class LinkFormatPipeline(object):
    def process_item(self, item, spider):
        if item['link'].startswith('http://') or item['link'].startswith('www.'):
            return item
        else:
            base_url = spider.allowed_domains[0].rstrip('/')
            path = item['link'].lstrip('/')
            item['link'] = '%s/%s' % (base_url, path)
            return item


class LinkUniquenessValidatorPipeline(object):
    def process_item(self, item, spider):
        if CrawlerResult.objects.filter(link=item['link']).exists():
            raise exc.AlreadyCrawledException('Item already crawled')

        return item


class DBPipeline(object):
    def process_item(self, item, spider):
        item.save()
        return item
