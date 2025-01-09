from django.http import JsonResponse
import scrapy
import json
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from movie_scraper.movie_scraper.spiders.movies_spider import MoviesSpiderSpider  # Import your Scrapy spider class

from django.http import JsonResponse
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def fetch_movies(request, genre):
    scraped_data = []  # Store the scraped data

    try:
        # Custom pipeline to collect data
        class DataPipeline:
            def __init__(self):
                self.data = []

            def process_item(self, item, spider):
                # print(f"Processing item: {item}")  # Debug log
                self.data.append(item)
                return item


        # Create a Scrapy process with custom pipeline
        pipeline = DataPipeline()
        MoviesSpiderSpider.custom_pipeline = pipeline  # Pass pipeline to spider

        # Set up the Scrapy process
        process = CrawlerProcess(get_project_settings())

        # Start Scrapy and wait until it finishes
        process.crawl(MoviesSpiderSpider, genre=genre)
        print("Starting Scrapy process...")
        process.start()  # This will block until the spider finishes
        print("Scrapy process completed.")


        # Retrieve data from the pipeline
        scraped_data = pipeline.data

        # Return the scraped data as JSON
        # print(f"Scraped data: {scraped_data}")  # Debug log
        return JsonResponse(scraped_data, safe=False)


    except Exception as e:
        print(f"Error occurred: {e}")
        return JsonResponse({"error": "Failed to scrape data"}, status=500)
