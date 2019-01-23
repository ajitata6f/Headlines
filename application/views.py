from application import app
from flask import render_template, request
import feedparser
import json
import urllib
import urllib3

WEATHER_API_KEY = "6d3623fe0f1dcf8ceb28aa78b0e2b071"
CURRENCY_APP_ID = "ddcbfb2d68e143288cd728fa089b4784"

DEFAULTS = {"publication": "bbc",
            "city": "London, UK"}

RSS_FEEDS = {"bbc": "http://feeds.bbci.co.uk/news/rss.xml",
             "cnn": "http://rss.cnn.com/rss/edition.rss",
             "fox": "http://feeds.foxnews.com/foxnews/latest",
             "iol": "http://www.iol.co.za/cmlink/1.640"}

WEATHER_URL = "api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}"
CURRENCY_URL = "https://openexchangerates.org/api/latest.json?appid={}".format(CURRENCY_APP_ID)


@app.route("/")
def home():
    # get publication from user input
    publication = request.args.get("publication")
    if publication is None:
        publication = DEFAULTS["publication"]

    articles = get_news(publication)

    # get city from user input
    city = request.args.get("city")
    if city is None:
        city = DEFAULTS["city"]

    weather = get_weather(city)

    return render_template("index.html", articles=articles, feed_source=publication, weather=weather)


def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS["publication"]
    else:
        publication = query.lower()

    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']


def get_weather(query):
    query = urllib.parse.quote(query)
    url = WEATHER_URL.format(query, WEATHER_API_KEY)
    http = urllib3.PoolManager()
    res = http.request('GET', url)
    parsed = json.loads(res.data)
    weather = None
    if parsed.get("weather"):
        weather = {"description": parsed["weather"][0]["description"],
                   "temperature": parsed["main"]["temp"],
                   "city": parsed["name"],
                   "country": parsed["sys"]["country"]}

    return weather


def get_rate(frm, to):
    http = urllib3.PoolManager()
    all_currency = http.request("GET", CURRENCY_URL)
    parsed = json.loads(all_currency).get("rates")
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())

    return to_rate/frm_rate
