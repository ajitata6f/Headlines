from application import app
import feedparser

RSS_FEEDS = {"bbc":"http://feeds.bbci.co.uk/news/rss.xml",
             "cnn":"http://rss.cnn.com/rss/edition.rss",
             "fox":"http://feeds.foxnews.com/foxnews/latest",
             "iol":"http://www.iol.co.za/cmlink/1.640"}

@app.route("/")
@app.route("/<application>")
def get_news(publication):
    feed = feedparser.parse(RSS_FEEDS[publication])
    first_article = feed['entries'][1]

    return """"<html>
            <body>
                <h1>BBC Headlines</h1>
                <b>{0}</b><br>
                <i>{1}</i><br>
                <p>{2}</p><br>
            </body>
        </html>
        """.format(first_article.get("title"), first_article.get("published"), first_article.get("summary"))




