import requests
import bs4
import re
import csv, os
from game import Game
import pandas as pd
from matplotlib import pyplot as plt


url = 'https://steamcharts.com/top'
steamUrl = 'https://store.steampowered.com'

res = requests.get(url)

res.raise_for_status()

soup = bs4.BeautifulSoup(
    res.text, features="html.parser", from_encoding='utf-8')

games = []

names = []
appUrl = []
peakPlayers = []
totalHours = []
prices = []

columns = ['name', 'peakPlayers', 'totalHours', 'price']
df = pd.DataFrame(columns=columns)

names.extend(soup.select('.game-name a'))
peakPlayers.extend(soup.select('peak-concurrent'))
totalHours.extend(soup.select('player-hours'))


def loadDataFromSteamSpy():
    for i in range(1, 10):
        nurl = url+'/p.' + str(i)
        print(nurl)
        nres = requests.get(nurl)
        soup = bs4.BeautifulSoup(
            nres.text, features="html.parser", from_encoding="utf-8")
        names.extend(soup.select('.game-name a'))
        peakPlayers.extend(soup.select('td.peak-concurrent'))
        totalHours.extend(soup.select('td.player-hours'))


def WriteDicToCSV(csv_file,csv_columns,dict_data):
    try:
        with open(csv_file,'w',encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile,fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)
    except:
        print("se mamut")



def GetClasification(pagetext):
    soup = bs4.BeautifulSoup(pagetext, features="html.parser",from_encoding="utf-8")

    return ''

def createGamesData():
    r = min(len(names), len(peakPlayers), len(totalHours))

    for i in range(0, r):

        g = Game()
        g.name = names[i].getText().strip()
        g.appUrl = names[i].get('href')
        g.peakPlayers = int(peakPlayers[i].getText().strip())
        g.hoursPlayed = int(totalHours[i].getText().strip())

        res = requests.get(steamUrl+g.appUrl)
        soup = bs4.BeautifulSoup(res.text, features="html.parser", from_encoding="utf-8")
        prices = soup.select('div.game_purchase_price.price')
        genresBlock = soup.select('div.details_block')
        genres = []
        genreBlock = []

        games.append(g)

        if len(genresBlock) > 0:
            genreBlock = genresBlock[0]
            for b in genresBlock:
                if b.find('<b>Genre:</b>') != -1:
                    genreBlock = b
                    break

            soup = bs4.BeautifulSoup(str(genreBlock),features="html.parser", from_encoding="utf-8")
            genres = [ge.getText() for ge in soup.select('div.details_block>a')]
            g.genres = genres


        if len(prices) > 0:
            p = prices[0].getText().strip()

            matches = re.findall(r'\d+\.?\d+', p)
            if len(matches) > 0:

                p = matches[0]
            else:
                p = 0
            g.price = p



loadDataFromSteamSpy()
createGamesData()


currentPath = os.getcwd()
csv_file = "gamesData.csv"
WriteDicToCSV(csv_file,games[0].to_dict().keys(), [g.to_dict() for g in games])

df = pd.DataFrame.from_records([g.to_dict() for g in games])


