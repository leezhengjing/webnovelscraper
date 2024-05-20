import requests
from bs4 import BeautifulSoup
import csv

URL = "https://www.fortuneeternal.com/novel/i-became-a-flashing-genius-at-the-magic-academy-raw-novel/chapter-140/"
html_text = requests.get(URL).text
soup = BeautifulSoup(html_text, 'lxml')
original = soup.findAll('p')
# convert the original to one string without the </sentence/> tags

original_string = ''
for sentence in original:
    original_string += sentence.text
    original_string += ' '

#export as csv
with open('original.csv', 'w',encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow([original_string])
