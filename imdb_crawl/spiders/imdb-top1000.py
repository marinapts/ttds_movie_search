# -*- coding: utf-8 -*-
import scrapy


class iMDBTop1000Spider(scrapy.Spider):
    name = 'imdb-top1000'
    start_urls = [
        'https://www.imdb.com/search/title/?groups=top_1000&view=simple&sort=user_rating,desc&count=100&start=1',
    ]

    def parse(self, response):
        for movie in response.xpath('//div[@class="lister-item mode-simple"]'):
            yield {
                'img': movie.xpath('.//img/@src').extract_first(),
                'index': int(movie.xpath('.//span[@class="lister-item-index unbold text-primary"]/text()').extract_first().replace(",", "").replace(".", "")),
                'title': movie.xpath('.//div[@class="col-title"]//a/text()').extract_first(),
                'url': movie.xpath('.//div[@class="col-title"]//a/@href').extract_first(),
                'year': movie.xpath('.//span[@class="lister-item-year text-muted unbold"]/text()').extract_first().replace("(", "").replace(")", ""),
                'rating': movie.xpath('.//strong/@title').extract_first().split(" ")[0]
            }

        next_page_url = response.xpath('//a[@class="lister-page-next next-page"]/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

        # for quote in response.xpath('//div[@class="quote"]'):
        #     yield {
        #         'text': quote.xpath('./span[@class="text"]/text()').extract_first(),
        #         'author': quote.xpath('.//small[@class="author"]/text()').extract_first(),
        #         'tags': quote.xpath('.//div[@class="tags"]/a[@class="tag"]/text()').extract()
        #     }
        #
        # next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        # if next_page_url is not None:
        #     yield scrapy.Request(response.urljoin(next_page_url))