'''
https://sandbox.oxylabs.io/products
page - list of games:
-titles
-genre
-stars
-part of decs
-price
-stock
-image
click - specific games:
-all above +...
-platform
-game type
-recommended/similar games

Extracting info, best to crawl into specific games (home page info + more)
'''

import scrapy
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
import sql_funcs

# scrapy.Spider used only on defined pages, i.e., not for crawling
class FirstSpider(scrapy.Spider):
    name='first'
    allowed_domains=['sandbox.oxylabs.io']
    start_urls=[
        'https://sandbox.oxylabs.io/products'
        # 'https://sandbox.oxylabs.io/products?page=2'
    ]

    def parse(self,response):
        for i in response.xpath('/html/body/div/main/div/div/div/div[2]/div').getall():
            print(BeautifulSoup(i,'html.parser').prettify())

# if __name__=='__main__':
#     process=CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
#     process.crawl(FirstSpider)
#     process.start()

# ===================


class SpiCrawler(CrawlSpider):
    name='crawl_spider'
    allowed_domains=['sandbox.oxylabs.io']
    start_urls=['https://sandbox.oxylabs.io/products']
    rules=(
        Rule(LinkExtractor(allow=(r'\?page=\d')),follow=True),
        Rule(LinkExtractor(allow=(r'/\d+')),callback='parse_item',follow=False),
    )

    def __init__(self,*args,**kwargs):
        super(SpiCrawler,self).__init__(*args,**kwargs)
        options=Options()
        options.add_argument('--headless')
        options.add_argument("user-agent=Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)")
        self.driver=webdriver.Edge(options=options)

        self.conn=sqlite3.connect('more_advanced/scrapydb.db')
        self.cur=self.conn.cursor()

    def parse_item(self,response):
        title=response.css('h2.title::text').get().strip()
        developer=response.xpath('//span[@class="brand developer"]/text()[normalize-space()]').get().strip()
        players=response.xpath('//div[@class="brand-wrapper css-1f150rr e15c0rei0"]/span[strong[contains(text(),"Type:")]]\
                         /text()[normalize-space()]').get()
        description=response.css('p.description::text').get().strip()
        price,currency=response.css('div.price::text').get().strip().split(' ')
        price=price.replace(',','.')
        stock=response.css('p.availability::text').get().strip()

        # Selenium slower, so only using where necessary (JS)
        self.driver.get(response.url)
        WebDriverWait(self.driver,8).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div.game-genres-wrapper')))
        genres=[i.text.strip() for i in self.driver.find_elements(By.CSS_SELECTOR,'span.genre')]
        stars=len(self.driver.find_elements(By.CSS_SELECTOR,'svg.star-icon'))
        platform=self.driver.find_element(By.CSS_SELECTOR,'span.game-platform').text.strip()
        related_titles=[i.text.strip() for i in self.driver.find_elements(By.CSS_SELECTOR,'h4.title')]
        image=self.driver.find_element(By.CLASS_NAME, 'image').get_attribute("src").split('/')[-1].strip()

        data=({
            'title':title,
            'developer':developer,
            'players':players,
            'description':description,
            'price':float(price),
            'currency':currency,
            'stock':stock,
            'genres':','.join(genres),
            'stars':stars,
            'platform':platform,
            'related_titles':','.join(related_titles),
            'image':image,
        })
        self.db_insert(data)
    
    def closed(self,reason):
        self.driver.quit()
        self.conn.close()

    def db_insert(self,data):
        query='''
            INSERT INTO scrappy_data(title, developer, players, description, price, currency, stock, genres, stars, platform,
              related_titles, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        self.cur.execute(query,(
            data['title'],data['developer'],data['players'],data['description'],data['price'],data['currency'],data['stock'],
            data['genres'],data['stars'],data['platform'],data['related_titles'],data['image']
        ))
        self.conn.commit()


if __name__=='__main__':
    process=CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
    process.crawl(SpiCrawler)
    process.start()
    sql_funcs.duplicates('more_advanced/scrapydb.db')