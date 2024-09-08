import requests
from bs4 import BeautifulSoup
import time
import pandas

#Gets the URL to be scraped and takes the page content as its input
URL = "https://www.pro-football-reference.com/players/"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

#Finds the content div and gets the contents of an unordered list
#These list items contain hrefs to help build links to NFL players sorted by an index of letters
results = soup.find(id="content")
items = results.find("ul", class_="page_index")

#Loops through each list item and builds a link to a letter
for item in items:
    
    #Gets the link to each letter and parses through it
    link = "https://www.pro-football-reference.com" + str(item.find('a', href=True)['href'])
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")

    #Gets the link of each player that is currently active
    players = soup.find(id="div_players")
    for bold in players.find_all('b'):
        link = "https://www.pro-football-reference.com"  + str(bold.find('a', href = True)['href'])

    #Sleeps to avoid rate limiting as per PFR scraping guidlines
    time.sleep(4)



