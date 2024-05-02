from flask import jsonify, request
from app.controller import api

@api.route('/version', methods=['GET'])
def get_version():
    return "version hola"