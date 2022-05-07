from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import requests
import numpy as np
import csv

def get_av(url):
    try:
        page = urlopen(url).read()
    except:
        print("AHHH")
        return 0
    soup = BeautifulSoup(page)

    table = soup.find("tbody")
    rows = table.find_all('tr')

    avs = []
    for row in rows:
        if (row.find('th', {"scope":"row"}) != None):
            cell = row.find("td", {"data-stat": "av"})
            a = cell.text.strip().encode()
            try:
                avs.append(int(a.decode("utf-8")))
            except:
                avs.append(0)

    return np.mean(avs)

letters = ["X","Y","Z"]
for letter in letters:
    url = "https://www.pro-football-reference.com/players/"+letter+"/"
    page = urlopen(url).read()
    soup = BeautifulSoup(page)
    results = soup.find(id='div_players')
    players = results.find_all("p")

    name_av = []
    av = 0
    for player in players:
        text = player.getText()
        a = text.index("(")-1
        b = text.index(")")+1
        name = text[:a]
        years = text[b+1:]
        print(years)
        if int(years[0:4]) > 2008:
            link = player.find('a', href=True)['href']
            full_link = "https://www.pro-football-reference.com" + link
            print(name, years, full_link)
            try:
                av = get_av(full_link)
            except:
                print("AHHH")
                av = -1
            name_av.append([name,years,av])
            print(av)

    with open('result' + letter + '.csv','w') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Years', 'AV'])
        writer.writerows(name_av)
