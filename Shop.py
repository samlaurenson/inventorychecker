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
    def __init__(self, name, currency, labels : Labels, items):
        self.name = name
        self.currency = currency
        self.labels = labels
        self.items = items

