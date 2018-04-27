# -*- coding: utf-8 -*-
import scrapy

from book_sacrpy.items import BookItem


class BookSpiserSpider(scrapy.Spider):
    name = 'book_spiser'
    allowed_domains = ['allitebooks.com','amazon.com']
    start_urls = ['http://allitebooks.com/security/',]

    def parse(self, response):
        num_pages = int(response.xpath('//a[contains(@title, "Last Page →")]/text()').extract_first())
        base_url = "http://www.allitebooks.com/security/page/{0}/"
        for page in range(1,num_pages):
            yield scrapy.Request(base_url.format(page),dont_filter=True,callback=self.pare_page)


    def pare_page(self,response):
        for ever in response.css('.format-standard'):
            book_url = ever.css('.entry-thumbnail a::attr(href)').extract_first("")
            yield scrapy.Request(book_url,callback=self.pare_book_info)


    def pare_book_info(self,response):
        title = response.css('.single-title').xpath('text()').extract_first()
        isbn = response.xpath('//dd[2]/text()').extract_first('').replace(' ','')
        items = BookItem()
        items['title'] = title
        items['isbn'] = isbn
        amazon_price_url = 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=' + isbn
        yield scrapy.Request(amazon_price_url,callback=self.pare_book_price,meta={'items': items})


    def pare_book_price(self,response):
        items = response.meta['items']
        items['price'] = response.xpath('//span/text()').re(r'\$[0-9]+\.[0-9]{2}?')[0]
        yield items




