import requests
from bs4 import BeautifulSoup


def parse_html(url):
    response = requests.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
 
    h1_tag = soup.find('h1')
    h1 = h1_tag.string if h1_tag else None

    title_tag = soup.find('title')
    title = title_tag.string if title_tag else None
    
    meta_tag = soup.find('meta', attrs={'name': 'description'})
    description = meta_tag['content'] if meta_tag else None
    
    if description:
        description = description[:255]
    
    return {
        'status_code': response.status_code,
        'h1': h1[:255] if h1 else None,
        'title': title[:255] if title else None,
        'description': description
    }