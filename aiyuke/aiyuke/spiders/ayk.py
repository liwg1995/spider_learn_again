# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from aiyuke.items import AiyukeItem



class AykSpider(scrapy.Spider):
    name = 'ayk'
    allowed_domains = ['www.aiyuke.com']
    start_urls = ['http://www.aiyuke.com/view/cate/index.htm']
    headers = {
        "Host": "www.aiyuke.com",
        "Referer": "http://www.aiyuke.com/view/cate/yundongbaojian.htm",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }


    def parse(self, response):
        nodes = response.css(".news_list_main .news_list_box")
        for node in nodes:
            url = node.css(".desc h1 a::attr(href)").extract_first("")
            image_url = node.css(".img a img::attr(src)").extract_first("")
            yield scrapy.Request(url, headers=self.headers, callback=self.content, meta={"image_url": image_url})

        next_page = response.css(".p_next::attr(href)").extract_first("")
        now_url = response.url
        if next_page:
            yield scrapy.Request(url=parse.urljoin(now_url, next_page), headers=self.headers, callback=self.parse)

    def content(self, response):
        title = response.css(".news_content h1::text").extract_first('')
        source = response.css(".news_from::text").extract_first('').split(':')[-1].strip()
        datetime = response.css(".news_date::text").extract_first('').strip()
        contents = response.css(".news_content_body p").extract()[1:-3]
        content = "".join(contents).strip()
        cate = response.css(".showpath li a span::text").extract()[2]
        image_url = response.meta.get("image_url")
        items = AiyukeItem()
        items['title'] = title
        items['source'] = source
        items['datetime'] = datetime
        items['content'] = content
        items['cate'] = cate
        items['image_url'] = image_url
        yield items
