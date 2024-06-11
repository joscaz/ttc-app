from flask import jsonify, request, current_app, send_from_directory
from app import db
from app.api.reporte.controller import (compare_files_and_generate_report, updateSuggestion)
from app.api.prueba.model import Prueba
from app.controller import RequestException
from app.controller import api
from werkzeug.utils import secure_filename
from app.api.reporte.utils import test_mappings
import pytest
import os

@api.route('/download_excel', methods=['GET'])
def download_excel():
    directory = current_app.config['EXCEL_FOLDER'] # El directorio donde se guardan los archivos generados
    print(directory)
    filename = "prueba.xlsx"  # El nombre del archivo que quieres enviar
    try:
        return send_from_directory(directory, filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    
@api.route('/update_suggestion', methods=['POST'])
def update_suggestion():
    data = request.get_json()
    locator = data['locator']
    action = data['action']
    print('Locator received:', locator)
    response = updateSuggestion(locator, action)
    return jsonify(response)
    
@api.route('/upload', methods=['POST'])
def upload_and_compare_file():
    file = request.files['file']
    original_url = request.form.get('original_url')
    ids_pruebas_str = request.form.get('id_pruebas')  # IDs como cadena separada por comas
    id_pruebas = [int(id) for id in ids_pruebas_str.split(',') if id.strip().isdigit()]

    if file and file.filename.endswith('.html'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Iniciar pruebas pytest
        results = {}
        for id_prueba in id_pruebas:
            if id_prueba in test_mappings:
                result = pytest.main(['-k', test_mappings[id_prueba]])
                results[id_prueba] = result == 0  # True si la prueba pasó, False si falló
                # Registrar en la base de datos
                new_prueba = Prueba(
                    nombre_prueba=test_mappings[id_prueba],
                    estado=(result == 0),
                    cambio_aceptado=False
                )
                db.session.add(new_prueba)

        # Leer el contenido del archivo subido
        with open(filepath, 'r', encoding='utf-8') as f:
            file_content = f.read()

        # Comparar archivos y generar reporte
        (report_path, 
         broken_locators_original,
         broken_locators_new,
         suggestions) = compare_files_and_generate_report(filepath,
                                                          original_url,
                                                          file_content,
                                                          id_pruebas)

        return jsonify({
            'message': 'Report generated successfully.',
            'report_path': report_path,
            'tests_passed': sum(results.values()),
            'tests_failed': len(results) - sum(results.values()),
            'broken_locators_original': len(broken_locators_original),
            'broken_locators_new': len(broken_locators_new),
            'suggestions': suggestions,
            'broken_locators_details': {
                'original': broken_locators_original,
                'new': broken_locators_new
            }
        })
    else:
        raise RequestException(message="Invalid file type", code=400)