from scrapy.spiders import CrawlSpider
from scrapy.crawler import CrawlerProcess
import variables
from scrapy.utils.project import get_project_settings
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

class FirstSpider(CrawlSpider):
    name='rotating_crawler'
    allowed_urls=['books.toscrape.com']
    start_urls=['https://books.toscrape.com/']

    rules=(Rule(LinkExtractor(allow='/catalogue'),'parse',follow=False),)
    
    def __init__(self,*args,**kwargs):
        super(FirstSpider,self).__init__(*args,**kwargs)

    @classmethod
    def update_settings(cls,settings):
        super().update_settings(settings)
        settings.set('USER_AGENT_LIST',variables.ROTATING_AGENT_LIST,priority='spider')
        settings.set('ROTATING_PROXY_LIST',variables.ROTATING_PROXY_LIST,priority='spider')
        settings.set('DOWNLOADER_MIDDLEWARES',variables.DOWNLOADER_MIDDLEWARES,priority='spider')
    
    def parse(self,response):
        proxy = response.request.meta.get('proxy', 'No proxy')
        user_agent = response.request.headers.get('User-Agent', b'').decode('utf-8')
        print(f"\nUser-Agent: {user_agent}\n")
        ip_address = response.ip_address
        print(f"\nIP Address: {ip_address}\n")
        proxy = response.request.meta.get('proxy', b'').decode('utf-8')
        print(f"\n\nProxy Used: {proxy} \n\n")

if __name__=='__main__':
    settings=get_project_settings()
    custom_settings={
        'ROTATING_PROXY_LIST':variables.ROTATING_PROXY_LIST,
        'USER_AGENT_LIST':variables.ROTATING_AGENT_LIST,
        'DOWNLOADER_MIDDLEWARES':variables.DOWNLOADER_MIDDLEWARES,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 2.0,
        'AUTOTHROTTLE_MAX_DELAY': 20.0,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 0.5,
        'DOWNLOAD_DELAY': 10.0,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1
    }
    settings.update(custom_settings)
    crawl=CrawlerProcess(settings=settings)
    crawl.crawl(FirstSpider)
    crawl.start()