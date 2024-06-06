from app import flask_app
from werkzeug.exceptions import HTTPException
from flask import Blueprint, request, current_app, jsonify, g
from marshmallow import ValidationError

def get_url_prefix():
  url_prefix = '/ttc-api/'

  return url_prefix

api = Blueprint('ttc-api', __name__, url_prefix=get_url_prefix())

def validate_schema_data(schema, data):
  try:
    loaded_data = schema.load(data)
  except ValidationError as err:
    raise RequestException(message=err.messages, code=400)

  return loaded_data

def log_request_error(request_data, code):
    # Log the request data and the error
    current_app.logger.error(f"Error {code} at {request_data['url']}")
    current_app.logger.error(f"Method: {request_data['method']}")
    current_app.logger.error(f"Headers: {request_data['headers']}")
    current_app.logger.error(f'Request Data: {request_data["data"]}')

def validate_schema_data(schema, data):
  try:
    loaded_data = schema.load(data)
  except ValidationError as err:
    raise RequestException(message=err.messages, code=400)
  
  return loaded_data


def get_request_data():
    # Access request data
    request_data = {
        'url': request.url,
        'method': request.method,
        'headers': dict(request.headers),
        'data': None
    }

    # Check if the request is JSON and log the data
    if request.is_json:
        try:
            request_data['data'] = request.json
        except Exception as json_error:
            flask_app.logger.error(f'Error parsing JSON: {json_error}')

    # If the request is not JSON, log the data as text
    if request_data['data'] is None:
        request_data['data'] = request.data.decode('utf-8')
    
    return request_data

@flask_app.errorhandler(500)
def handle_internal_server_error(e):
    request_data = get_request_data()
    log_request_error(request_data=request_data, code=500)

    # You can return a custom response if desired
    # response = jsonify({'error': 'Internal Server Error'})
    # response.status_code = 500
    return jsonify(error=str(e)), 500


class RequestException(HTTPException):
  def __init__(self, message, code):
    self.message = message
    self.code = code
    super().__init__(self.message)

def request_exception(e):
    return jsonify(error=str(e)), e.code

flask_app.register_error_handler(RequestException, request_exception)

import app.api.reporte.routes
import app.api.prueba.routes