import urllib.request
import json

URL_MOSTACTIVE = "https://api.iextrading.com/1.0/stock/market/list/mostactive"
URL_COMPANYNEWS = "https://api.iextrading.com/1.0/stock/{}/news/last/5"

def main():
    companies = getSymbolsMostActive()
    for company in companies:
        headlines = getCompanyNews(company[0])
        print("News Headlines for '{}'".format(company[1]))
        for headline in headlines:
            print("     * {}".format(headline))

def getCompanyNews(symbol):
    try:
        headlines = []
        news = json.loads(fetchData(URL_COMPANYNEWS.format(symbol)))
        for article in news:
            headlines.append(article['headline'])
        return headlines
    except Exception as e:
        print("Error fetching news!")
        return []

def getSymbolsMostActive():
    try:
        symbols = []
        data = json.loads(fetchData(URL_MOSTACTIVE))
        for company in data:
            symbols.append((company['symbol'], company['companyName']))
        return symbols
    except Exception as e:
        print("Error fetching symbols!")
        return []

def fetchData(url):
    response = urllib.request.urlopen(url)
    data = response.read()
    return data.decode('utf-8')

main()
