from bs4 import BeautifulSoup
import requests
import time

#make requests for items you want to see if in stock

MainPage = requests.get("https://store.randomland.com/collections/frontpage")
initialSoup = BeautifulSoup(MainPage.text, 'html.parser')
requestsArray = []
for a in initialSoup.find_all('a', {'class': 'grid-view-item__link grid-view-item__image-container full-width-link'}):
	requestsArray.append("https://store.randomland.com"+a['href'])

def getRequests(request):
    r = requests.get(request)
    return r

def getStatus(r):
    soup = BeautifulSoup(r.text, 'html.parser')
    div = soup.find('div', {'class': 'product-form__item product-form__item--submit product-form__item--payment-button product-form__item--no-variants'})
    span = div.find('span')
    product = soup.title.string
    stockstatus = span.string
    if ("Add to cart" in stockstatus):
        stockstatus = "In Stock"
    else:
        stockstatus = "Out of Stock"
    print("The product " + product + " has stock status: " + stockstatus)


for r in requestsArray:
    getStatus(getRequests(r))
    

                 
