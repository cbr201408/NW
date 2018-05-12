from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app)


@app.route("/")
def index():
    listings = mongo.db.listings.find_one()
    return render_template("index.html", dict=listings)

# @app.route("/clear")
# def clear():
#     result = mongo.db.listings.delete_many({})
#     return redirect("http://127.0.0.1:5000/", code=302)

@app.route("/scrape")
def scrape():
    listings = mongo.db.listings
    listings_data = scrape_mars.scrape()
    listings.delete_many({})
    listings.insert_one(listings_data)
    return redirect("http://127.0.0.1:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
