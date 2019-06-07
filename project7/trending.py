'''
Mark Hesser
www.hessercan.com
mark@hessercan.com
Python Project 7: Stack Overflow & Indeed API
'''

import sys
import os
import json
import math
import operator
import gzip
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

STACKOVERFLOW_API_URL = "https://api.stackexchange.com/2.2/questions?page={}&pagesize={}&order=desc&sort=creation&site=stackoverflow"
STACKOVERFLOW_MAX_PAGE_SIZE = 100
INDEED_FEED_URL = "https://rss.indeed.com/rss?q{}&l={}"

def main():
    config = loadConfig()
    # Gets a Dictionary of Most recent Topics from Stack Overflow, then sorts that data into a list of trending topics based on limit set
    trendingTopics = sortTopics(getTrending(config['sample_size'], STACKOVERFLOW_MAX_PAGE_SIZE), config['topic_limit'])
    # print("DEBUG: Trending Topics: {}".format(trendingTopics))

    # Checks to see if anything was returned to trendingTopics
    # Generates a String with commas and Prints to the Console
    if len(trendingTopics) > 0:
        topicsStr = ", ".join(trendingTopics)
        print("Current Trending Topics: {}\n".format(topicsStr))
        # listJobs("best buy", config['location'])

        # Lists jobs for each topic
        for topic in trendingTopics:
            listJobs(topic, config['location'], config['job_limit'])
    else:
        print("Can't Display Trending Topics, Something went wrong. Please Try Again.")

# Loads the config.json file
# Config Dictionary Format:
# - location: string (City, State)
# - job_limit: int (number of jobs that will be displayed)
# - sample_size: int (number of questions to collect tags from)
# - topic_limit: int (number of topics to display jobs for)
def loadConfig():
    file = 'config.json'
    path = os.path.dirname(os.path.realpath(__file__))
    cfile = os.path.join(path,file)
    if os.path.exists(cfile):
        try:
            with open(cfile, 'r') as c:
                config = json.load(c)
        except Exception as e:
            print("Error: {}".format(e))
            writeDefaultConfig(cfile, 2)
    else:
        writeDefaultConfig(cfile, 1)

    if all (k in config for k in ("location", "job_limit", "sample_size", "topic_limit")):
        return config
    else:
        writeDefaultConfig(cfile, 2)

# Deletes Config File and Writes the Default Config
# Parameters:
# - cfile: string (abspath to Config File)
# - code: int (1: File not Found, 2: File Corrupt)
def writeDefaultConfig(cfile, code):
    DEFAULT_CONFIG = [
        "{",
        "\t\"location\" : \"State College, PA\",",
        "\t\"job_limit\" : 10,",
        "\t\"sample_size\" : 100,",
        "\t\"topic_limit\" : 5",
        "}"
    ]

    if code == 1:
        alert = "File Not Found"
    elif code == 2:
        os.remove(cfile)
        alert = "File is Corrupt"
    else:
        alert = "Unknown Error"

    with open(cfile, 'w') as o:
        for item in DEFAULT_CONFIG:
            o.write("%s\n" % item)
        print("ALERT: 'config.json' {}, Default Settings have been applied.".format(alert))
        print("Please edit the config file found at: \n{}".format(cfile))
        exit()


# Stack Overflow
# Determines from sample_size how many pages
# Parameters:
# - sample_size: int (number of questions to collect)
# - mps: int (Max Page Size per request, used to calculate number of pages)
def getTrending(sample_size, mps):
    print("Getting Trending Topics...")

    # Algorithm that calculates the number of pages and the pagesize of the last page
    numPages = math.ceil(sample_size / mps)
    lastPage = sample_size % mps
    if lastPage == 0:
        lastPage = mps
    # print("DEBUG: numPages: {}.format(numPages))
    # print("DEBUG: lastPage: {}.format(lastPage))

    topics = {}

    # Collecting the Data from each page
    for page in range(1, numPages + 1):
        if page < numPages:
            getTrendingRun(page, mps, topics)
        elif page == numPages:
            getTrendingRun(page, lastPage, topics)

    print()

    # print("DEBUG: TOPICS: {}".format(topics))
    return topics

# Uses the STACKOVERFLOW_API_URL to get a dictionary of recent questions from the page  provided
# Takes that data and collects the tags from each question and tallies up the results
# Appends the topic to the dictionary and Increments by 1 each time found
# Parameters:
# - page: int (page to get data from)
# - pagesize: int (number of questions to collect from each page)
# - topics: dictionary {
#    key: tag
#    value: int (number of times found)
# }
def getTrendingRun(page, pagesize, topics):
    url = STACKOVERFLOW_API_URL.format(encodeURL(page), encodeURL(pagesize))
    # print("DEBUG: STACK_URL: {}".format(url))
    # print("DEBUG: Page: {}, PageSize: {}".format(page,pagesize))

    try:
        data = jsonify(url)
    except urllib.request.HTTPError as err:
        if err.code == 400:
            print("STACK_URL: {}".format(url))
            print('Error 400: Bad Request')
            return -1
        elif err.code == 404:
            print("STACK_URL: {}".format(url))
            print('Bad URL, Error 404: Page not Found')
            return -2

    for item in data['items']:
        for tag in item['tags']:
            if topics.get(tag):
                topics[tag] += 1
            else:
                topics[tag] = 1

# Takes the Trending Dictionary and Sorts it by most popular
# Uses the limit to create a new list of trending topics
# Returns New List topTrending
def sortTopics(trending, limit):
    s_trending = (sorted(trending.items(), key=operator.itemgetter(1), reverse=True))

    topTrending = []
    for topic in list(s_trending)[0:limit]:
        # Topic Index 0: Name of Topic, Index 1: Number of Hits
        topTrending.append(topic[0])

    return topTrending

# Displays a List of Jobs available from the provided location and topic
# Limit the amount of jobs displayed
def listJobs(topic, location, limit):
    url = INDEED_FEED_URL.format(encodeURL(topic),encodeURL(location))
    try:
        data = fetchData(url)
    except urllib.request.HTTPError as err:
        if err.code == 400:
            print('URL not Encoded, Bad Request')
            return -1
        elif err.code == 404:
            print('Bad URL, Page not Found')
            return -2

    jobs = parseFeed(data)
    if len(jobs) > limit:
        numJobs = limit
    else:
        numJobs = len(jobs)

    print("{} most recent '{}' jobs near {}".format(numJobs, topic, location))

    counter = 1
    for job in jobs:
        if counter <= limit:
            print("    * {}".format(job['title']))
            print("        - {}".format(job['link']))
        counter += 1
    print()

# Parses Indeed XML from RSS Feed and returns a list of Jobs
# Index 0 is the Title, and Index 1 is the link to the job
def parseFeed(data):
    jobs = []
    root = ET.fromstring(data)
    items = root.findall('channel/item')
    for item in items:
        job = {}
        # print("DEBUG: {}".format(item.findtext('link')))
        job['title'] = item.findtext('title')
        job['link'] = item.findtext('link')
        jobs.append(job)
    return jobs

# Downloads data from URL and decodes it to UTF-8
# Returns downloaded data
def fetchData(url):
    response = urllib.request.urlopen(url)
    data = response.read()
    return data.decode('utf-8')

# Downloads Compressed JSON data from URL and Decompresses it
# Returns Decompresses JSON Data as a dictionary
def jsonify(url):
    response = urllib.request.urlopen(url).read()
    tmp = gzip.decompress(response).decode('utf-8')
    repo = json.loads(tmp)
    return repo

# Encodes strings to URL friendly formats (ex. spaces => %20)
def encodeURL(string):
    return urllib.parse.quote(str(string))

# Only runs main() if run script from command line
if __name__ == '__main__':
    sys.exit(main())
