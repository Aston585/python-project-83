import requests
from bs4 import BeautifulSoup


class Parser:
    def __init__(self, url):
        self.response = requests.get(url, timeout=3)
        self.soup = BeautifulSoup(self.response.text, 'lxml')

    def get_site_status(self):
        return self.response.status_code

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
