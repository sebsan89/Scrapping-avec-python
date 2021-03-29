import requests
from bs4 import BeautifulSoup

import one_books as o_book



def books_in_category(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    articles = soup.findAll('article')
    list_books_url = []
    for article in articles:
        list_books_url.append(article.find('a')['href'].replace('../../..', 'http://books.toscrape.com/catalogue'))
    return list_books_url

def pagination(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    number_results = soup.find('form', {'class': 'form-horizontal'}).find('strong').text
    number_results = int(number_results)
    list_url = [response.url]
    if number_results >= 20:
        number_page = (number_results // 20) + 1
        for i in range(2, 1 + number_page):
                list_url.append(response.url.replace('index.html', '') + 'page-' + str(i) + '.html')
    url_books = []
    for books in list_url:
        url_books = url_books + (books_in_category(books))
    return url_books

def save_in_csv_category(data_converted, dico):
    file_name = str(dico["title"]) + '.csv'
    key = list(dico.keys())
    key = "; ".join(key)
    with open(file_name, 'w', encoding="utf-8") as file:
        file.write(key + "\n" + data_converted)
    print("Save in " + file_name)

if __name__ == "__main__":
    url = "http://books.toscrape.com/catalogue/category/books/fiction_10/index.html"
    urls = pagination(url)
    for book_url in urls:
        response = requests.get(book_url)
        response.encoding = 'utf-8'
        dico = o_book.scrapp_only_book(response) # data recovery
        csv = o_book.convert_to_csv(dico) + "\n" # Data transformation
        name_file = str(dico["category"]) + '.csv'
        o_book.save_in_csv(csv, dico, name_file) # Save data in CSV