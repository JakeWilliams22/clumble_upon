import pprint
import requests
from bs4 import BeautifulSoup
import flask as Flask
from flask_cors import CORS
import os
 
app = Flask.Flask(__name__, static_url_path='')
CORS(app)

cards = []
cardIterator = iter(cards);

''' Serves URL's read from mix sequentially '''

def setUp():
  req = requests.get('https://mix.com/')
  soup = BeautifulSoup(req.text, "html.parser") #Todo: make this request with a token for your account

  global cards
  global cardIterator
  cards = soup.findAll("a", {"class": "ArticleCard__title"})
  cardIterator = iter(cards);

@app.route('/next-site', methods=["GET"])
def getNextSite():
    if len(cards) == 0: 
        setUp()
    nextCard = next(cardIterator);
    while('href' not in nextCard.attrs and nextCard != None):
        nextCard = next(cardIterator)
    return nextCard['href'];
    
    
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    