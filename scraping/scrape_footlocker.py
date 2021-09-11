from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from time import sleep

driver = webdriver.Chrome(executable_path='../../../../Webdriver/bin/chromedriver')

categories = {
             "mens" : "https://www.footlocker.ca/en/category/mens/shoes.html",
             "womens" : "https://www.footlocker.ca/en/category/womens/shoes.html",
             "kids" : "https://www.footlocker.ca/en/category/kids/shoes.html"
}

def scrape_category(category: str):
    driver.get(categories.get(category))
    sleep(3)

def main():
    for category in categories.keys():
        print(category)
        scrape_category(category)

main()
