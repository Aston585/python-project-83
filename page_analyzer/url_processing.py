from urllib.parse import urlparse, urlunparse
import validators


def deco_removing_duplicate_slashes(func):
    def inner(component):
        split_component = component.split('/')
        component_without_slashes = '/'.join([x for x in split_component if x])
        return func(component_without_slashes)
    return inner


def deco_case_normalization(func):
    def inner(component):
        return func(component.lower())
    return inner


def deco_removing_spaces(func):
    def inner(component):
        split_component = component.split(' ')
        return func(''.join(split_component))
    return inner


@deco_case_normalization
@deco_removing_spaces
@deco_removing_duplicate_slashes
def normalyze_component(component):
    return component


def processing_url(url):
    url_parse = urlparse(url)
    netloc = normalyze_component(url_parse.netloc)
    path = normalyze_component(url_parse.path)
    if not netloc:
        return urlunparse([url_parse.scheme, path, '', '', '', ''])
    return urlunparse([url_parse.scheme, netloc, path, '', '', ''])


def normalyze_url(url):
    url = processing_url(url)
    url_parse = urlparse(url)
    return urlunparse([url_parse.scheme, url_parse.netloc, '', '', '', ''])


def validate_url(url):
    if len(url) < 255 and validators.url(url):
        return True
    return False


# url_test1 = 'https:/// rU.HexLet .iO //projects/83'
# url_test2 = 'https://rU.HexLet .iO //projects/83/'
# url_test3 = 'https://ru.hexlet.io/projects/83'
# url_test4 = 'https://ru.hexlet.io/projects/83'
# expected_url = 'https://ru.hexlet.io/projects/83'

# assert processing_url(url_test1) == expected_url
# assert processing_url(url_test2) == expected_url
# assert processing_url(url_test3) == expected_url
# assert processing_url(url_test4) == expected_url
