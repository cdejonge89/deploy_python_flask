from flask import Flask 
app = Flask(__name__)
app.secret_key = "shhhh"
DATABASE = "affirmation_schema"
