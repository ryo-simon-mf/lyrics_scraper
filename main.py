import os
import csv
import time
import datetime
import re
import requests
import urllib
import urllib.request
import pandas as pd
from bs4 import BeautifulSoup

def Hinichi():
    Month = str(datetime.datetime.now().month).zfill(2)
    Day = str(datetime.datetime.now().day).zfill(2)
    Minute= str(datetime.datetime.now().minute).zfill(2)
    Hour = str(datetime.datetime.now().hour).zfill(2)
    return(str(Month + Day + Hour + Minute))

now = Hinichi()

ARTIST = 'SAKANA'

# df prepare
dl_file =  '/content/'+ ARTIST + now +'.csv' 
file = open(dl_file, 'w')
w = csv.writer(file)


# first Row Init
add_row = []
add_row.append('Track Name')
add_row.append('Artist Name')
add_row.append('Lyrics')
add_row.append('Composed')
add_row.append('URL')
add_row.append('LYRICS')
w.writerow(add_row)


#Get artist url


# search Sakanaction ad Uta-Net Kashi_Kensaku
url = 'https://www.uta-net.com/search/?Aselect=1&Keyword=%E3%82%B5%E3%82%AB%E3%83%8A%E3%82%AF%E3%82%B7%E3%83%A7%E3%83%B3&Bselect=3&x=0&y=0'
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; NP06; rv:11.0) like Gecko",
        }


request = urllib.request.Request(url=url, headers=headers)
response = urllib.request.urlopen(request)
soup = BeautifulSoup(response,"html.parser")
response.close()

contents = soup.find('p', id='flash_area') # get lyrics
get1 = soup.find_all('td', class_='side td1') # get artist lyric composite name
get2 = soup.find_all('td', class_='td2') # get artist lyric composite name
get3 = soup.find_all('td', class_='td3') # get artist lyric composite name
get4 = soup.find_all('td', class_='td4') # get artist lyric composite name


songs = len(get1)

for i in range(songs):
    song_name = get1[i].get_text()
    song_artist = get2[i].get_text()
    song_lyrics = get3[i].get_text()
    song_composed = get4[i].get_text()
    song_url = 'https://www.uta-net.com/' + get1[i].find('a').get("href")

    song_request = urllib.request.Request(url=song_url, headers=headers)
    song_response = urllib.request.urlopen(song_request)
    song_soup = BeautifulSoup(song_response,"html.parser")
    song_response.close()

    LYRICS = song_soup.find('div', id='kashi_area') .get_text()

    print(song_name, song_artist, song_lyrics, song_composed, song_url, LYRICS)

    add_row = []
    add_row.append(song_name)
    add_row.append(song_artist)
    add_row.append(song_lyrics)
    add_row.append(song_composed)
    add_row.append(song_url)
    add_row.append(LYRICS)
    w.writerow(add_row)

file.close()


get_matrix = dl_file
df = pd.read_csv(get_matrix)
NUM = len(df['LYRICS'])

lyrics_all = ''

for S_NUM in range(NUM):
    lyrics_all = lyrics_all + df['LYRICS'][S_NUM]

f = open("/content/" + ARTIST+ "_LYRICS"+ now +'.txt', "w")
f.write(lyrics_all)
f.close()
