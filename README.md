# Fit-fuel
A fitness university project for IT7405 which allows for simple workout and meal logging with some automated functionalities.
Prerequisites
•	Python installed on your system Python 3.9.13
•	Django installed (will be set up in the virtual environment).
•	A database configured (Djongo)
________________________________________
Steps
1. Create a Python Virtual Environment
1.	Open your terminal or command prompt.
2.	Navigate to your project directory.
3.	Create a virtual environment:
python -m venv venv
4.	Activate the virtual environment:
venv\Scripts\activate
5.	Install the required dependencies:
pip install -r requirements.txt
________________________________________
2. Apply Database Migrations
1.	Run the following command to create migration files:
python manage.py makemigrations
2.	Apply the migrations to your database:
python manage.py migrate
This will create the necessary tables in your database.
________________________________________
3. Populate the Database with Data
1.	Use the setup.py script to populate the database with initial data:
python setup.py
This script will add predefined entries for ActivityLevel and Workout models.
________________________________________
4. Run the Development Server
1.	Start the Django development server:
python manage.py runserver
2.	Open your browser and navigate to:
http://127.0.0.1:8000/
You should see your Django project up and running.
