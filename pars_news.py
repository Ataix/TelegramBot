import csv
import requests
import datetime
from bs4 import BeautifulSoup

url = 'https://kaktus.media/'

def get_html(url):
    res = requests.get(url)
    return res.text

def write_csv(data):
    """Сохраняет данные в csv"""
    with open('news.csv', 'a+') as basic_file:
        writer = csv.writer(basic_file)
        writer.writerow((data['title'], data['img'], data['article']))

def get_table_data(html):
    """Извлекаем новости с таблицы"""
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('ul', class_= 'topic_list view_lenta 1').find_all('li', class_='topic_item clearfix')
    for el in table:    
        try:
            title = el.find('div', class_= 't f_medium').find('span', class_ = 'n').text
        except:
            title = ''
        try:
            title_url = el.find('div', class_= 't f_medium').find('a').get('href')
            title_html = get_html(title_url)
            article_soup = BeautifulSoup(title_html, 'html.parser')
            article = article_soup.find('div', itemprop = 'articleBody').text
        except:
            article = ''
        try:
            img = el.find('div', class_= 'i').find('img').get('data-src')
        except:
            img = ''

        data = {'title': title, 'img': img, 'article': article}
        write_csv(data)

def main():
    html = get_html(url)
    get_table_data(html)

if __name__ == '__main__':
    main()