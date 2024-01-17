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
        tag_h1 = self.soup.find('h1').get_text(strip=True)
        return tag_h1 if tag_h1 else ''

    def get_tag_title(self):
        tag_title = self.soup.find('title').get_text(strip=True)
        return tag_title if tag_title else ''

    def get_attr_content_from_tag_meta(self):
        meta = self.soup.find('meta', attrs={"name": "description"})
        if not meta:
            return ''
        return meta.get('content')
