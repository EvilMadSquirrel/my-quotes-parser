import requests
from bs4 import BeautifulSoup
import json


def get_html(page_number=1):
    num = page_number
    response = requests.get(f'https://quotes.toscrape.com/page/{num}/')
    response.raise_for_status()
    return (response.text, True)


def parse_html(page_number=1):
    raw_html = get_html(page_number)[0]
    soup = BeautifulSoup(raw_html, 'html.parser')
    quotes = soup.find_all('div', {'class': 'quote'})
    page_result = {'quotes': []}
    for quote in quotes:
        text: str = quote.find('span', {'class': 'text'}).text
        author = quote.find('small', {'class': 'author'}).text
        raw_tags = quote.find_all('a', {'class': 'tag'})
        tags = []
        for tag in raw_tags:
            tags.append(tag.text)
        page_result['quotes'].append(
            {'text': text, 'author': author, 'tags': tags})
    return page_result


def main():

    results = []
    for page in range(1, 11):
        result = parse_html(page)
        results.append(result)

    with open('results.json', 'w') as file:
        json.dump(results, file)


if __name__ == '__main__':
    main()
