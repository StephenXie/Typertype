import requests
from random import randint


quotes = requests.get('https://type.fit/api/quotes').json()


def get_quote():
    return quotes[randint(0, 1600)]['text']

print(get_quote())