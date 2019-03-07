import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from time import sleep
from random import randint

# urls
url_guardian = "https://www.theguardian.com/football/series/rumourmill"
url_bbc = "https://www.bbc.com/sport/football/gossip"

# pages
page = requests.get(url_guardian)
bbc_page = requests.get(url_bbc)

# instances
soup = BeautifulSoup(page.content, 'html.parser')
souper = BeautifulSoup(bbc_page.content, 'html.parser')

# functions
def drop_reporters_in_rumors(rumor):
    for i in rumor:
        if(len(i) < 15):
            rumor.remove(i)

# Guardian
rumors = [entry.get_text().split(':')[1] for entry in soup.find_all(attrs={"class":"js-headline-text","data-link-name":"article"})]
links = [link.get('href') for link in soup.find_all(attrs={"class":"js-headline-text","data-link-name":"article"})]
dates = [date.get_text() for date in soup.find_all('time')[::2]]
players = pd.DataFrame({'rumors':rumors,'links':links,'date_posted':dates})

# BBC Sports
bbc_rumors = [entry.text for entry in souper.select('div#story-body p')]
bbc_links = [entry.get('href') for entry in souper.select('div#story-body a')[:(len(bbc_rumors))]]
bbc_dates = [date.get('title') for date in souper.find_all('abbr')[::2]]
bbc_dates = list(bbc_dates * (len(bbc_links)))
bbc_players = pd.DataFrame({'rumors':bbc_rumors,'links':bbc_links,'date_posted':bbc_dates})
players = players.append(bbc_players,ignore_index=True)

# Telegraph
telegraph1 = requests.get('https://www.telegraph.co.uk/football-transfers/')
soapy = BeautifulSoup(telegraph1.content, 'html.parser')
link1 = [('https://www.telegraph.co.uk' + link.get('href')) for link in soapy.select('h3 a')]
rumor1 = [entry.get_text().strip() for entry in soapy.select('a.card__link span')[1:]]
drop_reporters_in_rumors(rumor1);
date1 = [date.get_text().split(',')[0] for date in soapy.select('div time')[1:]]
telegraph1_data = pd.DataFrame({'rumors':rumor1,'links':link1,'date_posted':date1})
players = players.append(telegraph1_data,ignore_index=True)

# Telegraph pages 2-5
pages = [str(i) for i in range(2,6)]

reqs = 0;

for page in pages:
    response = requests.get('https://www.telegraph.co.uk/football-transfers/page-' + page)
    sleep(randint(8,15))
    reqs += 1
    if reqs > 72:
            warn('Number of requests was greater than expected.')
            break
    soupy = BeautifulSoup(response.content, 'html.parser')
    link = [('https://www.telegraph.co.uk' + link.get('href')) for link in soupy.select('h3 a')]
    rumor = [entry.get_text().strip() for entry in soupy.select('a.card__link span')]
    drop_reporters_in_rumors(rumor);
    date = [date.get_text().split(',')[0] for date in soupy.select('div time')]
    telegraph_players = pd.DataFrame({'rumors':rumor,'links':link,'date_posted':date})
    players = players.append(telegraph_players,ignore_index=True)
print(players)
