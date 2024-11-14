from flask import Flask, render_template , request , redirect , url_for , flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Configure the SQLite database URI
app.config["SECRET_KEY"] = "your_car"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy extension
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    # Relationship with Car: A user can own many cars
    cars = db.relationship('Car', backref='owner', lazy=True)

# Define the Car model
class Car(db.Model):
    car_id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    license_plate = db.Column(db.String(20), unique=True, nullable=False)

    # Foreign key to User: This links each car to one user (one-to-many)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    # Relationship with Image: Each car can have up to 10 images
    images = db.relationship('Image', backref='car', lazy=True)

# Define the Image model for storing car images
class Image(db.Model):
    image_id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(255), nullable=False)  # URL or path to the image file
    car_id = db.Column(db.Integer, db.ForeignKey('car.car_id'), nullable=False)
    
    

    def __repr__(self):
        return f'<Image {self.image_url} for Car ID {self.car_id}>'

@app.route("/")
def homePage():
    return render_template("index.html")

@app.route("/signup" , methods=['GET' , 'POST'])
def SignUp():
    if(request.method == "POST"):
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        # Create a new user instance
        new_user = User(name=name, username=username, password=hashed_password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Account created successfully!", "success")
            return redirect(url_for("user_dashboard" , user_id=new_user.user_id , username=new_user.username))  # Redirect to homepage or login
        
        except Exception as e:
            db.session.rollback()
            flash("Username already exists or another error occurred.", "danger")
            
            return redirect(url_for("login"))  
             
    return render_template("SignUp.html")

@app.route("/login")
def logi():
    return render_template("login.html")

@app.route("/user_auth", methods=["GET" , "POST"])
def user_auth():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        # Query the database for the user
        user = User.query.filter_by(username=username).first()

        # Validate user exists and password matches
        if user and check_password_hash(user.password, password):
            print("Logged in successfully!", "success")
            
            # Store user ID in session
            session["user_id"] = user.user_id
            
            # Redirect to user's dashboard with dynamic URL
            return redirect(url_for("user_dashboard", user_id=user.user_id , username=user.username))
        else:
            message = "Invalid username or password. Please try again."
            # flash("Invalid username or password", "danger")
            # return redirect(url_for("user_auth" , message=message))
            return render_template("login.html" , message=message)

    

@app.route("/logout")
def logout():
    session.clear()  # Clears all session data to log the user out
    flash("You have been logged out successfully.", "success")
    return redirect(url_for("homePage"))

@app.route("/userdashboard/<int:user_id>")
def user_dashboard(user_id):
    user = User.query.get_or_404(user_id)
    print("inside dashboard",user_id)
    return render_template("user_dashboard.html" , username=user.username , add_new_car=add_new_car , user_id=user_id )


# @app.route("/create/<int:user_id>" , methods=["GET","POST"])
# def add_new_car(user_id):
#     if request.method == "POST":
#         make = request.form["make"]
#         model = request.form["model"]
#         year = request.form["year"]
#         license_plate = request.form["license_plate"]
        
#         # Optional: Assume a logged-in user with user_id=1 for testing
#         owner_id = user_id   # Replace with actual logged-in user ID in production
        
#         print("inside",user_id)

#         # Check if the car's license plate already exists to prevent duplicates
#         existing_car = Car.query.filter_by(license_plate=license_plate).first()
#         if existing_car:
#             # flash("A car with this license plate already exists.", "danger")
#             return redirect(url_for("add_new_car" , user_id=user_id))

#         # Create a new car record
#         new_car = Car(make=make, model=model, year=year, license_plate=license_plate, owner_id=owner_id)
        
#         try:
#             db.session.add(new_car)
#             db.session.commit()
#             flash("Car added successfully!", "success")
#             return redirect(url_for("user_dashboard", user_id=user_id))
        
#         except Exception as e:
#             db.session.rollback()
#             flash("An error occurred. Please try again.", "danger")
#             return redirect(url_for("add_new_car" , user_id=user_id) )
    
#     return render_template("add_new_car.html" , user_id=user_id)
#     # return render_template("add_new_car.html")


@app.route("/create/<int:user_id>", methods=["GET", "POST"])
def add_new_car(user_id):
    if request.method == "POST":
        make = request.form.get("make")
        model = request.form.get("model")
        year = request.form.get("year")
        license_plate = request.form.get("license_plate")

        # Check if the car's license plate already exists to prevent duplicates
        existing_car = Car.query.filter_by(license_plate=license_plate).first()
        if existing_car:
            return redirect(url_for("add_new_car", user_id=user_id))  # Redirect with user_id if car exists

        # Create a new car record with the provided data
        new_car = Car(make=make, model=model, year=year, license_plate=license_plate, owner_id=user_id)
        
        try:
            db.session.add(new_car)
            db.session.commit()
            return redirect(url_for("user_dashboard", user_id=user_id))  # Redirect to the user's dashboard
        
        except Exception as e:
            db.session.rollback()
            return redirect(url_for("add_new_car", user_id=user_id))  # Redirect back to the car form
    
    return render_template("add_new_car.html", user_id=user_id)  # Render form with user_id for GET request


@app.route("/view_cars/<int:user_id>")
def view_cars(user_id):
    
    search_term = request.args.get('search', '')  # Get the search term from query parameters
    if search_term:
        # Filter cars based on make, model, or license_plate that match the search term
        user_cars = Car.query.filter(
            Car.owner_id == user_id,
            (Car.make.ilike(f"%{search_term}%") |
             Car.model.ilike(f"%{search_term}%") |
             Car.license_plate.ilike(f"%{search_term}%"))
        ).all()
    # Query cars owned by the user with the given user_id (owner_id)
    else:
        user_cars = Car.query.filter_by(owner_id=user_id).all()

    # Check if the user has cars
    if user_cars:
        return render_template("view_car.html", user_id=user_id, cars=user_cars , detailed_car=detailed_car)
    else:
        # flash("You have no cars added yet.", "info")
        return render_template("view_car.html", user_id=user_id, cars=None , detailed_car=detailed_car)




@app.route("/detailed_car/<int:user_id>/<int:car_id>", methods=["GET", "POST"])
def detailed_car(user_id, car_id):
    car = Car.query.get(car_id)
    if not car or car.owner_id != user_id:
        return redirect(url_for("user_dashboard", user_id=user_id))

    can_upload_images = True
    if request.method == "POST":
        # Check how many images this car already has
        image_count = Image.query.filter_by(car_id=car_id).count()

        if image_count >= 10:
            # Set the flag to False, indicating that the user cannot upload more images
            can_upload_images = False
        else:
            image_url = request.form["image_url"]
            new_image = Image(image_url=image_url, car_id=car_id)
            try:
                db.session.add(new_image)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return render_template("detailed_car.html", car=car, user_id=user_id, images=Image.query.filter_by(car_id=car_id).all(), can_upload_images=can_upload_images, error_message="An error occurred. Please try again.")

        return redirect(url_for("detailed_car", user_id=user_id, car_id=car_id))

    images = Image.query.filter_by(car_id=car_id).all()
    return render_template("detailed_car.html", car=car, user_id=user_id, images=images, can_upload_images=can_upload_images , update_car=update_car)


# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route("/detailed_car/<int:user_id>/<int:car_id>", methods=["GET", "POST"])
# def detailed_car(user_id, car_id):
#     car = Car.query.filter_by(car_id=car_id, owner_id=user_id).first()
    
#     if not car:
#         flash("Car not found or you're not authorized to view this car.", "danger")
#         return redirect(url_for("view_cars", user_id=user_id))

#     if request.method == "POST":
#         # Handle image upload
#         if 'image' not in request.files:
#             flash("No file part", "danger")
#             return redirect(request.url)
        
#         image_file = request.files['image']
        
#         if image_file.filename == '':
#             flash("No selected file", "danger")
#             return redirect(request.url)

#         if image_file and allowed_file(image_file.filename):
#             filename = secure_filename(image_file.filename)
#             image_path = os.path.join('static', 'images', filename)
#             image_file.save(image_path)
            
#             # Save image URL in the database
#             new_image = Image(image_url=image_path, car_id=car_id)
#             db.session.add(new_image)
#             db.session.commit()
            
#             flash("Image uploaded successfully!", "success")
#             return redirect(url_for('detailed_car', user_id=user_id, car_id=car_id))

#     return render_template("detailed_car.html", user_id=user_id, car=car)




# @app.route("/detailed_car/<int:user_id>/<int:car_id>", methods=["GET", "POST"])
# def detailed_car(user_id, car_id):
#     car = Car.query.filter_by(car_id=car_id, owner_id=user_id).first()
#     if car is None:
#         flash("Car not found or you're not authorized to view this car.", "danger")
#         return redirect(url_for("view_cars", user_id=user_id))

#     # Handle image uploads or other logic as needed here

#     return render_template("detailed_car.html", user_id=user_id, car=car)


@app.route("/update_car/<int:user_id>/<int:car_id>", methods=["GET", "POST"])
def update_car(user_id, car_id):
    # Fetch the car record
    car = Car.query.get(car_id)
    if not car or car.owner_id != user_id:
        return redirect(url_for("user_dashboard", user_id=user_id))

    # Fetch the existing images associated with the car
    images = Image.query.filter_by(car_id=car_id).all()

    if request.method == "POST":
        # Update the car details (make, model, year, license plate)
        make = request.form["make"]
        model = request.form["model"]
        year = request.form["year"]
        license_plate = request.form["license_plate"]

        # Update the car record
        car.make = make
        car.model = model
        car.year = year
        car.license_plate = license_plate

        # Handle image uploads
        if "image_urls" in request.form:
            new_image_urls = request.form.getlist("image_urls")  # List of new image URLs

            # Remove existing images and add new ones
            Image.query.filter_by(car_id=car_id).delete()
            for url in new_image_urls:
                if url:  # Ensure URL is not empty
                    new_image = Image(image_url=url, car_id=car_id)
                    db.session.add(new_image)

        try:
            db.session.commit()
            flash("Car details and images updated successfully!", "success")
            return redirect(url_for("view_car", user_id=user_id))  # Redirect to the car view page
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while updating the car details.", "danger")
            return redirect(url_for("detailed_car", user_id=user_id, car_id=car_id))

    return render_template("update_car.html", car=car, user_id=user_id, images=images)

   
@app.route("/delete_car/<int:user_id>/<int:car_id>", methods=["GET","POST"])
def delete_car(user_id, car_id):
    # Fetch the car object based on car_id
    car = Car.query.get(car_id)

    # Check if the car exists and the user is the owner
    if not car or car.owner_id != user_id:
        flash("Car not found or you're not the owner!", "danger")
        return redirect(url_for("view_cars", user_id=user_id))

    # Delete associated images
    images = Image.query.filter_by(car_id=car_id).all()
    for image in images:
        db.session.delete(image)

    # Delete the car record
    db.session.delete(car)

    # Commit the changes
    try:
        db.session.commit()
        flash("Car deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while deleting the car.", "danger")

    # Redirect to the user's car list
    return redirect(url_for("view_cars", user_id=user_id))

# @app.route("/detail_car")
# def detailed_car():
#     return render_template("detailed_car")


# @app.route('/view/<int:user_id>')
# def view_car(user_id):
#     print("inside view fn" , user_id)
#     return "car is mine"


if __name__ == "__main__":
    # Create the tables (User, Car, Image)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
