import requests
from bs4 import BeautifulSoup


URL = "https://www.pro-football-reference.com/players/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="content")
job_elements = results.find("ul", class_="page_index")

for job_element in job_elements:
    print ("Found the URL:", job_element.find('a', href=True)['href'])
