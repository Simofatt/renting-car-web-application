from flask import Flask ,Response,request,render_template,redirect, url_for,jsonify
import pymongo
import json
import os
from user import User
app = Flask(__name__)
app.static_folder = 'static'
from bson.objectid import ObjectId
from cars import Cars
from werkzeug.utils import secure_filename




## CONNECTION TO DB
try : 
    mongo = pymongo.MongoClient(host="localhost", port =27017,serverSelectionTimeoutMS =1000 )
    db = mongo.location_voitures #use the company db in mongo 
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







# Connect to MongoDB
try:
    mongo = pymongo.MongoClient(
        host='localhost', 
        port=27017,
        serverSelectionTimeoutMS = 1000     
    )

    db = mongo.location_voitures
    cars_collection = db['voiture']
    mongo.server_info() # trigger exception if cannot connect to db
    print("Connected to db")
except:
    print("ERROR - Cannot connect to db")

@app.route('/manage_cars')
def manage_cars():
    cars = cars_collection.find()
    return render_template('managecars.html', cars=cars)



UPLOAD_FOLDER = 'static/assets/images/cars/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/add_car', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        year = int(request.form['year'])
        price = int(request.form['price'])
        matricule = request.form['matricule']
        image = request.files['image']

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(filename)

            car_data = {
                'marque': make,
                'modele': model,
                'annee': year,
                'prix': price,
                'matricule': matricule,
                'image': filename
            }
            cars_collection.insert_one(car_data)

            return redirect('/manage_cars')

    return render_template('addcar.html')


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/update_car', methods=['POST'])
def update_car():
    car_id = request.form.get('carId')
    make = request.form['make']
    model = request.form['model']
    year = int(request.form['year'])
    price = int(request.form['price'])
    matricule = request.form['matricule']

    filter_criteria = {'_id': ObjectId(car_id)}
    update_data = {'$set': {'marque': make, 'modele': model, 'annee': year, 'prix': price, 'matricule': matricule}}

    try:
        cars_collection.update_one(filter_criteria, update_data)
        return redirect('/manage_cars')
    except Exception as e:
        print(f"Error updating document: {e}")


@app.route('/modify_car')
def modify_car():
    car_id = request.args.get('carId')
    car = cars_collection.find_one({'_id': ObjectId(car_id)})

    if car:
        return render_template('modifycar.html', car=car)
    else:
        return "Car not found"

@app.route('/delete_car', methods=['POST'])
def delete_car():
    car_id = request.form.get('carId')

    try:
        cars_collection.delete_one({'_id': ObjectId(car_id)})
        return redirect('/manage_cars')
    except Exception as e:
        print(f"Error deleting document: {e}")




















####################################
# if the script is the main programme, else if its imported from another module not __main__
if __name__ == "__main__"  :
    app.run(port =80, debug =True ) 





