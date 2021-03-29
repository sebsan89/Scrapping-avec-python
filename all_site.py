"""
This code is used to retrieve the data of all book for all category on Booktoscrapp.com
"""
import requests
from bs4 import BeautifulSoup
import one_category as o_category

def category(url):
    """[summary]

    Args:
        url ([string]): [url website]

    Returns:
        [list]: [list url for all category]
    """
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    links_category = soup.find('ul', {'class': 'nav-list'}).findAll('li')
    liste = []
    for link_category in links_category:
        href = "http://books.toscrape.com/" + link_category.find('a')['href'].replace('..', '')
        liste.append(href)
    del liste[0]
    return liste

if __name__ == "__main__":
    WEBSITE = "http://books.toscrape.com"
    urls_all_category = category(WEBSITE)

    for url_category in urls_all_category:
        o_category.main(url_category)
