# -*- coding: utf-8 -*-

import scrapy
import re

from ziroom.items import ZiroomItem

class ZiroomSpider(scrapy.Spider):
    name = "Ziroom"
    allowed_domains = ["www.ziroom.com"]
    start_urls = ['http://www.ziroom.com/z/nl/z1-s10%E5%8F%B7%E7%BA%BF-t%E7%9F%A5%E6%98%A5%E8%B7%AF-o1.html',
                  'http://www.ziroom.com/z/nl/z1-o1-s10%E5%8F%B7%E7%BA%BF-t%E8%A5%BF%E5%9C%9F%E5%9F%8E.html',
                  'http://www.ziroom.com/z/nl/z1-o1-s10%E5%8F%B7%E7%BA%BF-t%E7%89%A1%E4%B8%B9%E5%9B%AD.html']

    def parse(self, response):
        for house in response.xpath('//ul[@id="houseList"]/li'):

            priceUnit = house.xpath('.//div[@class="priceDetail"]/p/span/text()').extract()[0]
            if u'天' in priceUnit:
                continue

            item = ZiroomItem()
            item['name'] = house.xpath('.//h3/a/text()').extract()[0]
            item['direction'] = item['name'].split('-')[1]
            item['name'] = item['name'].split('-')[0]
            item['link'] = 'http:'+house.xpath('.//h3/a/@href').extract()[0]
            item['subway'] = house.xpath('.//h4/a/text()').extract()[0].split(' ')[1]
            detail = house.xpath('.//div[@class="detail"]/p[1]/span/text()').extract()
            item['size'] = detail[0].strip().replace('\n', '').replace(' ', '')
            item['height'] = detail[1].strip().split('/')[0]
            item['totalHeight'] = detail[1].strip().split('/')[1].replace(u'层','')
            item['type'] = detail[2].strip()
            distance = house.xpath('.//div[@class="detail"]/p[2]/span/text()').extract()[0]
            item['distance'] = re.findall(u'\d+', distance)[1]
            item['price'] = house.xpath('.//div[@class="priceDetail"]/p/text()').extract()[0].strip().replace(u'￥ ','')
            yield item