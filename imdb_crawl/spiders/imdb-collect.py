# -*- coding: utf-8 -*-
import scrapy
import logging
import re
from imdb_crawl.items import ImdbCrawlItem

"""
iMDB data:
#1 Main page: https://www.imdb.com/title/tt0111161
- Title [x]
- Categories (Genres) [x]
- Thumbnail [x]
- Year [x]
- Rating [x]
- Count of ratings [x]
#2 Cast page: https://www.imdb.com/title/tt0111161/fullcredits
- Cast: actors and character name
#3 Plot Keywords page: https://www.imdb.com/title/tt0111161/keywords
- Plot keywords (maybe only take those that have no relevance ratings or majority of people found them relevant?)
#4 Quotes page: https://www.imdb.com/title/tt0111161/quotes
- Quotes (character name and quote) [x]
"""

IMDB_IDS_FILE = './imdb-top1000.txt'

class iMDBCollect(scrapy.Spider):
    name = 'imdb-collect'
    start_urls = []
    with open(IMDB_IDS_FILE, 'r') as f:
        for id in f:
            id = re.sub(r'\s+', '', id)
            if re.match(r'tt\d+', id):
                start_urls.append('https://www.imdb.com/title/{}/'.format(id))

    # Entry method for crawling movie's main page
    def parse(self, response):
        main_url = response.url
        item = ImdbCrawlItem()

        # Scrape the main page info here and add it to item
        item['id'] = main_url.split("/")[-2]
        item['title'] = response.xpath('//div[@class="title_wrapper"]/h1/text()').extract_first().replace('\xa0', '')
        item['year'] = int(response.xpath('//span[@id="titleYear"]/a/text()').extract_first())
        rating_title = response.xpath('//div[@class="ratingValue"]/strong/@title').extract_first()
        item['rating'] = float(rating_title.split(" ")[0])
        item['countOfRatings'] = int(rating_title.split(" ")[3].replace(",", ""))
        genres = response.xpath('//div[@class="title_wrapper"]/div[@class="subtext"]/a/text()').getall()
        item['categories'] = [g for g in genres if g.isalpha()]
        item['thumbnail'] = response.xpath('//div[@class="poster"]//img/@src').extract_first()


        yield scrapy.Request(main_url+'fullcredits',
                             meta={'main_url': main_url, 'item': item},
                             callback=self.parse_cast)

        """
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
        """


    def parse_cast(self, response):
        main_url = response.request.meta['main_url']
        item = response.request.meta['item']

        # Scrape the cast data here and add it to item
        item['cast'] = dict()
        cast_table = response.xpath('//table[@class="cast_list"]//tr')
        for tr in cast_table:
            first_td_text = tr.xpath('.//td/text()').extract_first()
            if first_td_text is not None and "Rest" in first_td_text:
                break  # rest of cast, irrelevant
            names = tr.xpath('.//a/text()').getall()
            names_without_link = tr.xpath('.//td/text()').getall()
            final_names = [n.replace('\n', '').strip() for n in names+names_without_link if len(n.replace("...", "").strip()) > 0]
            if len(final_names) == 2:
                item['cast'][final_names[0]] = final_names[1]


        yield scrapy.Request(main_url + 'keywords',
                             meta={'main_url': main_url, 'item': item},
                             callback=self.parse_keywords)


    def parse_keywords(self, response):
        main_url = response.request.meta['main_url']
        item = response.request.meta['item']

        # Scrape the plot keywords here and add them to item
        item['plotKeywords'] = response.xpath('//td[@class="soda sodavote"]/@data-item-keyword').getall()

        yield scrapy.Request(main_url + 'quotes',
                             meta={'main_url': main_url, 'item': item},
                             callback=self.parse_quotes)


    def parse_quotes(self, response):
        item = response.request.meta['item']

        # Scrape the quotes data here and add it to item
        quotes = response.xpath('//div[starts-with(@id,"qt")]/div[@class="sodatext"]/descendant::text()').getall()
        full_quotes = ''.join(quotes)
        full_quotes = re.sub(r'\[.*\]', '', full_quotes)
        full_quotes = re.sub(r':\s*\n', ': ', full_quotes)
        while True:
            before = full_quotes
            full_quotes = re.sub(r'\n\s*\n', '\n', full_quotes)
            if before == full_quotes:
                break
        full_quotes = re.sub(r'\n.*:\s*\n', '\n', full_quotes)
        full_quotes = re.sub(r'\s+\n', '\n', full_quotes)
        item['quotes'] = full_quotes

        yield item

