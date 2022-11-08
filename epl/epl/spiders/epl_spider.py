# Importing of necessary libraries
import time
import scrapy
from selenium.webdriver.common.by import By
from selenium import webdriver

# Building the crawler class
class EplSpiderSpider(scrapy.Spider):
    name = 'epl_spider'

    def start_requests(self):
        driver = webdriver.Chrome(executable_path='C:\drivers\chromedriver.exe')
        driver.get('https://www.premierleague.com/stats/top/players/appearances?se=-1')
        driver.maximize_window()
        time.sleep(3)
        # Handling Pop-up cookies
        try:
            cookies = driver.find_element(By.CSS_SELECTOR, value='button.js-accept-all-close')
            cookies.click()
        except:
            pass

        for link in driver.find_elements(By.CSS_SELECTOR, value=("tbody.statsTableContainer a.playerName")):
            players_link = link.get_attribute('href')
            yield scrapy.Request(url = players_link, callback=self.parse_info)

        # Dealing with pagination
        while True:
            try:
                next_page = driver.find_element(By.CSS_SELECTOR, value='div.paginationNextContainer div:nth-child(2)')
                if next_page is not None:
                    driver.execute_script("arguments[0].click();", next_page)
                    time.sleep(3)
            except:
                print('No more pages to load')
                break
        driver.quit()

    # Parsing of epl website
    def parse_info(self, response):
            yield {
                'player_name': response.css('div.name::text').get(),
                'player_nationality' : response.css('span.playerCountry::text').get(),
                'player_DOB': response.css('ul.pdcol2 div.info::text').get(),
                'player_height': response.css('ul.pdcol3 div.info::text').get(),
                'indigene':response.css('div.homeGrown::text').get(),
                'honours_and_awards': response.css('div.playerOverviewAside.u-hide-mob table.honoursAwards tbody tr th::text').getall(),
                'awards_season':response.css('div.playerOverviewAside.u-hide-mob table.honoursAwards tbody tr table td::text').getall(),
                'player_position': response.css('div.playerOverviewAside.u-hide-mob div.info::text').get()

            }


    def parse(self, response):
        player_stat = response.urljoin('stats')
        yield scrapy.Request(url=player_stat, callback=self.parse_stat)

    def parse_stat(self, response):
        yield {
            'player_name': response.css('div.name::text').get(),
            'appearance' : response.css('span[data-stat="appearances"]::text').get(),
            'goals':response.css('div.topStat span[class="allStatContainer statgoals"]::text').get(),
            'statwins':response.css('span.allStatContainer.statwins::text').get(),
            'statlosses':response.css('span.allStatContainer.statlosses::text').get()

        }
