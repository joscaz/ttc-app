from flask import jsonify, request, current_app, Response
from app.api.controller import (compare_files_and_generate_report, getPruebas, getPruebaById, editPruebaById, deletePrueba)
from app.api.controller import validate_schema_data
# from app.api.utils import (format_report)
from app.api.schema import prueba_load_schema, prueba_dump_schema
from app.api.dummy import (create_dummy_pruebas)
from app.controller import api
from werkzeug.utils import secure_filename
import os


@api.route('/version', methods=['GET'])
def get_version():
    create_dummy_pruebas()
    return "version hola"

@api.route('/upload', methods=['POST'])
def upload_and_compare_file():
    file = request.files['file']
    original_url = request.form.get('original_url')
    id_prueba = request.form.get('id_prueba')
    # critical_locators = request.form.getlist('critical_locators')

    if file and file.filename.endswith('.html'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Leer el contenido del archivo subido
        with open(filepath, 'r', encoding='utf-8') as f:
            file_content = f.read()

        # Comparar archivos y generar reporte
        report_path, total_changes, broken_locators = compare_files_and_generate_report(filepath, original_url, file_content, id_prueba)

        return jsonify({
            'message': 'Report generated successfully.',
            'report_path': report_path,
            'total_changes': total_changes,
            'critical_locators_broken': len(broken_locators),
            'broken_locators': broken_locators
        })
    else:
        return jsonify({'error': 'Invalid file type.'}), 400
    
@api.route('/pruebas', methods=['GET'])
def get_pruebas():
    count, pruebas = getPruebas()
    return jsonify({"Cantidad de pruebas: ": count, "Pruebas: ": pruebas})

@api.route('/pruebas/<int:id>', methods=['GET'])
def get_prueba_by_id(id):
    prueba = getPruebaById(id)
    if prueba:
        return jsonify({"prueba":prueba})
    return jsonify("Prueba no encontrada"), 404

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

    return jsonify("Prueba no encontrada"), 404

@api.route('/pruebas/<int:id>', methods=['DELETE'])
def delete_prueba(id):
    prueba = getPruebaById(id)

    if prueba:
        deletePrueba(prueba)
        return Response(status=204)