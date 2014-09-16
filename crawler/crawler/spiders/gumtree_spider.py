import scrapy

from crawler.items import CrawlerItem


class GumtreeSpider(scrapy.Spider):
    name = "gumtree"
    allowed_domains = ["www.gumtree.pl"]
    start_urls = [
        "http://www.gumtree.pl/fp-parking-i-garaz/warszawa/c9071l3200008?AdType=2&maxPrice=1000&minPrice=",
    ]

    def parse(self, response):
        for sel in response.xpath('//tr[re:test(@id, "resultRow\d")]'):
            left_element = sel.xpath('td[1]')
            mid_element = sel.xpath('td[2]')
            right_element = sel.xpath('td[3]')
            item = CrawlerItem()
            non_image_left = left_element.xpath('div[@class="ar-text-wrap clearfix"]')
            item['title'] = non_image_left.xpath('div[@class="ar-title"]/a/text()').extract()
            item['link'] = non_image_left.xpath('div[@class="ar-title"]/a/@href').extract()
            item['desc'] = non_image_left.xpath('div[@class="ar-descr"]/span/text()').extract()
            item['price'] = mid_element.xpath('div[@class="ar-price"]/strong/text()').extract()
            item['added'] = right_element.xpath('div/div/div[@class="ar-date"]/ul/li[2]/text()').extract()
            yield item
