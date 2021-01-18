from Shop import Labels, Item, Shop
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import chalk
from datetime import datetime
import re

#  #product-actions button
#will need to click button and see if it returns error or not

# also #product-acitons .unavailable
# check for 'not available for delivery'

#So probably check if product is available for delivery
#If is - then check add to basket button is present and say "in stock"
#else out of stock
#don't know if clicking add to basket will provide error in this case but will assume not

def Currys():
    labels = Labels(750, "FREE delivery available", ["Not available for delivery", "Sorry this item is out of stock"])

    items = []
    items.append(Item("asus", "Tuf", "3080", "https://www.currys.co.uk/gbuk/computing-accessories/components-upgrades/graphics-cards/asus-geforce-rtx-3080-10-gb-tuf-gaming-graphics-card-10214421-pdt.html"))
    items.append(Item("dell", "inspirion", "17", "https://www.currys.co.uk/gbuk/computing/laptops/laptops/dell-inspiron-17-3793-17-3-laptop-intel-core-i5-1-tb-hdd-128-gb-ssd-10202440-pdt.html"))
    items.append(Item("google", "Pixel", "4A 5G", "https://www.currys.co.uk/gbuk/phones-broadband-and-sat-nav/mobile-phones-and-accessories/mobile-phones/google-pixel-4a-5g-128-gb-just-black-10215418-pdt.html"))
    items.append(Item("asus", "Tuf oc", "3080", "https://www.currys.co.uk/gbuk/computing-accessories/components-upgrades/graphics-cards/asus-geforce-rtx-3080-10-gb-tuf-gaming-oc-graphics-card-10214446-pdt.html"))
    items.append(Item("msi", "gaming x trio", "3080", "https://www.currys.co.uk/gbuk/computing-accessories/components-upgrades/graphics-cards/asus-geforce-rtx-3080-10-gb-tuf-gaming-oc-graphics-card-10214446-pdt.html"))
    items.append(Item("gigabyte", "gaming oc", "3080", "https://www.currys.co.uk/gbuk/computing-accessories/components-upgrades/graphics-cards/gigabyte-geforce-rtx-3080-10-gb-gaming-oc-graphics-card-10214434-pdt.html"))
    items.append(Item("gigabyte", "eagle oc", "3080", "https://www.currys.co.uk/gbuk/computing-accessories/components-upgrades/graphics-cards/gigabyte-geforce-rtx-3080-10-gb-eagle-oc-graphics-card-10214430-pdt.html"))
    items.append(Item("gigabyte", "vision oc", "3080", "https://www.currys.co.uk/gbuk/computing-accessories/components-upgrades/graphics-cards/gigabyte-geforce-rtx-3080-10-gb-vision-oc-graphics-card-10216248-pdt.html"))
    items.append(Item("msi", "ventus 3x oc", "3080", "https://www.currys.co.uk/gbuk/computing-accessories/components-upgrades/graphics-cards/msi-geforce-rtx-3080-10-gb-ventus-3x-oc-graphics-card-10214426-pdt.html"))

    return Shop("Currys", '£', labels, items)

def checkCurrysStock():
    PATH = "G:\chromedriver\87\chromedriver" #WILL NEED TO CHANGE SO CAN WORK ON ALL SYSTEMS
    driver = webdriver.Chrome(executable_path=PATH)
    driver.minimize_window()
    shop = Currys()
    inc = 0
    while(True):
        if inc >= len(shop.items):
            inc = 0

        url = shop.items[inc].url
        driver.get(url)

        sentence = ""
        sentence += "[" + chalk.yellow(datetime.now().strftime('%H:%M:%S')) + "] " + chalk.bold(chalk.magenta(shop.name)) + " | "
        sentence += shop.items[inc].brand + " " + shop.items[inc].model + " " + shop.items[inc].series + " || "

        try:
            findelem = driver.find_elements_by_id('delivery')
            if len(findelem) == 0:
                #nostock = driver.find_elements_by_class_name('nostock').size == 0
                #nostock[2].text == shop.labels.outOfStock[1]
                #availability = driver.find_elements_by_class_name('unavailable')
                #available = availability[1].text
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
            if nostock == shop.labels.outOfStock[1]:
                sentence += chalk.red("Out of stock")
        except:
            sentence += chalk.bold(chalk.red("Unknown error occurred"))

        print(sentence)
        inc+=1

