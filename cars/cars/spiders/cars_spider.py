import scrapy
import time
from selenium.webdriver.common.by import By
from selenium import webdriver


class CarsSpiderSpider(scrapy.Spider):
    name = 'cars_spider'

    def start_requests(self):
        driver = webdriver.Chrome(executable_path='C:\drivers\chromedriver.exe')
        driver.get('https://www.google.com/search?tbs=lf:1,lf_ui:10&tbm=lcl&sxsrf=ALiCzsZlF_AJwlwL4v22Z0oLl2wZZncUlQ:1668245725702&q=Car+Dealerships+Toronto&rflfq=1&num=10&sa=X&ved=2ahUKEwjRoIPPq6j7AhWtrokEHb9zAogQjGp6BAhrEAE&biw=1368&bih=761&dpr=2#rlfi=hd:;si:17707916458558643626,a;mv:[[43.7746593,-79.2965952],[43.650897799999996,-79.539889]]')
        driver.maximize_window()
        time.sleep(3)
        # Handling Pop-up cookies
        for link in driver.find_elements(By.CSS_SELECTOR, value=("div.rllt__details span.OSrXXb")):
            players_link = link.get_attribute('href')
            yield scrapy.Request(url = players_link, callback=self.parse_info)

    def parse_info(self, response):
        pass


