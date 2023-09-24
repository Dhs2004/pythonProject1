import scrapy
from BaiduSpider.items import NewsItem
from copy import deepcopy
class NewSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/']
    def parse(self, response):
        news_list = response.xpath('//ul[@class="s-hotsearch-content"]/li')
        for news in news_list:
            item = NewsItem()
            item['index'] = news.xpath('a/span[1]/text()').extract_first()
            item['title'] = news.xpath('a/span[2]/text()').extract_first()
            item['link'] = news.xpath('a/@href').extract_first()
            yield scrapy.Request(
                item['link'],
                callback=self.parse_newsnum,
                meta={'item': deepcopy(item)}
            )
    def parse_newsnum(self, response):
        item = response.meta['item']
        item = response.meta['item']
        item['newsNum'] = response.xpath(
            '//span[@class="nums_text"]/text()').extract_first()
        yield item