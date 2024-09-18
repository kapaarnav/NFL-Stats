import requests
from bs4 import BeautifulSoup
import pandas as pd
import functions
import time

#Gets the URL to be scraped and takes the page content as its input
URL = "https://www.pro-football-reference.com/players/"
page = requests.get(URL)

#Makes sure the status of the page is valid
if page.status_code == 200:
    soup = BeautifulSoup(page.text, 'html.parser')
else:
    print(f"Failed to retrieve data: {page.status_code}")


#Finds the content div and gets the contents of an unordered list
#These list items contain hrefs to help build links to NFL players sorted by an index of letters
results = soup.find(id="content")
items = results.find("ul", class_="page_index")

curryear = 2024
offense = {"(QB)": [], "(RB)": [], "WR": [], "TE": [], "K": []}


#Uses one player from each position as examples to set the header for the CSV file per position
header_links = [("https://www.pro-football-reference.com/players/H/HenrDe00.htm", "data/RB.csv"),
              ("https://www.pro-football-reference.com/players/M/MahoPa00.htm", "data/QB.csv"),
                ("https://www.pro-football-reference.com/players/J/JeffJu00.htm", "data/WR.csv"),
                  ("https://www.pro-football-reference.com/players/K/KelcTr00.htm", "data/TE.csv"),
                   ("https://www.pro-football-reference.com/players/T/TuckJu00.htm", "data/K.csv")]
functions.set_headers(header_links[0], "rushing_and_receiving")
functions.set_headers(header_links[1], "passing")
functions.set_headers(header_links[2], "receiving_and_rushing")
functions.set_headers(header_links[3], "receiving_and_rushing")
functions.set_headers(header_links[4], "kicking")


#Loops through each list item and builds a link to a letter
for item in items:
    
    #Gets the link to each letter and parses through it
    link = "https://www.pro-football-reference.com" + str(item.find('a', href=True)['href'])
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")

    #Gets the link of each player that is currently active
    players = soup.find(id="div_players")
    for bold in players.find_all('b'):

        #Gets the player link and their position
        link = "https://www.pro-football-reference.com"  + str(bold.find('a', href = True)['href'])
        position = bold.contents[-1].strip()

        if position == "(QB)":
            functions.send_to_csv(link, "data/QB.csv", "passing")
        elif position == "(RB)":
            functions.send_to_csv(link, "data/RB.csv", "rushing_and_receiving")
        elif position == "(WR)":
            functions.send_to_csv(link, "data/WR.csv", "receiving_and_rushing")
        elif position == "(TE)":
            functions.send_to_csv(link, "data/TE.csv", "receiving_and_rushing")
        elif position == "(K)":
            functions.send_to_csv(link, "data/K.csv", "kicking")        
        
    #Sleeps to avoid rate limiting as per PFR scraping guidlines
    time.sleep(4)
