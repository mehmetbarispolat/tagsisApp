from flask import Flask,render_template,redirect,request,url_for, jsonify
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

""" GLOBAL VARIABLE """
#------------------------------------------------------------
SERVICE_KEY_PATH = './serviceAccountKey.json'
#------------------------------------------------------------

""" FIREBASE CONNECT"""
#------------------------------------------------------------
cred = credentials.Certificate(SERVICE_KEY_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()
#------------------------------------------------------------
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/map')
def map():
    return render_template("jquerymap.html")

@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        searchInput = request.form['searchInput']
        return redirect(url_for("getResult",searchInput = searchInput))

@app.route('/getResult/<searchInput>')
def getResult(searchInput):
    list_of_tagsis = searchTagsis(searchInput)
    return render_template("home.html",list_of_tagsis = list_of_tagsis)

@app.route('/getMap/<searchInput>',methods=[ 'POST'])
def getMap(searchInput):
    if request.method == 'POST':
        list_of_region = searchRegion(searchInput)
        return jsonify({'data': render_template('response.html', list_of_tagsis=list_of_region)})

def searchTagsis(searchInput):
    list_of_tagsis = []
    tagsis_ref = db.collection(u'tagsis')
    docs = tagsis_ref.stream()
    searchInput = searchInput.replace('I','ı').lower()
    for doc in docs:
        if searchInput in doc.to_dict()["productName"].lower() or searchInput in doc.to_dict()["brand"].lower() or searchInput in doc.to_dict()["companyName"].replace('İ','i').replace('I','ı').lower():
            list_of_tagsis.append(doc.to_dict())
    return list_of_tagsis

def searchRegion(searchInput):
    list_of_region = []
    region_ref = db.collection(u'tagsis')
    docs = region_ref.stream()
    searchInput = searchInput.replace('ı','I')
    for doc in docs:
        if searchInput.replace('i','İ').upper() in doc.to_dict()["companyName"]:
            list_of_region.append(doc.to_dict())
    return list_of_region


"""
tagsis_ref = db.collection(u'tagsis')
docs = tagsis_ref.stream() ## Tüm verileri alır. --> .stream()

for doc in docs:
    print(f'{doc.id} => {doc.to_dict()}')
"""
 #return render_template('index.html', productName = doc.to_dict()["productName"], brand = doc.to_dict()["brand"], companyName = doc.to_dict()["companyName"])#setdefault dict.