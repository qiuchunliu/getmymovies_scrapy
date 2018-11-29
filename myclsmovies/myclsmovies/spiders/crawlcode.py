# -*- coding: utf-8 -*-
import scrapy
from myclsmovies.items import MyclsmoviesItem


class CrawlcodeSpider(scrapy.Spider):
    name = 'crawlcode'
    allowed_domains = ['maoyan.com']
    start_urls = ['http://maoyan.com/board/4?offset=0']
    url_domain = 'http://maoyan.com/board/4'

    def parse(self, response):
        dd = response.xpath('//dd')
        for each in dd:
            movieranking = each.xpath('./i/text()').get()
            moviename = each.xpath('./a/@title').get()
            movietime = each.xpath('.//p[@class="releasetime"]/text()').get().split('：')[-1]
            movieactor = each.xpath('.//p[@class="star"]/text()').get().strip()  # 需要去掉换行符
            movielink = each.xpath('./a/@href').get()  # 完整连接需要拼接
            moviescore = ''.join(each.xpath('.//p[@class="score"]//text()').getall())
            item = MyclsmoviesItem(movie_ranking=movieranking,
                                   movie_name=moviename,
                                   movie_time=movietime,
                                   movie_actor=movieactor,
                                   movie_link=movielink,
                                   movie_score=moviescore
                                   )
            yield item
        print('保存了一页')
        next_page = response.xpath('//ul[@class="list-pager"]/li[last()]/a/@href').get()
        # ?offset=10
        # print(next_page)
        # end = response.xpath('//ul[@class="list-pager"]/li[last()]/a/@class').get()
        # if end != 'page_10':
        #     next_page_url = self.url_domain + next_page
        #     yield scrapy.Request(next_page_url, callback=self.parse)
        # else:
        #     print('*****全部爬取完成*****')
        #     return
        next_page_url = self.url_domain + next_page
        yield scrapy.Request(next_page_url, callback=self.parse)
        end = response.xpath('//ul[@class="list-pager"]/li[last()]/a/@class').get()
        if end == 'page_10':
            print('*****全部爬取完成*****')
            return
