from flask import Blueprint, render_template, request, send_from_directory, current_app
import json
#from . import db
import os

server = Blueprint('server', __name__,static_folder="static")


# stock_name="TSLA"
# stock_date="2021-01-21"
# plotname=driver(stock_name,stock_date)

# landing page, assumed
# app.config['stock_date']=stock_date
# app.config['plotname']=plotname
@server.route('/')
def index():
    return render_template('index.html')#,stock_name=stock_name,stock_date=stock_date,plotname=plotname)

@server.route('/profile')
def profile():
    return render_template('profile.html')

# routes defined by steven either as demonstrations or actual needed routes

# Purpose: Unlike the Signup or Login route, this will simply regard the return or alteration of user data on the user's behest
# expected parameters
# userid: a string or integer corresponding to the user in the database. Should probably obfuscate or hash to prevent fuckery.
@server.route('/users/<userid>', methods=['GET']) # the first element is a string denoting the name of the route, the second is a list with the corresponding methods that this route takes
def users(data):
    # request object is what you get from an http request
    if request.method == 'GET': # the method used to arrive at this route is available for reading
        try:
            req_data = request.get_json() # jsonifying the request makes it easier to parse
            print(req_data)
            # find the user
            #result = getUser(req_data.userid) # undefined function, probably make it in another file and import it. Should get user data.

            # lets assume since we are still setting up that our function is a success and this is the result
            result = {userid: 0, username: "MaxTrader"}






            #if fail
            if(result == "some error we will probably define by name"): # the actual error name should probably be defined asap and this changed with it
                raise Exception("User data not found.")
            # call a function or do the ops required to return relevant user information to the front end
            return json.dumps({"userdata": result})
        except Exception as e:
            print(e) # print the error so backend folk know exactly whats going on. May be bad practice, esp printing backend errors in the front end
            # i.e.: dont send the actual backend errors to the front end, translate them into something simple as to not expose our stack
            return json.dumps({"error_message": e})
            pass
        return

# Expected Parameters
# email: str
# email2: str - for validation of hte first email
# password: str
# password2: str - For validation of the first password
# username: str 
@server.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        req_data = request.get_json()
        print(req_data)
        # Do stuff with that info, like do the input validation and then add the user to the DB
        try:
            # attempt to register user

            #auth_data = sign_up(req_data["password"], req_data["password2"])
            #result = makeUser(req_data["email"], req_data["first_name"], req_data["last_name"], auth_data[0], auth_data[1][0], auth_data[1][1])
            
            # The above two functions were custom made. The first to make sure the two passwords are the same than return a hash, private key, and public key
            # it would raise an exception in the function which wouldve been caught by the try catch statement surrounding all this.
            # the second was a database function to actually make the user in the db through the pymongo stuff


            # lets assume since we are still setting up that our function is a success and this is the result
            result = {userid: 0, username: "MaxTrader"}

            # if registration fails
            if result == "Insertion Error":
                raise Exception(result)  

        except Exception as e:
            print(e)
            return json.dumps({"error_message": e})
            pass
        return json.dumps({"message": "Signup Complete"})
    if request.method == 'GET':
        # prolly just display the page?
        bottom_text = "bottomtext"
    return bottom_text

# email: str - user's email
# password: str - hopefully the user's password
@server.route('/login', methods=['POST', 'GET']) 
def login():
    if request.method == 'POST':
        req_data = request.get_json()
        # Again do stuff with the info passed in
        try:
            #result = log_in(req_data["email"], req_data["password"]) # log_in was a function I made to handle logging in, make your own!
            result = "good"

            if result == 'some error': # please define the error and make the necessary changes
                raise Exception(result)
  
        except Exception as e:
            print(e)
            return json.dumps({"error_message": e})
        return json.dumps({"message": "Loggin in!"}) # This may not even be the way to do it but we will figure it out
    if request.method == 'GET':
        return """<h1> Fields are email and password </h1>"""


"""File download stuff"""
@server.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    try:
        uploads = os.path.join(current_app.root_path, current_app.config['DOWNLOADS'])
        return send_from_directory(directory=uploads, filename=filename)
    except Exception as e:
        print(e)