from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import chalk
from datetime import datetime
import json
import time

class Labels:
    def __init__(self, maxPrice, inStock, outOfStock):
        self.maxPrice = maxPrice
        self.inStock = inStock
        self.outOfStock = outOfStock

class Item:
    def __init__(self, brand, model, series, url):
        self.brand = brand
        self.model = model
        self.series = series
        self.url = url

class Shop:
    def __init__(self, currency, labels : Labels):
        self.name = ''
        self.currency = currency
        self.items = []
        self.labels = labels

    def loadData(self):
        with open('gpus.json') as file:
            products = json.load(file)[self.name]
        
        for product in products['items']:
            self.items.append(Item(product['company'], product['brand'], product['series'], product['url']))

class Currys(Shop):
    def __init__(self, currency, labels):
        super().__init__(currency, labels)
        self.name = 'Currys'

    def checkStock(self):
        driver = webdriver.Chrome(executable_path=CHROMEPATH)
        driver.minimize_window()
        inc = 0
        while(True):
            if inc >= len(self.items):
                inc = 0

            url = self.items[inc].url
            driver.get(url)

            sentence = ""
            sentence += "[" + chalk.yellow(datetime.now().strftime('%H:%M:%S')) + "] " + chalk.bold(chalk.magenta(self.name)) + " | "
            sentence += self.items[inc].brand + " " + self.items[inc].model + " " + self.items[inc].series + " || "

            try:
                findelem = driver.find_elements_by_id('delivery')
                if len(findelem) == 0:
                    sentence += chalk.red("Out of stock")
                else:
                    getPrice = driver.find_elements_by_class_name('amounts')[1].text
                    splitText = str.split(getPrice)

                    if len(splitText) == 1:
                        price = splitText[0]
                    else:
                        #Text is all thrown together when there is a sale on
                        #So this will be to extract the current price from the text
                        increment = 1
                        price = "£"
                        while(True):
                            try:
                                #Building price by going through each char in text after the '£' sign
                                #and checks if char is an integer - if is then will append to price string
                                #this way the program will stop before reaching the sale text
                                if isinstance(int(splitText[0][increment]), int):
                                    price += splitText[0][increment]
                                increment+=1
                            except:
                                #Adding the decimal and the 2 units following decimal (e.g. .99)
                                price+= splitText[0][increment] + splitText[0][increment+1] + splitText[0][increment+2]
                                break

                    sentence += chalk.green("In Stock")
                    sentence += " (" + price + ") ::: [LINK]: " + chalk.cyan(url)
            except NoSuchElementException:
                nostock = driver.find_elements_by_class_name('nostock')[2].text
                if nostock == self.labels.outOfStock[1]:
                    sentence += chalk.red("Out of stock")
            except:
                sentence += chalk.bold(chalk.red("Unknown error occurred"))

            print(sentence)
            inc+=1

class Amazon(Shop):
    def __init__(self, currency, labels):
        super().__init__(currency, labels)
        self.name = 'Amazon'
    
    def checkStock(self):
        driver = webdriver.Chrome(executable_path=CHROMEPATH)
        driver.minimize_window()
        inc = 0
        while(True):
            #Reset increment if gone over all items
            if inc >= len(self.items):
                inc = 0

            url = self.items[inc].url
            driver.get(url)

            time.sleep(0.30)

            sentence = ""
            sentence += "[" + chalk.yellow(datetime.now().strftime('%H:%M:%S')) + "] " + chalk.bold(chalk.magenta(self.name)) + " | "
            sentence += self.items[inc].brand + " " + self.items[inc].model + " " + self.items[inc].series + " || "

            try:
                availability = driver.find_element_by_id('availability')
                if availability.text != self.labels.inStock:
                    sentence += chalk.red("Out of Stock")
                else:
                    price = driver.find_element_by_id('corePrice_feature_div')
                    sentence += chalk.green("In Stock")
                    sentence += " (" + price.text.strip() + ") ::: [LINK]: " + chalk.cyan(url)

            except NoSuchElementException:
                sentence += chalk.bold(chalk.red("Error finding item deatils"))

            except:
                sentence += chalk.bold(chalk.red("Unknown error occurred"))

            print(sentence)
            inc+=1 

#EACH USER NEEDS TO REPLACE THIS WITH THEIR OWN DIRECTORY TO CHROMEDRIVER
# https://chromedriver.chromium.org/downloads
CHROMEPATH = ".\96\chromedriver"