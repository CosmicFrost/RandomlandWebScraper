from bs4 import BeautifulSoup
import requests
import time
import twitter
import schedule
from datetime import datetime
import sys
from past.builtins import execfile

#setup twitter authorization info

token = "1258495989402554371-hVzlRBAfHlzl0FZMSeDyYEdNJQXY57"
token_secret = "Psp6Gv4O1tUUwwSefzrpGY8RLCRGfXojuHBaqmBgEK4Xd"
consumer_key = "Jxa7ChzjyOjeSBs2PxHcJ92Pa"
consumer_secret = "HhakCITYO5ao2A54kVYm7sFowHqC6Pnrm5oQJ6hRXSLZ8B8i9f"
api = twitter.Api(consumer_key = consumer_key, consumer_secret = consumer_secret, access_token_key = token, access_token_secret = token_secret)
 
# set up an array to compare the results to before inserting tweet.

compareToPrevious = []
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
        product = product.strip()
    else:
        stockstatus = "Out of Stock"

    if ("In Stock" in stockstatus):
           print("The product " + product + " has stock status: " + stockstatus)
           prior_message = "The product " + product + " has stock status: " + stockstatus + " at " + str(datetime)


           #Build date string
           now = datetime.now()
           year = now.strftime("%Y")
           month = now.strftime("%m")
           day = now.strftime("%d")
           time = now.strftime("%H:%M:%S")
           date_time = now.strftime("%m/%d/%Y, %H:%M:%S")


           message = "The product " + product + " has stock status: " + stockstatus #+ " at " + str(datetime)
           if (message not in compareToPrevious):

               createTweet(message)
               compareToPrevious.append(message)

           #todo: fix the time stamp conversion to string. also, need to figure out a way to hold the status of a previous time...
           #maybe store the status in an array? or a database...check into this.
           #todo number 2: find a better way to hide the keys
           #todo number 3: figure out how to put this into a docker file / docker container

def createTweet(message):
    status = api.PostUpdate(message)
        

def job():
        for r in requestsArray:
            getStatus(getRequests(r))


def cleanup_job():
       
        MAX_TIMELINE_COUNT = 200
        max_tweet_id = None
        statuses = api.GetUserTimeline(count=MAX_TIMELINE_COUNT, max_id=max_tweet_id)
        for status in statuses:
               tweet_id = status.id
               api.DestroyStatus(tweet_id, trim_user=True)
    

    
def main():
    #schedule.every(25).minutes.do(job)
    #schedule.every(1)..do(cleanup_job)
   # schedule.every().day.at("00:00").do(cleanup_job)
   # while True:
        #delete -tweets --until 2020-05-11 tweet.js
   #  schedule.run_pending()
    # time.sleep(1)
     #cleanup_job()
     job()

try:
        main()
except:
        cleanup_job()
        main()


                 
