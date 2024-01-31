from urllib.parse import urlparse
import validators


def normalyze_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


def validate_url(url):
    if len(url) < 255 and validators.url(url):
        return True
    return False
