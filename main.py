from pandas.core.frame import DataFrame
import requests
from bs4 import BeautifulSoup
import json
from unidecode import unidecode
import pandas as pd


def get_html(page_number=1):
    num = page_number
    response = requests.get(f'https://quotes.toscrape.com/page/{num}/')
    response.raise_for_status()
    return (response.text, True)


def parse_html(page_number=1):
    raw_html = get_html(page_number)[0]
    soup = BeautifulSoup(raw_html, 'html.parser')
    quotes = soup.find_all('div', {'class': 'quote'})
    page_result = []
    for quote in quotes:
        text: str = quote.find('span', {'class': 'text'}).text
        text = unidecode(text)
        author = quote.find('small', {'class': 'author'}).text
        author = unidecode(author)
        raw_tags = quote.find_all('a', {'class': 'tag'})
        tags = []
        for tag in raw_tags:
            tags.append(tag.text)
        page_result.append(
            {'text': text, 'author': author, 'tags': tags})
    return page_result


def main():
    results = []
    for page in range(1, 11):
        result = parse_html(page)
        data = pd.DataFrame(result)
        results.append(data)
    with pd.ExcelWriter('results.xlsx') as writer:
        for i in range(len(results)):
            results[i].to_excel(writer, sheet_name=f'Quotes_page{i}')


if __name__ == '__main__':
    main()
