from flask import Flask ,Response,request,render_template,session,redirect, url_for,jsonify
import pymongo
import json
import os
from user import User
app = Flask(__name__)
app.static_folder = 'static'
from bson.objectid import ObjectId
from cars import Cars
from werkzeug.utils import secure_filename
from pymongo import MongoClient





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














############################ AHMED ##################################

app.secret_key = 'HereWegoAgain'


client = MongoClient('mongodb://localhost:27017')
db = client['location_voitures']
collection = db['client']


@app.route('/AddNewClient')
def hello():
    return render_template('AddNewClient.html')

@app.route('/add_client', methods=['POST'])
def add_client():
    client_data = {
        'cin': request.form['CIN'],
        'nom': request.form['nom'],
        'prenom': request.form['prenom'],
        'email': request.form['email'],
        'tel': request.form['telephone'],
        'adresse': request.form['adresse']
    }
    collection.insert_one(client_data)

    session['success'] = True

    return redirect(url_for('list_clients'))


@app.route('/clients')
def list_clients():
    clients = collection.find()
    return render_template('ClientList.html', clients=clients, client=None)





@app.route('/deleteClient', methods=['POST'])
def delete_client():

    client_id = request.form.get('idClient')

    print(f"Deleting client with ID: {client_id}")


    result = collection.delete_one({'cin': client_id})

    if result.deleted_count > 0:
        return redirect(url_for('list_clients'))
    else:
        return 'Failed to delete the client or client not found.'




@app.route('/add_new_client.html')
def add_new_client():
    success = session.pop('success', False)
    if success:
        return """
        <script>
            Swal.fire({
                title: 'Success!',
                text: 'Client data inserted successfully.',
                icon: 'success',
                confirmButtonText: 'OK'
            });
        </script>
        """

    return render_template('AddNewClient.html')
@app.route('/modify_client', methods=['POST'])
def modify_client():

    print(request.form)  # Debugging line
    cin = request.form['CIN']
    nom = request.form['nom']
    prenom = request.form['prenom']
    email = request.form['email']
    telephone = request.form['telephone']
    adresse = request.form['adresse']

    # Find the client with the matching CIN
    query = {'cin': cin}
    client = collection.find_one(query)

    if client:
        # Update the client data
        update = {
            '$set': {
                'nom': nom,
                'prenom': prenom,
                'email': email,
                'tel': telephone,
                'adresse': adresse
            }
        }
        collection.update_one(query, update)

        return redirect(url_for('list_clients'))
    else:
        return 'Client not found'
if __name__ == '__main__':
    app.run(debug=True)






####################################
# if the script is the main programme, else if its imported from another module not __main__
if __name__ == "__main__"  :
    app.run(port =80, debug =True ) 





