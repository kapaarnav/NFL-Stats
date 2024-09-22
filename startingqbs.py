import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

#Grabs the URL with links to starting QB's
url = requests.get("https://www.profootballnetwork.com/nfl-starting-quarterbacks/")
soup = BeautifulSoup(url.content, 'html.parser')

#Makes sure the status of the page is valid
if url.status_code == 200:
    soup = BeautifulSoup(url.text, 'html.parser')
else:
    print(f"Failed to retrieve data: {url.status_code}")
