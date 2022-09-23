import requests
from bs4 import BeautifulSoup
import random

def get_link():
    r = requests.get('http://www.google.com')
    year = 0
    month = 0
    day = 0
    while(1):
        year = random.randint(1985, 1995)
        month = random.randint(1, 12)
        day = random.randint(1, 31)
        r = requests.get(
            f'https://www.gocomics.com/calvinandhobbes/{year}/{month}/{day}')
        if r.status_code == 200:
            break

    soup = BeautifulSoup(r.content, 'lxml')
    tag = soup.find_all("picture", class_='item-comic-image')
    url = tag[0].img['src']
    return [url, year, month, day]