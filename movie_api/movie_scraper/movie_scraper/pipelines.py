# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


# class MovieScraperPipeline:
#     def process_item(self, item, spider):
#         return item
# movie_scraper/pipelines.py
class DataPipeline:
    def __init__(self):
        self.data = []

    def open_spider(self, spider):
        print("Pipeline: Spider opened.")

    def process_item(self, item, spider):
        print(f"Pipeline: Processing item: {item}")  # Debug log
        self.data.append(item)
        return item

    def close_spider(self, spider):
        print(f"Pipeline: Spider closed. Items collected: {len(self.data)}")
