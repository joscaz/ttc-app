import pytest
from flask import Flask
from flask_cors import CORS
from app import db
from app.controller import api as api_module
from app.api.codigo.model import Codigo

@pytest.fixture(scope="session")
def app():
  my_app = Flask(__name__)
  CORS(my_app)

  my_app.config.from_object('config')
  my_app.config['TESTING'] = True
  my_app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+pg8000://user:password@test_ttc_app_db/test_ttc_app_db'

  return my_app

@pytest.fixture(scope="session")
def sqlalchemy(app):
  with app.app_context():    
    app.register_blueprint(api_module)
    db.init_app(app)
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()

@pytest.fixture(scope="session")
def create_codigo(sqlalchemy, create_agent):
  codigo_data = {
    'id_codigo': 1,
    'nombre_archivo': 'prueba_pytest.html',
    'contenido': 'xxx x xxx x xx xxxxx x x x x x ',
    'fecha_subida': '2025-01-01T00:00:00'
  }
  codigo = Codigo(**codigo_data)
  db.session.add(codigo)
  db.session.commit()
  return codigo

@pytest.fixture(scope="session")
def client(app, sqlalchemy, create_codigo):
  with app.test_client() as client:
    yield client

@pytest.fixture(scope="session")
def url_prefix(app):
  url_prefix = '/ttc-api/'
    
  return url_prefix