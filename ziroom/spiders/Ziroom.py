# -*- coding: utf-8 -*-

import scrapy
import re

from ziroom.items import ZiroomItem

class ZiroomSpider(scrapy.Spider):
    name = "Ziroom"
    allowed_domains = ["www.ziroom.com"]
    start_urls = [u'http://www.ziroom.com/z/nl/z1-s10号线-t苏州街-o2-u1.html',
u'http://www.ziroom.com/z/nl/z1-s10号线-t海淀黄庄-o2-u1.html',
u'http://www.ziroom.com/z/nl/z1-s10号线-t知春里-o2-u1.html',
u'http://www.ziroom.com/z/nl/z1-s10号线-t知春路-o2-u1.html',
u'http://www.ziroom.com/z/nl/z1-s10号线-t西土城-o2-u1.html',
u'http://www.ziroom.com/z/nl/z1-s10号线-t牡丹园-o2-u1.html',
u'http://www.ziroom.com/z/nl/z1-s10号线-t北土城-o2-u1.html',
u'http://www.ziroom.com/z/nl/z1-s10号线-t安贞门-o2-u1.html',
u'http://www.ziroom.com/z/nl/z1-s10号线-t惠新西街南口-o2-u1.html',
u'http://www.ziroom.com/z/nl/z1-s10号线-t芍药居-o2-u1.html',
u'http://www.ziroom.com/z/nl/z1-s10号线-t太阳宫-o2-u1.html']

    def parse(self, response):
        for house in response.xpath('//ul[@id="houseList"]/li'):

            distance = house.xpath('.//div[@class="detail"]/p[2]/span/text()').extract()[0]
            distance = re.findall(u'\d+', distance)[1]
            distance_value = int(distance)

            if distance_value > 1000:
                continue

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
            item['distance'] = distance
            item['price'] = house.xpath('.//div[@class="priceDetail"]/p/text()').extract()[0].strip().replace(u'￥ ','')
            item['image'] = '=image("http:'+house.xpath('./div[1]/a/img/@_webpsrc').extract()[0]+'")'

            yield item