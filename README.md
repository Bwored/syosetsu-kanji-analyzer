# Syosetsu Kanji Analyzer

This is a Python project i made for fun that scrapes a Japanese novel from [syosetsu](https://ncode.syosetu.com), extracts all the kanji from the text, sorts them by frequency, looks up their meanings and readings using [KanjiApi.dev](https://kanjiapi.dev/), and creates an Anki deck for learning them.

## Requirements

- Python 3
- Requests
- BeautifulSoup
- CSV

## Usage

Run the main.py file and follow the menu options:

0. Scrape Ncode: Enter the fiction code and chapter number of the novel you want to scrape. The text will be saved in a file called text.txt.
1. Extract Japanese words and kanji from a text file: Enter the name of the text file you want to extract kanji from. The kanji will be saved in a file called just_kanji.txt.
2. Sort Japanese words and kanji by frequency: Enter the name of the kanji file you want to sort by frequency. The sorted kanji will be saved in a file called sorted_kanji.csv.
3. Lookup Kanji: This will lookup the meanings and readings of the kanji in the sorted_kanji.csv file using KanjiApi.dev and save them in a file called kanji_with_meanings.csv.
4. Not implemented yet

## TODO(s)

* Lookup novel using title instead of code
* Select chapter based on title
* Feature set for words
* Anki deck!


## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
