# SpyneDrive

A car management web application built with Flask, SQLAlchemy, and Bootstrap, allowing users to manage and track their car fleet with features for car detail management, image uploads, and secure user authentication.

---

## Table of Contents
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Features](#features)
- [Usage](#usage)

- [Contributing](#contributing)
- [License](#license)

---

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/SpyneDrive.git
   cd SpyneDrive

2. **Create a Virtual Environment**
    ``` bash
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`

3. **Install Required Packages**
    ``` bash
    pip install -r requirements.txt

4. Set Up Database
    ``` bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade

## Project Structure

    SpyneDrive/
    ```bash
    ├── app/
    │   ├── __init__.py            # Initialize Flask app and database
    │   ├── models.py              # Define database models
    │   ├── routes.py              # Define app routes and logic
    │   ├── templates/             # HTML templates
    │   │   ├── base.html          # Base template with common structure
    │   │   ├── login.html         # Login page template
    │   │   ├── add_new_car.html   # Form for adding a new car
    │   │   └── detailed_car.html  # Page to view car details and manage images
    │   └── static/                # Static assets (CSS, JS, Images)
    ├── migrations/                # Database migrations
    ├── config.py                  # Configuration settings
    ├── README.md                  # Project documentation
    ├── requirements.txt           # Python package requirements
    └── run.py                     # Application entry point

## Features

- User Authentication: Secure login and logout functionality.
- Car Management: Add, update, and delete car details.
- Image Upload: Upload up to 10 images per car record.
- Search Functionality: Search cars by make, model, or license plate.
- Alerts: Visual alerts for successful and failed actions (e.g., login, car updates).

## Usage

1. **Run the Application**
    ``` bash
    flask run

2. **Access the App**
    Access the App

    Open your browser and go to http://127.0.0.1:5000.

3. **Login or Sign Up**

    - If running for the first time, register a new account.
    - After logging in, you can start managing car records.

## Contributing
1. **Fork the Repository**
    Create a New Branch for your feature or bugfix.
    ```bash
   
    git checkout -b feature-name

2. **Commit Your Changes**
    ```bash

    git commit -m "Add some feature"

3. **Push to Your Branch**
    ```bash

    git push origin feature-name

4. **Create a Pull Request**

## License
    This project is licensed under the MIT License.



    This format includes all instructions and information in a single, well-organized document. 



