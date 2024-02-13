#Initialize Flask app and database here.
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #database name
db = SQLAlchemy(app)
app.secret_key = 'your_secret_key_here'
migrate = Migrate(app, db)


from app import routes
