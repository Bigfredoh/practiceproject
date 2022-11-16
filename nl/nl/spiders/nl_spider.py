# Importing of the necessary libraries
import scrapy
from scrapy import Request
# Building of scrapy framework for parsing the website
class TotalspiderSpider(scrapy.Spider):
    name = 'nairaland'
    current_page = 4554
    start_urls = ['https://www.nairaland.com/news/']
# Extracting links from all the pages
    def parse(self, response):
        links =  response.css('[summary="links"] a::attr(href)').getall()
        for link in links:
            yield Request(url=link, callback=self.parse_categories)
        total_pages = int(response.css('div.body p:nth-child(6) b:last-child::text').get())
        url = 'https://www.nairaland.com/news/' + str(TotalspiderSpider.current_page)
        if TotalspiderSpider.current_page <= total_pages:
            TotalspiderSpider.current_page += 1
            yield Request (url=url, callback=self.parse)
# Parsing of the website
    def parse_categories(self, response):
        news_container = response.css('div.body')
        for content in news_container:
            yield {
                'news': content.css('p.bold a:nth-child(4)::text').get(),
                'news_category':(content.css('p.bold a:nth-child(3)::text').get()),
                'views': content.css('p.bold::text').getall(),
                'poster':content.css('a.user::text').get(),
                'time':content.css('span.s b:nth-child(1)::text').get(),
                'month':content.css('span.s b:nth-child(2)::text').get(),
                'year':content.css('span.s b:nth-child(3)::text').get(),
                'news_link': response.urljoin(content.css('p.bold a:nth-child(4)::attr(href)').get())

            }


