"""
This code is used to retrieve the data of all book for one category on Booktoscrapp.com
"""
import requests
from bs4 import BeautifulSoup
import one_books as o_book

def books_in_category(url_books):
    """listing books in category

    Args:
        url_books ([string]): [category page url]

    Returns:
        [list]: [urls of all books in the category]
    """
    response_cat = requests.get(url_books)
    response_cat.encoding = 'utf-8'
    soup = BeautifulSoup(response_cat.text, 'lxml')
    articles = soup.findAll('article')
    list_books_url = []
    for article in articles:
        href = article.find('a')['href'].replace('../../..', 'http://books.toscrape.com/catalogue')
        list_books_url.append(href)
    return list_books_url

def pagination(url):
    """[generate the urls of the pages of a category with pagination]

    Args:
        url ([string]): [url of a category for checking the existence of a pagination]

    Returns:
        [list]: [category pagination urls]
    """
    response_pag = requests.get(url)
    response_pag.encoding = 'utf-8'
    soup = BeautifulSoup(response_pag.text, 'lxml')
    number_results = soup.find('form', {'class': 'form-horizontal'}).find('strong').text
    number_results = int(number_results)
    list_url = [response_pag.url]
    if number_results >= 20:
        number_page = (number_results // 20) + 1
        for i in range(2, 1 + number_page):
            list_url.append(response_pag.url.replace('index.html', '') + 'page-' + str(i) + '.html')
    url_books = []
    for books in list_url:
        url_books = url_books + (books_in_category(books))
    return url_books

def main(URL_CATEGORY):
    print("urls search")
    urls = pagination(URL_CATEGORY)
    print("Data Extraction on the category")
    for book_url in urls:
        response = requests.get(book_url)
        response.encoding = 'utf-8'
        dico = o_book.scrapp_only_book(response) # data Extraction
        data_csv = o_book.convert_to_csv(dico) + "\n" # Data transformation
        name_file = str(dico["category"]) + '.csv'
        o_book.save_in_csv(data_csv, dico, name_file) # Load data in CSV
    print("Load data in " + name_file)
if __name__ == "__main__":
    main("http://books.toscrape.com/catalogue/category/books/fiction_10/index.html")