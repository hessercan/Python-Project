import xml.etree.ElementTree as ET
import urllib.request
import datetime

FEED_URL="https://www.npr.org/rss/podcast.php?id=510306"

def main():
    # fetch the feed and parse it
    try:
      data = fetchData(FEED_URL)
    except Exception as e:
      print("Error fetching data:  {}".format(e))
      return -1
    parseFeed(data)

def parseFeed(feed):
    # parse the feed, look for title of the feed
    root = ET.fromstring(feed)
    title = root.findtext('channel/title')
    items = root.findall('channel/item')
    print("Podcast:  {}".format(title))
    for item in items:
          item_title = item.findtext('title')
          item_pubdate = item.findtext('pubDate')
          td = datetime.datetime.strptime(item_pubdate, "%a, %d %b %Y %X %z")
          pub = datetime.datetime.strftime(td, "%B %d, %Y")
          if td.year == 2019:
            print("    {} | {}".format(item_title, pub))

def fetchData(url):
    # download text data, decode it
    response = urllib.request.urlopen(url)
    data = response.read()
    return data.decode('utf-8')

if __name__ == '__main__':
    quit(main())
