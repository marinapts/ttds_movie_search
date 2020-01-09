# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
from scrapy.exporters import JsonItemExporter

QUOTES_FOLDER = './quotes'
OUTPUT_JSON_FILE = './movies.json'
FOLDER_STRUCTURE_DEPTH = 3

class ImdbCrawlPipeline(object):
    def open_spider(self, spider):
        f = open(OUTPUT_JSON_FILE, 'wb')
        self.exporter = JsonItemExporter(f)
        self.exporter.start_exporting()


    def close_spider(self, spider):
        self.exporter.finish_exporting()


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
        with open(quotes_path, 'wb') as f:
            f.write(item['quotes'].encode('utf-8'))

        # The quotes are now written, so it is safe to discard them from the item
        del item['quotes']

        # Export everything else to JSON file:
        self.exporter.export_item(item)

        return item
