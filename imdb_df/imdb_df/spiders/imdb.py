import scrapy
from scrapy_selenium import SeleniumRequest

class ImdbSpider(scrapy.Spider):
    name = 'imdb'
    def start_requests(self):
        url = 'https://www.imdb.com/search/title/?title_type=feature&year=2016-01-01,2022-09-30&sort=num_votes,desc&start=80000&ref_=adv_nxt'
        yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        container = response.css('div.lister-item.mode-advanced')
        for content in container:
            yield {'movie_name': content.css('h3.lister-item-header a::text').get(),
                   'released_year': content.css('h3.lister-item-header span.lister-item-year::text').get(),
                   'parental_guide': content.css('p.text-muted span:nth-child(1)::text').get(),
                   'runtime': content.css('span.runtime::text').get(),
                   'genre': content.css('span.genre::text').get(),
                   'vote': content.css('p.sort-num_votes-visible :nth-child(2)::text').get(),
                   'rating': content.css('div.ratings-imdb-rating strong::text').get(),
                   'metascore': content.css('div.ratings-metascore span::text').get(),
                   'gross': content.css('p.sort-num_votes-visible :nth-child(5)::text').get(),
                   'director': content.css('div.lister-item-content p:nth-child(5) a[href*="adv_li_dr"]::text').getall()
                   }

        try:
            next_page = response.css("div.nav div.desc a.lister-page-next.next-page::attr(href)").get()
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)
        except:
            pass


