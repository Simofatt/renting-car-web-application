from flask import Flask ,Response,request,render_template,redirect, url_for
import pymongo
import json
from user import User
app = Flask(__name__)
from bson.objectid import ObjectId
from cars import Cars



## CONNECTION TO DB
try : 
    mongo = pymongo.MongoClient(host="localhost", port =27017,serverSelectionTimeoutMS =1000 )
    db = mongo.carsRent #use the company db in mongo 
    mongo.server_info() 
    print("connect to db")

except : 
    print("ERROR - Cannot connect to db")


#ROOT TO LOGIN
@app.route("/login")
def blade() : 
    return render_template("login.html")

#AUTHENTIFICATION 

@app.route("/auth", methods=["POST"])
def auth():
    email = request.form["email"]
    password = request.form["password"]

    user = User.authenticate(email, password)

    if user is not None:
        # Authentication successful, redirect to get_cars route
        return redirect(url_for('get_cars'))

    return render_template("login.html", error_message="Invalid credentials")




#GET ALL THE CARS BASED ON THE ETAT 
@app.route('/cars', methods=['GET'])
def get_cars():
  
 car_list = Cars.get()
 return render_template('category.html', cars=car_list)




























####################################
# if the script is the main programme, else if its imported from another module not __main__
if __name__ == "__main__"  :
    app.run(port =80, debug =True ) 





