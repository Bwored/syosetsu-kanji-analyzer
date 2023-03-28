import re
import csv
import requests
from bs4 import BeautifulSoup

from collections import Counter

def main():
    # Menu to select the function to run
    print('0. Scrape Ncode')
    print('1. Extract Japanese words and kanji from a text file')
    print('2. Sort Japanese words and kanji by frequency')
    print('3. Lookup Kanji')
    
    choice = input('Enter your choice: ')
    
    if choice == '0':
        fiction = input('Enter fiction code:')
        chapter = input('Enter chapter number: ')
        scrape_ncode(fiction,chapter)
    elif choice == '1':
        extract_just_kanji()
    elif choice == '2':
        sort_just_kanji('result/just_kanji.txt')
    elif choice == '3':
        lookup_kanji()
    else:
        print('')
    
def scrape_ncode(fic,chapter):
    """
        Scrapes the syosetsu novel from the url
    """
    # Create a header to pass to the request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
    }
    url = f'https://ncode.syosetu.com/{fic}/{chapter}/'
    # Create a http request
    response = requests.get(url, headers=headers)
    
    # Check response status and handle errors
    if response.status_code != 200:
        print(f'Error: {response.status_code}')
        return
    
    # Extract html from the response
    html = response.text
    
    # Beautiful soup
    soup = BeautifulSoup(html, 'html.parser')
    
    # get title
    novel_title = soup.find('a', href=f'/{fic}/').text
    
    # get subtitle
    novel_subtitle = soup.find('p', class_="novel_subtitle").text
    
    # get chapter index
    novel_no = soup.find('div', id="novel_no").text
    
    # get class 'novel_view'
    novel_view = soup.find('div', class_='novel_view')
    paragraphs = novel_view.find_all('p', id=re.compile('L\d+'))


    # paragraphs to string
    paragraphs = [paragraph.text.replace('\u3000', '') for paragraph in paragraphs]
    
    # clean up paragraphs
    paragraphs = [paragraph for paragraph in paragraphs if paragraph != '']

    with open('result/text.txt', 'w', encoding='utf-8') as f:
        for paragraph in paragraphs:
            f.write(paragraph + '\n')
    
    print(f'Finished extracting text from {novel_title} chapter {novel_no} titled {novel_subtitle}')

def extract_just_kanji():
    """
        Extracts all the kanji from a text file and writes it to a file
    """
    with open('result/text.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    just_kanji = re.findall(r'[\u4e00-\u9fff]+', text)
    with open('result/just_kanji.txt', 'w', encoding='utf-8') as f:
        for word in just_kanji:
            f.write(word + '\n')

def sort_just_kanji(file_path):
    """
        Sorts the kanji by frequency and writes it to a CSV file
    """
    
    with open(file_path, 'r', encoding='utf-8') as f:
        just_kanji = f.read()
    just_kanji = list(just_kanji)
    
    # create Counter object
    freq = Counter(just_kanji)

    # remove duplicates
    freq = {k: v for k, v in sorted(freq.items(), key=lambda item: item[1], reverse=True)}
    
    # write results to CSV file
    with open('result/sorted_kanji.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Character', 'Count'])
        for char, count in freq.items():
            writer.writerow([char, count])

def lookup_kanji():
    """
        Add kanji meaning, reading, and etc to CSV file using KanjiApi.dev
    """
    result = []
    with open('result/sorted_kanji.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        kanji = [row[0] for row in reader]
        count = [row[1] for row in reader]
    
    # remove '\n' from kanji
    kanji = [char.replace('\n', '') for char in kanji]
        
    # clean up kanji
    kanji = [char for char in kanji if len(char) == 1]
    
    for char in kanji:
        url = f'https://kanjiapi.dev/v1/kanji/{char}'
        response = requests.get(url)
        result.append(response.json())
        
        # progress bar
        print(f'Progress     : {round((kanji.index(char) + 1) / len(kanji) * 100, 2)}%', end='\r')
    
    with open('result/kanji_with_meanings.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Character', 'Meaning', 'On Reading', 'Kun Reading', 'JLPT Level'])
        for i in range(len(result)):
            writer.writerow([result[i]['kanji'], result[i]['meanings'], result[i]['on_readings'], result[i]['kun_readings'], result[i]['jlpt']])
            # writer.writerow([data['kanji'], data['jlpt'], data['meanings'], data['on_readings'], data['kun_readings']])

def create_anki_deck():
    """
        Creates an Anki deck from the kanji_with_meanings.csv file
    """
    print('Not yet implemented')

main()
