from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup
from time import sleep
import requests
import json

import cProfile

driver = webdriver.Chrome(ChromeDriverManager().install())

categories = {
            "mens" : "https://www.footlocker.ca/en/category/mens/shoes.html",
            "womens" : "https://www.footlocker.ca/en/category/womens/shoes.html",
            "kids" : "https://www.footlocker.ca/en/category/kids/shoes.html"
}

shoe_list = []

def last_page(driver, html):
    soup = BeautifulSoup(html, 'lxml')
    soup = soup.find('ul', 'row row--always gutterH')
    count = 0

    try:
        buttons = soup.children
        for button in buttons:
            count += 1
    except AttributeError:
        pass

    next_page_button = '//*[@id="main"]/div/div[2]/div/section/div/div[2]/nav/ul/li[' + str(count-1) + ']/a'

    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, next_page_button))).click()
        print("Next Page...")
    except (NoSuchElementException, TimeoutException):
        return True

    return False

def write_to_json(file_data, filename='outfile.json'):
    with open(filename, 'r+') as file:
        json.dump(file_data, file, indent = 4)

def scrape_shoe(url, name, colours):
    res = requests.get(url)

    soup = BeautifulSoup(res.text, 'lxml')
    try:
        data = str(soup.find_all('script', type='application/ld+json')[1])[42:-15]
    except IndexError:
        return

    json_data = json.loads(data)

    try:
        brand = json_data['brand']
    except KeyError:
        brand = name.split()[0]

    shoe_obj = {
        'name' : name,
        'colours' : colours,
        'description' : json_data['description'],
        'image' : json_data['image'],
        'brand' : brand,
        'model' : json_data['model'],
        'sku' : json_data['sku'],
        'condition' : json_data['itemCondition'],
        'url' : json_data['@id'],
        'offers' : json_data['offers']
    }
    shoe_list.append(shoe_obj)

def scrape_category(category):
    driver.get(categories.get(category))

    while True:
        sleep(2)
        html = driver.page_source

        soup = BeautifulSoup(html, 'lxml')
        shoes = soup.find_all('li', 'product-container col')

        for shoe in shoes:
            name = shoe.find('span', 'ProductName-primary').text
            print(name)
            colours = shoe.find('span', 'ProductName-alt').text[6:].split('/')
            links = [a['href'] for a in shoe.select('a[href]') if a.text]

            for link in links:
                url = "https://www.footlocker.ca" + link
                scrape_shoe(url, name, colours)
        if last_page(driver, html):
            write_to_json(shoe_list)
            break

def main():
    for category in categories.keys():
        print("Scraping " + category + "...")
        scrape_category(category)

main()
