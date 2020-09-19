import os
#import pymongo
from flask import Flask ,request,jsonify,render_template,url_for
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

# Database conection
#dbconn = pymongo.MongoClient("mongodb://localhost:27017/")
#dbname = "contactdb"
#db = dbconn[dbname]
#collection_name = "contactlist"
#collection = db[collection_name]

app = Flask(__name__)
@app.route("/")
@cross_origin()
def index():
    return render_template("home.html")

@app.route("/about")
@cross_origin()
def aboutus():
    return render_template("about.html")


@app.route("/contact",methods=['POST','GET'])
@cross_origin()
def contactus():
    if request.method=='POST':
        #name = request.form["name"]
        #email = request.form["email"]
        #phone = request.form["phone"]
        #desc = request.form["desc"]
        #contact = {
         #   "name":name,
         #   "email":email,
         #   "phone":phone,
         #   "desc":desc
        #}
        #x = collection.insert_one(contact)
        #print(x.inserted_id)
        error = "Contact Form Submit successfully"
        return render_template("contact.html",error=error)
    else:
        return render_template("contact.html")


@app.route("/image")
@cross_origin()
def imagescraper():
    return render_template("image.html")

@app.route("/review",methods=['POST','GET'])
@cross_origin()
def reviewscraper():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ", "")
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString
            uClient = uReq(flipkart_url) #uReq give the httpResponse object
            flipkartPage = uClient.read()
            uClient.close()
            flipkart_html = bs(flipkartPage, "html.parser")
            bigboxes = flipkart_html.findAll("div", {"class": "bhgxx2 col-12-12"})
            del bigboxes[0:3]
            box = bigboxes[0]
            productLink = "https://www.flipkart.com" + box.div.div.div.a['href']
            prodRes = requests.get(productLink)
            prodRes.encoding = 'utf-8'
            prod_html = bs(prodRes.text, "html.parser")
            commentboxes = prod_html.find_all('div', {'class': "_3nrCtb"})
            reviews = []
            for commentbox in commentboxes:
                try:
                    name = commentbox.div.div.find_all('p', {'class': '_3LYOAd _3sxSiS'})[0].text
                except:
                    name = 'No Name'

                try:
                    rating = commentbox.div.div.div.div.text

                except:
                    rating = 'No Rating'

                try:
                    commentHead = commentbox.div.div.div.p.text

                except:
                    commentHead = 'No Comment Heading'
                try:
                    comtag = commentbox.div.div.find_all('div', {'class': ''})
                    custComment = comtag[0].div.text
                except Exception as e:
                    print("Exception while creating dictionary: ", e)

                mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
                          "Comment": custComment}
                reviews.append(mydict)
                print(mydict)
            return render_template('review.html', reviews=reviews[0:(len(reviews) - 1)])
        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong'

    else:
        return render_template('review.html')





port = int(os.getenv("PORT"))
if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=5000)
    app.run(host='0.0.0.0', port=port)
    #app.run(host='127.0.0.1', port=5000, debug=True)

