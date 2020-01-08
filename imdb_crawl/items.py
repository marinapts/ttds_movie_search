# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

"""
iMDB data:
#1 Main page: https://www.imdb.com/title/tt0111161
- Title
- Categories (Genres)
- Thumbnail
- Year
- Rating
- Count of ratings
#2 Cast page: https://www.imdb.com/title/tt0111161/fullcredits
- Cast: actors and character name
#3 Plot Keywords page: https://www.imdb.com/title/tt0111161/keywords
- Plot keywords (only take those that have no relevance ratings or majority of people found them relevant)
#4 Quotes page: https://www.imdb.com/title/tt0111161/quotes
- Quotes (character name and quote)
"""

class ImdbCrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    title = scrapy.Field()  # string
    categories = scrapy.Field()  # list of strings
    thumbnail = scrapy.Field()  # string (URL)
    year = scrapy.Field()  # int
    rating = scrapy.Field()  # float
    countOfRatings = scrapy.Field()  # int
    cast = scrapy.Field()  # dict: actorName -> characterName
    plotKeywords = scrapy.Field()  # list of strings
    quotes = scrapy.Field()  # dict: characterName -> quote
