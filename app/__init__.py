from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from flask_cors import CORS
from .models import db, User
from .api import api
from .ig import ig

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(api)
app.register_blueprint(ig)

db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
moment = Moment(app)
CORS(app)

@login_manager.user_loader
def load_user(user_id):
    # return User.query.filter_by(id=user_id).first()
    return User.query.get(user_id)

login_manager.login_view='login_page'



from . import routes, models