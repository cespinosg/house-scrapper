import datetime
import os
import re

from bs4 import BeautifulSoup
import pandas as pd
import requests


class Scrapper:
    '''
    Reads idealista information about the housing market.
    '''

    def __init__(self):
        self.url = 'https://www.idealista.com/venta-viviendas/reus-tarragona/con-metros-cuadrados-mas-de_80,metros-cuadrados-menos-de_120/'

    def _get_html(self):
        '''
        Gets the page source code.
        '''
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'
        # How to solve the 403 error https://stackoverflow.com/a/60698630
        self.request = requests.get(self.url, headers={'User-Agent': user_agent})
        self.soup = BeautifulSoup(self.request.text, 'html.parser')

    def get_price(self):
        '''
        Finds the average price per m2 from the page html source code.
        '''
        self._get_html()
        # https://realpython.com/beautiful-soup-web-scraper-python/#find-elements-by-html-class-name
        price = self.soup.find_all('p', class_='items-average-price')[0].text
        price = re.search(r'([\d\.]+) eur/m', price)
        self.price = float(price.group(1).replace('.', ''))

    def append(self):
        '''
        Appends the current average price to the csv file.
        '''
        self.get_price()
        now = datetime.datetime.now()
        log = 'log.csv'
        if os.path.isfile(log):
            df = pd.read_csv(log, index_col='time')
        else:
            df = pd.DataFrame()
        index = pd.Index(data=[now], name='time')
        row = pd.DataFrame(data={'price': [self.price]}, index=index)
        df = df.append(row)
        df.to_csv(log)


if __name__ == '__main__':
    scrapper = Scrapper()
    scrapper.append()
