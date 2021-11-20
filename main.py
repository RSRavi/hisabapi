from flask import Flask, render_template, request, make_response, url_for, send_file, session, redirect
import pymongo
import ssl

myclient = pymongo.MongoClient("mongodb+srv://root:root@cluster0.6yvdo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
mydb = myclient["hisab"]

user = mydb['users']
provider = mydb['provider']
transaction = mydb['transaction']

app = Flask(__name__)

@app.route("/")
def index():
    result = user.find()
    for x in result:
        print(x)
    return "Welcome to Hisab"

@app.route('/create', methods=['POST', 'GET'])
def create():
    if (request.method == 'POST'):
        data = {}
        """data['_id']= "1234567890"
        data['name']= "ABCD"
        data['username'] = "1234567890"
        data['password'] = "abc123"
        data['address'] = "VNS"
        """
        type = request.form.get('type')
        data['_id']= request.form.get('username')
        data['name']= request.form.get('name')
        data['username'] = request.form.get('username')
        data['password'] = request.form.get('password')
        data['address'] = request.form.get('address')
        if type == 'users':
            user.insert_one(data)
        elif type == 'provider':
            provider.insert_one(data)
    return "OK"

@app.route('/login', methods=['POST', 'GET'])
def login():
    global result
    session.permanent = True
    if (request.method == 'POST'):
        type = request.form.get('type')
        if type == 'users':
            result = user.find_one({"_id": request.form.get('username')})
        elif type == 'provider':
            result = provider.find_one({"_id": request.form.get('username')})
        username = request.form.get('username')
        password = request.form.get('password')
        if username == result['username'] and password == result['password']:
            session['user'] = username
            session['logged_in'] = True
            return result
        return "<h1>Wrong username or password</h1>"

@app.route('/transactionAdd', methods=['POST', 'GET'])
def transaction():
    #session.permanent = True
    if (request.method == 'POST'):
        """id = request.form.get('username')
        month = request.form.get('month')
        data = request.form.get('data')
        pending = request.form.get('pending')
        paid = request.form.get('paid')"""

        id = "1234567890"
        month = "August 2021"
        data = {}
        pending = '700'
        paid = '0'
        fl = {'_id': id, 'month': month, 'data': data, 'pending': pending, 'paid': paid}
        print(fl)
        transaction.insert_one(fl)
    return "Success"

if __name__ == "__main__":
    app.debug = True
    app.run()
