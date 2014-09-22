# -*- coding: utf-8 -*-

# Scrapy settings for crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crawler (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    'crawler.pipelines.PaidLinksFilterPipeline': 10,
    'crawler.pipelines.ListsToValuesPipeline': 20,
    'crawler.pipelines.PriceFormatPipeline': 30,
    'crawler.pipelines.PriceValidatorPipeline': 31,
    'crawler.pipelines.DateFormatPipeline': 40,
    'crawler.pipelines.DateValidatorPipeline': 41,
    'crawler.pipelines.DescriptionValidatorPipeline': 50,
    'crawler.pipelines.DBPipeline': 1000,
}

LOG_LEVEL = 'INFO'


MIN_DESCRIPTION_RANKING = -3


import sys
sys.path.append('/home/bartek/projects/dontWasteTime/webapp/crawler_app')

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'crawler_app.settings'
