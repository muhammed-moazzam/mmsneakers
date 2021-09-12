from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup
from time import sleep
import requests

driver = webdriver.Chrome(executable_path='../../../../Webdriver/bin/chromedriver')

categories = {
             "mens" : "https://www.footlocker.ca/en/category/mens/shoes.html"
             # "womens" : "https://www.footlocker.ca/en/category/womens/shoes.html",
             # "kids" : "https://www.footlocker.ca/en/category/kids/shoes.html"
}

def scrape_shoe(url):
    res = requests.get(url)

    soup = BeautifulSoup(res.text, 'lxml')
    try:
        data = soup.find_all('script', type='application/ld+json')[1]
    except IndexError:
        return

    print(data)


def scrape_category(category: str):
    driver.get(categories.get(category))
    html = driver.page_source

    soup = BeautifulSoup(html, 'lxml')
    shoes = soup.find_all('li', 'product-container col')

    for shoe in shoes:
        print(shoe.find('span', 'ProductName-primary').text)
        links = [a['href'] for a in shoe.select('a[href]') if a.text]

        for link in links:
            url = "https://www.footlocker.ca" + link
            scrape_shoe(url)

def main():
    for category in categories.keys():
        print(category)
        scrape_category(category)

main()
