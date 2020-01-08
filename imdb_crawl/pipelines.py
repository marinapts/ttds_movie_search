# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os

QUOTES_FOLDER = './quotes'
FOLDER_STRUCTURE_DEPTH = 3

class ImdbCrawlPipeline(object):
    def process_item(self, item, spider):
        id = item['id']
        quotes_path = QUOTES_FOLDER

        # Make folder structure 3 levels deep:
        for i in range(2,2+FOLDER_STRUCTURE_DEPTH):
            quotes_path = os.path.join(quotes_path, id[i])
            if not os.path.exists(quotes_path):
                os.mkdir(quotes_path)

        # Now, quotes_path points to the directory where the quotes file should be saved. Let's save it
        quotes_path = os.path.join(quotes_path, "{}.txt".format(id))
        with open(quotes_path, 'w') as f:
            f.write(item['quotes'])

        return item
