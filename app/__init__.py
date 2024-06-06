from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_migrate import Migrate
import logging

# WSGI application obj
flask_app = Flask(__name__)
CORS(flask_app)

# Configurations
flask_app.config.from_object('config')

db = SQLAlchemy()
db.init_app(flask_app)
migrate = Migrate(flask_app, db)
ma = Marshmallow(flask_app)
# ma.init_app(flask_app)

# Configure Flask logging
logging.getLogger().setLevel(logging.INFO)
flask_app.logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
flask_app.logger.addHandler(handler)

#Service Healthcheck 
@flask_app.route(f'/healthcheck', methods=['GET'])
def healthcheck():
  return 'Healthy'

import app.api.codigo.model
import app.api.elemento.model
import app.api.prueba.model
import app.api.reporte.model
import app.api.version.model

from app.controller import api as api_module

flask_app.register_blueprint(api_module)