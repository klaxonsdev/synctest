from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app=app, db=db)
ma = Marshmallow(app)
login = LoginManager(app)
login.login_view = 'login'

<<<<<<< HEAD
from app import routes, models
=======
from app import routes, models, errors
>>>>>>> 10750702af3896eb6f04cbff45a48b730e2ee503
