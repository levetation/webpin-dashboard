from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import requests
from django.http import HttpResponse
from django.core.cache import cache

## find the url
def get_favicon_url(url):

    # creates cache key
    cache_key = f'favicon_{url}'

    # checks for url in cache
    favicon_url = cache.get(cache_key)
    if favicon_url:
        return favicon_url
    
    # generates favicon from url
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    favicon_url = None
    for link in soup.find_all('link'):
        if link.get('rel') == ['shortcut', 'icon'] or link.get('rel') == ['icon']:
            favicon_url = link.get('href')
            break
    if favicon_url:
        parsed_favicon_url = urlparse(favicon_url)
        if not parsed_favicon_url.scheme:
            parsed_url = urlparse(url)
            base_url = parsed_url.scheme + "://" + parsed_url.netloc
            favicon_url = urljoin(base_url, favicon_url)
        # puts url in cache
        cache.set(cache_key, favicon_url)
    return favicon_url

## Grab the favicon url for the page
def get_favicon(request):
    url = request.GET.get('url')
    cache_key = f'favicon_{url}'
    favicon_url = cache.get(cache_key)
    if not favicon_url:
        favicon_url = get_favicon_url(url)
    if favicon_url:
        cache.set(cache_key, favicon_url)
        response = requests.get(favicon_url)
        return HttpResponse(response.content, content_type=response.headers['Content-Type'])
    else:
        return HttpResponse(status=404)
    
def url_name(url):
    url_list = url.split('/')
    if len(url_list) >= 1:
        fav_url = f"{url_list[2]}"
        return fav_url