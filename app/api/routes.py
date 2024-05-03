from flask import jsonify, request, current_app
from app.api.controller import (process_with_selenium, save_report_and_code)
from app.api.utils import (format_report)
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
    prueba_ids = request.form.get('prueba_ids')

    if file and file.filename.endswith('.html'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # original_url = 'http://127.0.0.1:5500/app/tests/selenium/htmlPages/mainPageTest.html'
        report = process_with_selenium(original_url, filepath)

        if isinstance(report, dict):
            formatted_report = format_report(report)

            prueba_ids = [int(id.strip()) for id in prueba_ids.split(',')]

            for id_prueba in prueba_ids:
                save_report_and_code(filename, report, filepath, id_prueba)
            
            return jsonify({"message": "Archivo procesado y reporte generado.", "reporte": formatted_report}), 200
        else:
            return jsonify({"message": "No se detectaron diferencias significativas."}), 200
    else:
        return jsonify({"error": "Archivo no válido"}), 400
