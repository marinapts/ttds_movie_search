# -*- coding: utf-8 -*-
import scrapy
import logging
import re
from imdb_crawl.items import ImdbCrawlItem
from imdb_crawl.utils import *
from imdb_crawl import settings

"""
iMDB data:
#1 Main page: https://www.imdb.com/title/tt0111161
- Title [x]
- Description [x]
- Categories (Genres) [x]
- Thumbnail [x]
- Year [x]
- Rating [x]
- Count of ratings [x]
#2 Cast page: https://www.imdb.com/title/tt0111161/fullcredits
- Cast: actors and character name [x]
#3 Plot Keywords page: https://www.imdb.com/title/tt0111161/keywords
- Plot keywords (maybe only take those that have no relevance ratings or majority of people found them relevant?) [x]
#4 Quotes page: https://www.imdb.com/title/tt0111161/quotes
- Quotes (character name and quote) [x]
"""

IMDB_IDS_FILE = settings.IMDB_IDS_FILE
QUOTES_FOLDER = settings.QUOTES_FOLDER
DATA_FILE = settings.DATA_FILE

class iMDBCollect(scrapy.Spider):
    name = 'imdb-collect'
    start_urls = []
    print("Initialising start urls...")
    with open(IMDB_IDS_FILE, 'r') as f:
        k = 0
        for id in f:
            k += 1
            id = re.sub(r'\s+', '', id)
            if re.match(r'tt\d+', id):
                # Only webscrape data/quotes for this movie if it has not been scraped already (doesn't exist)
                if not exists_data(id, DATA_FILE) or not exists_quotes(id, QUOTES_FOLDER):
                    start_urls.append('https://www.imdb.com/title/{}/'.format(id))
            # Log progress
            if k % 100 == 0:
                print("{} movie ids have been processed.".format(k))


    # Entry method for crawling movie's main page
    def parse(self, response):
        main_url = response.url
        item = ImdbCrawlItem()

        # Scrape the main page info here and add it to item
        item['id'] = main_url.split("/")[-2]
        item['title'] = response.xpath('//div[@class="title_wrapper"]/h1/text()').extract_first().replace('\xa0', '').strip()
        item['description'] = ''.join(response.xpath('//div[@class="summary_text"]/descendant::text()').getall()).strip()
        try:
            item['year'] = int(response.xpath('//span[@id="titleYear"]/a/text()').extract_first())
        except:
            print("Failed to extract year for {}".format(item['id']))
        rating_title = response.xpath('//div[@class="ratingValue"]/strong/@title').extract_first()
        item['rating'] = float(rating_title.split(" ")[0])
        item['countOfRatings'] = int(rating_title.split(" ")[3].replace(",", ""))
        genres = response.xpath('//div[@class="title_wrapper"]/div[@class="subtext"]/a/text()').getall()
        item['categories'] = [g for g in genres if g.isalpha()]
        item['thumbnail'] = response.xpath('//div[@class="poster"]//img/@src').extract_first()


        yield scrapy.Request(main_url+'fullcredits',
                             meta={'main_url': main_url, 'item': item},
                             callback=self.parse_cast)



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

        # If no cast found so far, then there must be something wrong with the schema above. Try a different one (for TV Series)
        if len(item['cast']) == 0:
            for tr in cast_table:
                try:
                    actor = ''.join(tr.xpath('.//td')[1].xpath('./descendant::text()').getall()).strip()
                    character = ''.join(tr.xpath('.//td[@class="character"]/descendant::text()').getall()).strip().split('\n')[0].strip()
                    if actor != '' and character != '':
                        item['cast'][actor] = character
                except:
                    pass





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

