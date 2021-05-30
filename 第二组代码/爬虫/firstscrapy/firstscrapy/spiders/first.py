#import scrapy

from firstscrapy.items import FirstscrapyItem
#
# class FirstSpider(scrapy.Spider):
#     name = 'first'
#     #allowed_domains = ['https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd=%E5%8D%9A%E7%89%A9%E9%A6%86&medium=0']
#     baseurl='https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd=%E5%8D%9A%E7%89%A9%E9%A6%86&medium=0&x_bfe_rqs=03E80&x_bfe_tjscore=0.100000&tngroupname=organic_news&newVideo=12&rsv_dl=news_b_pn&pn='
#     # 第1页为小于10的数字 10为第2页，20为第三页，30为第四页，以此类推
#     for i in range(10, 50, 10):
#          # 点击界面第二页可以看到网页变化截取关键部分 https://www.baidu.com/s?wd=python&pn=10
#          start_urls = [baseurl+str(i)]
#     #start_urls = ['https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd=%E5%8D%9A%E7%89%A9%E9%A6%86&medium=0']
#
#     def parse(self, response):
#         div_list = response.xpath('//div[@class="result-op c-container xpath-log new-pmd"]')
#         #print(div_list)
#         for div in div_list:
#             title = div.xpath('.//h3/a/text()').getall()
#             title = "".join(title)
#             print(title)
#
#             #创建item对象
#             item = FirstscrapyItem()
#             item['title'] = title
#
#             #返回item给pipelines
#             yield item
#


# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider,Request
import re
import datetime
import time
from _datetime import timedelta

#URL = 'https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&rsv_dl=ns_pc&word={museum}&bt={bt}&et={et}&x_bfe_rqs=03E80&x_bfe_tjscore=0.100000&tngroupname=organic_news&newVideo=12&pn={page}'
URL = 'https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd={museum}&medium=2&x_bfe_rqs=03E80&x_bfe_tjscore=0.100000&tngroupname=organic_news&newVideo=12&rsv_dl=news_b_pn&pn={page}'
class FirstSpider(scrapy.Spider):
    name = 'first'
    #allowed_domains = ['baidu.com']
    page = 0
    museum = None
    startTime = None
    endTime = None
    start_urls = []
    end = False

    def __init__(self, museum="博物馆", startTime="2020-01-01", endTime=datetime.datetime.now().strftime("%Y-%m-%d"), *args, **kwargs):
        super(FirstSpider, self).__init__(*args, **kwargs)
        self.startTime = startTime
        self.endTime = endTime
        self.museum = museum
        self.start_urls = [URL.format(museum=museum, page=self.page * 10)]

    def parse(self, response):
        flag = 0
        div_list = response.xpath('//div[@class="result-op c-container xpath-log new-pmd"]')
        if not div_list:
            self.end = True
            return
        for div in div_list:
            s_time = div.xpath('.//span[@class ="c-color-gray2 c-font-normal"]/text()').getall()
            s_time = "".join(s_time)
            time = self.parse_time(s_time)
            if time=="":
                continue

            if (time>self.startTime) and (time<self.endTime):
                detail_url = div.xpath('./@mu').getall()
                detail_url = "".join(detail_url)

                title = div.xpath('.//h3/a//text()').getall()
                title = "".join(title).replace("\n", "").replace(" ", "")

                author = div.xpath('.//span[@class="c-color-gray c-font-normal c-gap-right"]//text()').getall()
                author = "".join(author).replace("\n", "").replace(" ", "")


                # description = div.xpath('.//span[@class ="c-font-normal c-color-text"]/text()').getall()
                # description = "".join(description).replace("\n", "").replace(" ", "")



                print(title)
                print(author)
                print(time)
                # print(description)
                print(detail_url)

                item = FirstscrapyItem()
                item['title'] = title
                item['author'] = author
                item['museum'] = self.museum
                item['detail_url'] = detail_url
                item['time'] = time
                yield scrapy.Request(detail_url, callback=self.parse_detail, meta={'item': item})

            elif time<self.startTime:
                flag = 1
                break



        if flag==1:
             return

        print('page = {}'.format(self.page))
        if (self.page<40) :
            self.page += 1
            new_url = URL.format(
                museum=self.museum, bt=self.startTime, et=self.endTime, page=self.page * 10)
            print(new_url)
            yield Request(new_url, callback=self.parse, dont_filter=True)

    def parse_detail(self,response):
        item=response.meta['item']
        content_list=response.xpath('//div[@class="index-module_textWrap_3ygOc"]')
        if not content_list:
            content_list = response.xpath('//p[@class="contentFont"]')
        content=""
        for div in content_list:
            c=div.xpath('.//text()').getall()
            c= "".join(c)
            content+=c+"\n"
        #print(content)
        item['content'] = content
        yield item

    def parse_time(self, s_time):
        result_time = ''
        regex = re.compile(r"[0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日")
        # 1、2017年06月15日 13:41
        if regex.match(s_time):
            t = time.strptime(s_time, '%Y年%m月%d日')
            y, m, d = t[0:3]
            result_time = datetime.datetime(y, m, d).strftime("%Y-%m-%d")

        # 6天前
        elif u'天前' in s_time:
            days = re.findall(u'(\d+)天前', s_time)[0]
            result_time = (datetime.datetime.now() - timedelta(days=int(days))).strftime("%Y-%m-%d")

        # 昨天 18:03
        elif u'昨天' in s_time:
            result_time = (datetime.datetime.now() - timedelta(days=int(1))).strftime("%Y-%m-%d")

        elif u'前天' in s_time:
            result_time = (datetime.datetime.now() - timedelta(days=int(2))).strftime("%Y-%m-%d")

        # 28分钟前
        elif u'分钟前' in s_time:
            result_time = datetime.datetime.now().strftime("%Y-%m-%d")

        # 1小时前
        elif u'小时前' in s_time:
            result_time = datetime.datetime.now().strftime("%Y-%m-%d")

        elif re.match(r"(\d+)月(\d+)日", s_time):
            g=re.search(r'(\d+)月(\d+)日',s_time)
            result_time = str(datetime.datetime.now().year)+"-"+str(g.group(1))+"-"+str(g.group(2))
            t = time.strptime(result_time, "%Y-%m-%d")
            y, m, d = t[0:3]
            result_time = datetime.datetime(y, m, d).strftime("%Y-%m-%d")


        return result_time



