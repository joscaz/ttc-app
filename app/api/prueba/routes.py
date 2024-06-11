from flask import jsonify, request, current_app, Response
from app.controller import (RequestException, api, validate_schema_data)
from app.api.prueba.controller import (getPruebas, getPruebaById, editPruebaById, deletePrueba)
from app.api.prueba.schema import prueba_load_schema, prueba_dump_schema
  
@api.route('/pruebas', methods=['GET'])
def get_pruebas():
    count, pruebas = getPruebas()
    return jsonify({"Cantidad de pruebas: ": count, "Pruebas: ": pruebas})

@api.route('/pruebas/<int:id>', methods=['GET'])
def get_prueba_by_id(id):
    prueba = getPruebaById(id)
    if prueba:
        return jsonify({"prueba":prueba})
    raise RequestException(message="Test not found", code=404)

@api.route('/pruebas/<int:id>', methods=['PUT'])
def update_prueba_by_id(id):
    schema = prueba_load_schema()  
    loaded_data = validate_schema_data(schema, request.get_json())
    prueba = getPruebaById(id)

    if prueba:
        prueba = editPruebaById(id, loaded_data)
        schema = prueba_dump_schema()
        result = schema.dump(prueba)
        return jsonify({"prueba": result})

    raise RequestException(message="Test not found", code=404)

@api.route('/pruebas/<int:id>', methods=['DELETE'])
def delete_prueba(id):
    prueba = getPruebaById(id)

    if prueba:
        deletePrueba(prueba)
        return Response(status=204)