__author__ = 'Sarge'

from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from databaseconnection import DatabaseConnection
import json

DATABASE = 'photoorderdbname'
HOST = 'localhost'
USERNAME = 'photoorderdbuser'
PASSWORD = 'somesecurepass'

app = Flask(__name__)
db = DatabaseConnection(HOST, DATABASE, USERNAME, PASSWORD)

#@app.route("/")
#def hello():
#    return render_template('404.html')


@app.route("/<siteurl>")
def photossite(siteurl = None):
    #photos = siteurl
    photos = db.getPhotosFromDB(siteurl)
    if photos == -1:
        return render_template('404.html')
    else:
        jquery = url_for('static', filename='jquery-2.1.3.min.js')
        script = url_for('static', filename='save.js')
        return render_template('template.html', photos=photos, jquery=jquery, script=script)


@app.route("/order", methods=['POST'])
def orderphoto():
    idphoto = request.form['idphoto']
    ordered = request.form['ordered']
    result = db.setPhotoOrderStatus(idphoto, ordered)
    if result == 0:
        return json.dumps({'status': 'OK'})
    else:
        return json.dumps({'status': 'Error'})

if __name__ == "__main__":
    app.run(debug=True)
