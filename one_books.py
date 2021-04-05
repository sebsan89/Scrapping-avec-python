"""
This code is used to retrieve the data of a book on Booktoscrapp.com
"""

import requests
from bs4 import BeautifulSoup
import os


def scrapp_only_book(response):
    """book data recovery function

    Args:
        response ([variable]): [book url]

    Returns:
        [dictionary]: [dictionary containing all the data of the book]
    """
    soup = BeautifulSoup(response.text, 'lxml')
    dico = {} # dictionary receiving all the information from the book
    table = soup.article.findAll('tr')
    dico_table = {} # dictionary receiving certain data contained in an html table
    for line in table:
        key = line.find('th').text
        value = line.find('td').text
        dico_table[key] = value

    # Data retrieved and organized in the "dico" dictionary
    dico["product_page_url"] = response.url
    dico["universal_ product_code (upc)"] = dico_table.get("UPC")
    dico["title"] = soup.article.find('h1').text
    dico["price_including_tax"] = dico_table.get("Price (incl. tax)")
    dico["price_excluding_tax"] = dico_table.get("Price (excl. tax)")
    dico["number_available"] = dico_table.get("Availability")
    try:
        description = soup.article.find('div', {'id': 'product_description'})
        dico["product_description"] = description.next_sibling.next_sibling.text.replace(';', ',')
    except AttributeError:
        dico["product_description"] = ""
    category = soup.find('ul', {'class': 'breadcrumb'}).find('li').next_sibling.next_sibling
    dico["category"] = category.next_sibling.next_sibling.text.replace('\n', '')

    rate = {"Zero": "0", "One": "1", "Two": "2", "Three": "3", "Four": "4", "Five": "5"}
    tag = soup.find('p', {'class': 'star-rating'})
    tag = tag['class'].pop(1)
    number_rate = rate[tag]
    dico["review_rating"] = number_rate
    url_image = soup.article.find('div', {'class': 'thumbnail'}).find('img').get('src')
    dico["image_url"] = url_image.replace('../..', 'http://books.toscrape.com')

    # added images with UPC as name in separate folders by category
    img_data = requests.get(dico["image_url"]).content
    if not os.path.exists(dico["category"]):
        os.makedirs(dico["category"])
        os.chdir(dico["category"])
        with open(dico["universal_ product_code (upc)"] + ".jpg", 'wb') as img:
            img.write(img_data)
        os.chdir('..')

    else:
        os.chdir(dico["category"])
        with open(dico["universal_ product_code (upc)"] + ".jpg", 'wb') as img:
            img.write(img_data)
        os.chdir('..')
        
    return dico
def convert_to_csv(dico):
    """[retrieving values ​​from the dictionary in a list before being written to the csv file]

    Args:
        dico ([dictionary]): [dictionary containing all the data of the book]

    Returns:
        [string]: [data converted into a readable format in CSV]
    """
    value = list(dico.values())
    value = "; ".join(value)
    value = str(value)
    return value
def save_in_csv(data_converted, dico, file_name):
    """[Creating the csv file and writing the data]

    Args:
        data_converted ([string]): [data converted into a readable format in CSV]
        dico ([dictionnary]): [allows you to easily retrieve the name of the category]
    """
    key = list(dico.keys())
    key = "; ".join(key)
    if not os.path.exists(file_name):
        with open(file_name, 'w', encoding="utf-8") as file:
            file.write(key + "\n" + data_converted)
    else:
        with open(file_name, 'a', encoding="utf-8") as file:
            file.write(data_converted)
    
if __name__ == "__main__":
    """launch function
    """
    url = "http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html"
    response = requests.get(url)
    response.encoding = 'utf-8'
    print("Data Extraction on the site")
    dico = scrapp_only_book(response) # data Extraction
    print("Data Transformation in CSV format")
    csv = convert_to_csv(dico) # Data Transformation
    file_name = str(dico["title"]) + '.csv'
    print("Load data in " + file_name)
    save_in_csv(csv, dico, file_name) # Load data in CSV
