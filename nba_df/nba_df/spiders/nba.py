# Importing of the necessary libraries
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
# Building of scrapy framework for parsing the website
class NbaspiderSpider(scrapy.Spider):
    name = 'nbaspider'

    # Integration of Selenium into Scrapy

    def start_requests(self):
        driver = webdriver.Chrome(executable_path='C:\drivers\chromedriver.exe')
        driver.get('https://www.nba.com/stats/alltime-leaders?')
        driver.maximize_window()
        time.sleep(3)

        cookie = driver.find_element(By.CSS_SELECTOR, value='button#onetrust-accept-btn-handler')
        cookie.click()
        time.sleep(3)
        #pagination
        pagination = driver.find_element(By.CSS_SELECTOR, value='div.Pagination_content__f2at7')
        pages = pagination.find_elements(By.CSS_SELECTOR, value='div.Pagination_pageDropdown__KgjBU option')
        last_page = int(pages[-1].text)
        current_page = 1
        while current_page <= last_page:
            for link in driver.find_elements(By.CSS_SELECTOR, value=("td.Crom_text__NpR1_.Crom_primary__EajZu.Crom_stickySecondColumn__29Dwf a")):
                players_link = link.get_attribute('href')
                yield scrapy.Request(players_link)

            current_page=+1
            try:
                next_button = driver.find_element(By.CSS_SELECTOR,value='div.Pagination_buttons__YpLUe button:nth-child(2)')
                next_button.click()
            except:
                break
        driver.quit()
    # Parsing of the website
    def parse(self, response):
        players_info = response.css('div.PlayerSummary_summary__CGowU')
        for player in players_info:
            yield {
                'player_info' : player.css('p.PlayerSummary_mainInnerInfo__jv3LO::text').get(),
                'player_name' : player.css('p.PlayerSummary_playerNameText___MhqC::text').getall(),
                'player_height':player.css('div.PlayerSummary_flexTop__g8SVG div:nth-child(1) p:nth-child(2)::text').get(),
                'player_weight':player.css('div.PlayerSummary_flexTop__g8SVG div:nth-child(3) p:nth-child(2)::text').get(),
                'player_nationality':player.css('div.PlayerSummary_flexTop__g8SVG div:nth-child(5) p:nth-child(2)::text').get(),
                'last_attended':player.css('div.PlayerSummary_flexTop__g8SVG div:nth-child(7) p:nth-child(2)::text').get(),
                #'player_age': player.css('div.PlayerSummary_hw__HNuGb div.PlayerSummary_flexBlock___CyTE div:nth-child(1) p:nth-child(2)::text').get(),
                'player_birthdate': player.css('div.PlayerSummary_hw__HNuGb div.PlayerSummary_flexBlock___CyTE div:nth-child(1) p:nth-child(2)::text').get(),
                'nba_draft':player.css('div.PlayerSummary_hw__HNuGb div.PlayerSummary_flexBlock___CyTE div:nth-child(3) p:nth-child(2)::text').get(),
                'years_of_experience':player.css('div.PlayerSummary_hw__HNuGb div.PlayerSummary_flexBlock___CyTE div:nth-child(5) p:nth-child(2)::text').get(),
                'player_points_per_game':player.css('div.PlayerSummary_statsSectionStats__9TdUC div:nth-child(2) p:nth-child(2)::text').get(),
                'player_rebounds_per_game':player.css('div.PlayerSummary_statsSectionStats__9TdUC div:nth-child(4) p:nth-child(2)::text').get(),
                'player_assists_per_game': player.css('div.PlayerSummary_statsSectionStats__9TdUC div:nth-child(6) p:nth-child(2)::text').get(),
                'player_pie':player.css('div.PlayerSummary_statsSectionStats__9TdUC div:nth-child(8) p:nth-child(2)::text').get()

            }


