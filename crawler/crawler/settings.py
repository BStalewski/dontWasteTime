# -*- coding: utf-8 -*-

import os.path
import sys

from os.path import abspath, dirname, join

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
    'crawler.pipelines.LinkUniquenessValidatorPipeline': 60,
    'crawler.pipelines.DBPipeline': 1000,
}

LOG_LEVEL = 'INFO'


MIN_DESCRIPTION_RANKING = -3
DEFAULT_RESULT_HOURS_LIMIT = 72
CRAWLING_MINUTE_MARGIN = 560

TIMEZONE = 'Europe/Warsaw'


ROOT_PROJECT_DIR = dirname(dirname(dirname(abspath(__file__))))
DJANGO_DIR = join(ROOT_PROJECT_DIR, 'webapp', 'crawler_app')

sys.path.append(DJANGO_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'crawler_app.settings'

# it is needed to be able to use operations (e.g. filtering) on django models
import django
django.setup()
