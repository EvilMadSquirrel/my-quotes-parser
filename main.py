import requests
from bs4 import BeautifulSoup


def get_html(page_number=1):
    num = page_number
    response = requests.get(f'https://quotes.toscrape.com/page/{num}/')
    response.raise_for_status()
    return response.text


def main():
    raw_html = get_html(1)
    soup = BeautifulSoup(raw_html, 'html.parser')
    print(soup.prettify())


if __name__ == '__main__':
    main()
