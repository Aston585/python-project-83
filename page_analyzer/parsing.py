import requests
from bs4 import BeautifulSoup


def request_site_status(url, timeout=3):
    try:
        responce = requests.get(url, timeout=timeout)
        return responce.status_code

    except requests.exceptions.RequestException:
        return None


class Parser:
    def __init__(self, url):
        self.responce = requests.get(url)
        self.soup = BeautifulSoup(self.responce.text, 'lxml')

    def get_tag_h1(self):
        if tag_h1 := self.soup.find('h1'):
            return tag_h1.get_text(strip=True)
        else:
            return ''

    def get_tag_title(self):
        if tag_title := self.soup.find('title'):
            return tag_title.get_text(strip=True)
        else:
            return ''

    def get_attr_content_from_tag_meta(self):
        if meta := self.soup.find('meta', attrs={"name": "description"}):
            return meta.get('content')
        else:
            return ''
