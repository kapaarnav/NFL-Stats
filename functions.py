import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

curryear = 2024

def send_to_csv(player_link, csv_file, tbody_id):

    #Gets the table, apply below
    url = requests.get(player_link)
    soup = BeautifulSoup(url.content, 'html.parser')

    if url.status_code == 200:
        soup = BeautifulSoup(url.text, 'html.parser')
    else:
        print(f"Failed to retrieve data: {url.status_code}")
        return

    name = soup.find(id="meta").find('h1').find('span').text

    print(name)
    # Find the tbody within the 'rushing_and_receiving' table
    tbody = soup.find(id=tbody_id)
    if tbody is None:
        return
    tbody = tbody.find('tbody')

    # Extract rows and determine the number of columns dynamically
    data = []

    # Go through each row
    for row in tbody.find_all('tr'):

        # Extract the 'th' element (year or identifier) and the 'td' elements (data)
        year = row.find('th').get_text(strip=True)[0:4]
        if year.isdigit() and int(year) < curryear - 5 or not year.isdigit():
            continue
        cells = [cell.get_text(strip=True) for cell in row.find_all('td')]

        # Prepend the year to the row data (so the year is the first column)
        row_data = [name, year] + cells
        data.append(row_data)

    # Convert the data into a pandas DataFrame and sends it to the CSV
    df = pd.DataFrame(data)
    df.to_csv(csv_file, mode = 'a', index= False, header=False)
    time.sleep(4)

#Sets the headers for the tops of the csv files per position
def set_headers(link, tbody_id):
    
    #Gets the url for a player; 5 preset players per position have been chosen
    url = requests.get(link[0])
    soup = BeautifulSoup(url.content, 'html.parser')

    if url.status_code == 200:
        soup = BeautifulSoup(url.text, 'html.parser')
    else:
        print(f"Failed to retrieve data: {url.status_code}")
        return
    
    columns = []

    #Gets the table body and one row within the table
    tbody = soup.find(id=tbody_id).find('tbody')
    row = tbody.find('tr')

    #Set the columns for one row in the table
    cells = [cell.get_text(strip=True) for cell in row.find_all('td')]
    columns = ['name', 'year'] + [cell['data-stat'] for cell in row.find_all('td')]
        
    #Sends the headers out to the given file
    df = pd.DataFrame(columns=columns)
    df.to_csv(link[1], index=False)
    time.sleep(4)