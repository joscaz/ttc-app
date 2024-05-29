from app import db
from app.api.model import Codigo, Reporte, Prueba
from app.controller import  RequestException
from app.api.schema import CodigoSchema, ReporteSchema, PruebaSchema, prueba_dump_schema, prueba_load_schema
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
# from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
import logging
import datetime
# from app.api.utils import (compare_elements, wait_for_page_load, capture_element_data)

# Configuración del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def wait_for_page_load(driver):
    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script('return document.readyState') == 'complete'
    )

def capture_element_data(elements):
    return [{'tag': e.tag_name, 'text': e.text, 'attributes': e.get_attribute('outerHTML'), 'xpath': e.get_attribute('xpath')} for e in elements]

def check_critical_locators(driver, locators):
    broken_locators = []
    for locator in locators:
        try:
            driver.find_element(By.XPATH, locator)
        except NoSuchElementException:
            broken_locators.append(locator)
    return broken_locators

# critical_locators = [
#     '//img[@alt="TTC Logo"]',
#     '//h1[@id="titulo"]',
#     '//div[@class="mission-vision"]/h2[1]',
#     '//div[@class="mission-vision"]/h2[2]',
#     '//p[@id="adios"]',
#     '//img[@alt="Python"]',
#     '//img[@alt="Selenium"]',
#     '//img[@alt="AWS"]',
#     '//div[@class="nombres"]/h4[1]',
#     '//div[@class="nombres"]/h4[2]',
#     '//div[@class="nombres"]/h4[3]'
#     # Añade otros XPaths críticos aquí.
# ]

def get_xpath_for_element(element: WebElement) -> str:
    """
    Generate a more specific XPath for a given web element by incorporating attributes like 'id' and 'class'.
    """
    parts = []
    while element.tag_name != 'html':
        part = element.tag_name
        # Añadir atributos 'id' o 'class' si están presentes para hacer el XPath más específico.
        id_ = element.get_attribute('id')
        class_ = element.get_attribute('class')
        if id_:
            part += f"[@id='{id_}']"
        elif class_:
            class_ = class_.split()[0]  # Usar solo la primera clase si hay varias
            part += f"[@class='{class_}']"
        else:
            # Contar la posición relativa entre los elementos hermanos del mismo tipo
            siblings = element.find_elements(By.XPATH, f'./preceding-sibling::{element.tag_name}') + element.find_elements(By.XPATH, f'./following-sibling::{element.tag_name}')
            if siblings:
                index = len(element.find_elements(By.XPATH, f'./preceding-sibling::{element.tag_name}')) + 1
                part += f"[{index}]"
        parts.insert(0, part)
        element = element.find_element(By.XPATH, '..')
    return '//' + '/'.join(parts)

def capture_all_locators(driver, url):
    driver.get(url)
    elements = driver.find_elements(By.XPATH, '//*')
    locators = [get_xpath_for_element(e) for e in elements if e.tag_name != 'html']
    return locators

def compare_files_and_generate_report(new_file_path, original_url, file_content, id_pruebas):
    # Configurar el WebDriver
    driver = webdriver.Edge()
    
    try:
        new_code = Codigo(nombre_archivo='archivo_a_probar', contenido=file_content)
        db.session.add(new_code)
        db.session.commit()  # Asegúrate de que se guarda correctamente y obtiene un ID

        # Cargar la página original
        driver.get(original_url)
        critical_locators_original = capture_all_locators(driver, original_url)
        wait_for_page_load(driver)
        original_elements = driver.find_elements(By.XPATH, '//*')
        original_data = capture_element_data(original_elements)

        # Cargar la página del archivo subido
        driver.get('file:///' + new_file_path)
        wait_for_page_load(driver)
        new_elements = driver.find_elements(By.XPATH, '//*')
        new_data = capture_element_data(new_elements)
        critical_locators_new = capture_all_locators(driver, 'file:///' + new_file_path)

            # Identificar locators rotos y nuevos
        broken_locators_original = [loc for loc in critical_locators_original if loc not in critical_locators_new]
        broken_locators_new = [loc for loc in critical_locators_new if loc not in critical_locators_original]


        # Comparar los datos capturados
        differences = []
        for original, new in zip(original_data, new_data):
            if original['text'] != new['text'] or original['attributes'] != new['attributes']:
                differences.append({'Original': original, 'New': new})

        # Verificar localizadores críticos en la página nueva
        # broken_locators = check_critical_locators(driver, critical_locators)
        total_changes = len(differences)

        # Crear reporte xlsx solo con locators rotos
        df_original = pd.DataFrame(broken_locators_original, columns=['Original broken/missing locators'])
        df_new = pd.DataFrame(broken_locators_new, columns=['New added/broken locators'])
        df_combined = pd.concat([df_original, df_new], axis=1)
        report_path = 'prueba.xlsx'
        df_combined.to_excel(report_path, index=False)

        # Instanciar y guardar el reporte
        new_report = Reporte(contenido=str(broken_locators_original + broken_locators_new), id_pruebas=id_pruebas, id_codigo=new_code.id_codigo)
        db.session.add(new_report)
        db.session.commit()

        return report_path, total_changes, broken_locators_original, broken_locators_new
    # except Exception as e:
    #     raise RequestException(message=e.messages, code=400)
    finally:
        driver.quit()

def getPruebas():
    pruebas = Prueba.query.all()
    prueba_schema = PruebaSchema(many=True)
    all_pruebas = prueba_schema.dump(pruebas)
    count = Prueba.query.count()
    return count, all_pruebas
    
def getPruebaById(id):
    prueba = Prueba.query.filter_by(id_prueba=id).first()
    prueba_schema = PruebaSchema()
    prueba_dumped = prueba_schema.dump(prueba)
    return prueba_dumped

def editPruebaById(id, data):
    Prueba.query.filter_by(id_prueba=id).update(data)
    db.session.commit()
    return Prueba.query.filter_by(id_prueba=id).first()

def deletePrueba(prueba):
    prueba.delete()
    db.session.commit()