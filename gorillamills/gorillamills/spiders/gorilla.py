# Importing of necessary Libraries
import scrapy
from scrapy_splash import SplashRequest

# Building of the scrapy class for parsing of gorillamill site

class GorillamillSpiderSpider(scrapy.Spider):
    name = 'gorillamill_spider'
    start_urls = ['https://gorillamill.com/products/high-performance-cutting-tools/',
                  'https://gorillamill.com/products/high-performance-roughers/',
                  'https://gorillamill.com/products/super-bitchin-performance-cutting-tools/',
                  'https://gorillamill.com/products/super-bitchin-performance-rougher-finisher/',
                  'https://gorillamill.com/products/high-performance-die-mold-chimps/',
                  'https://gorillamill.com/products/standard-performance-cutting-tools/',
                  'https://gorillamill.com/products/standard-performance-roughers/',
                  'https://gorillamill.com/products/high-performance-drills/',
                  'https://gorillamill.com/products/high-performance-chamfer-mills/',
                  'https://gorillamill.com/products/standard-performance-chamfer-mills/',
                  'https://gorillamill.com/products/high-performance-threadmills/',
                  'https://gorillamill.com/products/picatinny-form-cutters/',
                  'https://gorillamill.com/products/package-deals/'
                  ]
    # Following various products url

    def parse(self, response):
        products = response.css('div.product a::attr(href)').getall()
        for product in products:
            yield SplashRequest(product, callback=self.parse_sub_product)

    # Following various sub-products url

    def parse_sub_product(self, response):
        sub_products = response.css('div.product a::attr(href)').getall()
        for sub_product in sub_products:
            yield SplashRequest(sub_product, callback=self.parse_products_details)

    # Parsing of the gorillamill products

    def parse_products_details(self, response):
        yield {
            'title': response.css('div#specs div.uk-width-large-6-10 h1::text').get() + ', '.join(response.css('div#specs div.uk-width-large-6-10 h2::text').getall()),
            'image_url':response.css('div#specs div.uk-width-large-6-10 img::attr(src)').get(),
            'document_url':response.css('div#diagram-inner img::attr(src)').get(),
            'description': response.css('div#desc p:nth-child(2)::text').get() + response.css('div#desc p strong::text').get() + ', '.join(response.css('div#tolerances ul li::text').getall()),
            'attribute': [att.strip() for att in response.css('div.items div.uk-width-medium-3-10::text').getall() + response.css('div.items div.uk-width-medium-4-10::text').getall()],
            'stocks':response.css('div.items div.uk-width-medium-4-10 a::attr(data-stock)').get()
        }