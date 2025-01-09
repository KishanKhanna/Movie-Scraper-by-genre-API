import scrapy
import json

class MoviesSpiderSpider(scrapy.Spider):
    name = "movies_spider"

    # Add custom pipeline dynamically
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(MoviesSpiderSpider, cls).from_crawler(crawler, *args, **kwargs)
        if hasattr(cls, 'custom_pipeline'):
            crawler.signals.connect(cls.custom_pipeline.process_item, signal=scrapy.signals.item_scraped)
        return spider
    
    start_urls = [ "https://www.rottentomatoes.com/browse/movies_at_home/genres:" ]

    # Modify this to accept genre as an argument when the spider is run
    def __init__(self, genre=None, *args, **kwargs):
        super(MoviesSpiderSpider, self).__init__(*args, **kwargs)
        if genre:
            self.start_urls[0] += genre.strip().lower()  # Dynamically append genre to the URL

    def parse(self, response):
        # Extract the JSON from the <script> tag
        script_data = response.xpath('//script[@type="application/ld+json"]/text()').get()
        if script_data:
            data = json.loads(script_data)
            # Ensure we navigate the nested structure correctly
            item_list_element = data.get('itemListElement', {}).get('itemListElement', [])
            for movie in item_list_element:
                if movie.get('@type') == 'Movie':
                    yield {
                        'name': movie.get('name'),
                        'url': movie.get('url'),
                        'rating': movie.get('aggregateRating', {}).get('ratingValue'),
                        'review_count': movie.get('aggregateRating', {}).get('reviewCount'),
                        'image': movie.get('image'),
                        'date_created': movie.get('dateCreated'),
                    }
        
        # Extract images directly from the HTML for additional movies
        movies = response.xpath('//div[contains(@class, "flex-container")]')
        for movie in movies:
            image = movie.xpath('.//rt-img/@src').get()
            name = movie.xpath('.//span[@data-qa="discovery-media-list-item-title"]/text()').get()
            url = movie.xpath('.//a[@data-qa="discovery-media-list-item-caption"]/@href').get()
            if name and image:
                yield {
                    'name': name.strip(),
                    'url': response.urljoin(url) if url else None,
                    'image': image.strip(),
                }
