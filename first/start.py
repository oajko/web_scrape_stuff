import requests
from bs4 import BeautifulSoup
import data_inserter
import concurrent.futures

def walk_links(data):
    temp=data.contents[0]
    return (temp.get('href'),temp.text)

def run_scraper(pages):
    assert (pages is not int) or (pages > 0), 'pages should be integer and > 0'
    for page in range(pages):
        if page > 0:
            link=requests.get(f'https://news.ycombinator.com/?p={page+1}')
        else:
            link=requests.get('https://news.ycombinator.com/')
        soup=BeautifulSoup(link.content,'html.parser')

        links=soup.find_all(class_='titleline')
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            links=list(executor.map(walk_links,links))
        
        for href,text in links:
            data_inserter.insert_data(href,text)

if __name__=='__main__':
    run_scraper(3)