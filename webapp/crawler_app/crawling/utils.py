import os
import subprocess


from crawling.exceptions import UnknownCrawler
from crawler_app.settings import SCRAPY_DIR, CRAWLERS


def crawl(source):
    if source not in CRAWLERS:
        raise UnknownCrawler('Passed unknown crawler %s' % source)

    os.chdir(SCRAPY_DIR)
    subprocess.call(['scrapy', 'crawl', source])


def crawl_all():
    for source in CRAWLERS:
        crawl(source)
