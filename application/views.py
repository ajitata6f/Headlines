from application import app

@app.route("/")
def get_news():
    return "no news is good news"