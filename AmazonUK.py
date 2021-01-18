from Shop import Labels, Item, Shop
import urllib.request
from bs4 import BeautifulSoup
import requests
import chalk
import time
from amazoncaptcha import AmazonCaptcha
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime

#TODO: Add methods to work with page errors that may occur (such as 404)
#      Filter out products which go over max price range
#      Anything else that comes to mind :)
#      oh and maybe make another file for creating web browser -- just an idea

def AmazonUK():
    labels = Labels(750, "In stock.", ["out of stock", "unavailable"])

    items = []
    items.append(Item("asus", "Tuf", "3080", "https://www.amazon.co.uk/dp/B08HN37VQK"))
    items.append(Item("asus", "Tuf OC", "3080", "https://www.amazon.co.uk/dp/B08HN4DSTC"))
    items.append(Item("asus", "strix", "3080", "https://www.amazon.co.uk/dp/B08HN7VVLJ"))
    items.append(Item("asus", "strix oc", "3080", "https://www.amazon.co.uk/dp/B08HN6KYS3"))
    items.append(Item("evga", "ftw3", "3080", "https://www.amazon.co.uk/dp/B08HGBYWQ6"))
    items.append(Item("evga", "xc3", "3080", "https://www.amazon.co.uk/dp/B08HGLN78Q"))
    items.append(Item("evga", "xc3 black", "3080", "https://www.amazon.co.uk/dp/B08HH1BMQQ"))
    items.append(Item("evga", "xc3 ultra", "3080", "https://www.amazon.co.uk/dp/B08HJ9XFNM"))
    items.append(Item("gigabyte", "aorus master", "3080", "https://www.amazon.co.uk/dp/B08KHLDS72"))
    items.append(Item("gigabyte", "eagle oc", "3080", "https://www.amazon.co.uk/dp/B08HHZVZ3N"))
    items.append(Item("gigabyte", "gaming oc", "3080", "https://www.amazon.co.uk/dp/B08HLZXHZY"))
    items.append(Item("gigabyte", "vision oc", "3080", "https://www.amazon.co.uk/dp/B08KH7RL89"))
    items.append(Item("msi", "gaming x trio", "3080", "https://www.amazon.co.uk/dp/B08HM4V2DH"))
    items.append(Item("msi", "ventus 3x oc", "3080", "https://www.amazon.co.uk/dp/B08HM4M621"))
    items.append(Item("AmazonBasics", "Double Braided Nylon", "USB", "https://www.amazon.co.uk/dp/B0753R2TWC"))

    shop = Shop("Amazon", '£', labels, items)
    return shop

def checkAmazonUKStock():
    PATH = "G:\chromedriver\87\chromedriver" #WILL NEED TO CHANGE SO CAN WORK ON ALL SYSTEMS
    driver = webdriver.Chrome(executable_path=PATH)
    driver.minimize_window()
    shop = AmazonUK()
    inc = 0
    while(True):
        #Reset increment if gone over all items
        if inc >= len(shop.items):
            inc = 0

        url = shop.items[inc].url
        driver.get(url)

        time.sleep(0.30)

        sentence = ""
        sentence += "[" + chalk.yellow(datetime.now().strftime('%H:%M:%S')) + "] " + chalk.bold(chalk.magenta(shop.name)) + " | "
        sentence += shop.items[inc].brand + " " + shop.items[inc].model + " " + shop.items[inc].series + " || "

        try:
            availability = driver.find_element_by_id('availability')
            if availability.text != shop.labels.inStock:
                sentence += chalk.red("Out of Stock")
            else:
                price = driver.find_element_by_id('priceblock_ourprice')
                sentence += chalk.green("In Stock")
                sentence += " (" + price.text + ") ::: [LINK]: " + chalk.cyan(url)

        except NoSuchElementException:
            sentence += chalk.bold(chalk.red("Error finding item deatils"))

        except:
            sentence += chalk.bold(chalk.red("Unknown error occurred"))

        print(sentence)
        inc+=1 