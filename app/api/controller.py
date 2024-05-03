from app import db
from app.api.model import Codigo, Reporte, Prueba
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import logging
import datetime
from app.api.utils import (compare_elements, wait_for_page_load, capture_element_data)

# Configuración del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_with_selenium(original_url, filepath):
    driver = webdriver.Edge()  # Asegúrate de tener el driver correspondiente configurado
    try:
        # Cargar la página original
        driver.get(original_url)
        wait_for_page_load(driver)
        original_elements = driver.find_elements(By.XPATH, '//*')
        original_data = capture_element_data(original_elements)

        # Cargar la página del archivo subido
        driver.get('file:///' + filepath)
        wait_for_page_load(driver)
        new_elements = driver.find_elements(By.XPATH, '//*')
        new_data = capture_element_data(new_elements)
    
        differences = compare_elements(original_data, new_data)
    
        if not isinstance(differences, dict):
            logging.error(f"Expected a dictionary from compare_elements, got {type(differences)}")

        # Guardar los resultados en un CSV
        with open("differences_report.csv", "w", newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Element ID', 'Attribute', 'Original Value', 'New Value'])
            for el_id, attrs in differences.items():
                for attr, values in attrs.items():
                    original = values.get('old_value', 'N/A')
                    new = values.get('new_value', 'N/A')
                    writer.writerow([el_id, attr, original, new])

        return differences
    except Exception as e:
        logging.error(f"Exception occurred: {str(e)}")

    finally:
        driver.quit()

def save_report_and_code(filename, report, filepath, id_prueba):
    # Leer el contenido del archivo si es necesario
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()

    new_code = Codigo(nombre_archivo=filename, contenido=content)  # Cambia 'filepath' por 'content' si es necesario
    db.session.add(new_code)
    db.session.flush()  # Para obtener el id_codigo después de insertar

    new_report = Reporte(contenido=str(report), id_prueba=id_prueba, id_codigo=new_code.id_codigo)
    db.session.add(new_report)
    db.session.commit()