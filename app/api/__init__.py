from flask import Blueprint

api = Blueprint('api', __name__, url_prefix='/api')

from . import ig_routes
from . import shop_routes