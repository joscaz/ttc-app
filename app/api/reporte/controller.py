from app import db
from app.api.codigo.model import Codigo
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from app.api.elemento.model import Elemento
from app.api.reporte.model import Reporte
from selenium.webdriver.remote.webelement import WebElement
import pandas as pd
import logging
from thefuzz import fuzz

options = Options()
options.add_argument("--headless")
options.add_argument("window-size=1400,1500")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("start-maximized")
options.add_argument("enable-automation")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def wait_for_page_load(driver):
    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script('return document.readyState') == 'complete'
    )

def check_critical_locators(driver, locators):
    broken_locators = []
    for locator in locators:
        try:
            driver.find_element(By.XPATH, locator)
        except NoSuchElementException:
            broken_locators.append(locator)
    return broken_locators

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

def suggest_locator(broken_locator, candidate_locators):
    # Encuentra el locator candidato más similar al roto
    best_match = None
    highest_score = 0
    for candidate in candidate_locators:
        score = fuzz.ratio(broken_locator, candidate)
        if score > highest_score:
            highest_score = score
            best_match = (candidate, score)
    return best_match

def compare_files_and_generate_report(new_file_path, original_url, file_content, id_pruebas):
    # Configurar el WebDriver
    driver = webdriver.Chrome(options=options)
    
    try:
        new_code = Codigo(nombre_archivo='archivo_a_probar', contenido=file_content)
        db.session.add(new_code)
        db.session.commit()

        # Cargar página original
        driver.get(original_url)
        critical_locators_original = capture_all_locators(driver, original_url)
        wait_for_page_load(driver)

        # Cargar página del archivo subido
        driver.get('file:///' + new_file_path)
        wait_for_page_load(driver)
        critical_locators_new = capture_all_locators(driver, 'file:///' + new_file_path)

        # Identificar locators rotos y nuevos
        broken_locators_original = [loc for loc in critical_locators_original if loc not in critical_locators_new]
        broken_locators_new = [loc for loc in critical_locators_new if loc not in critical_locators_original]

        # Registrar localizadores rotos y nuevos en la base de datos
        for idx, locator in enumerate(broken_locators_original):
            new_element = Elemento(nombre=f'Original{idx}', localizador=locator, estado=False)  # Estado False por defecto
            db.session.add(new_element)
        
        for idx, locator in enumerate(broken_locators_new):
            new_element = Elemento(nombre=f'New{idx}', localizador=locator, estado=False)  # Estado False por defecto
            db.session.add(new_element)

        db.session.commit()

        suggestions = {}
        for locator in broken_locators_new:
            match = suggest_locator(locator, broken_locators_original)
            if match:
                suggested_locator, score = match
                if score > 70:
                    suggestions[locator] = {'suggestion': suggested_locator, 'score': score}

        # Crear reporte xlsx solo con locators rotos
        df_original = pd.DataFrame(broken_locators_original, columns=['Original broken/missing locators'])
        df_new = pd.DataFrame(broken_locators_new, columns=['New added/broken locators'])
        df_empty = pd.DataFrame([["", ""] for _ in range(max(len(df_original), len(df_new)))], columns=[' ', ' '])
        df_suggestions = pd.DataFrame([(k, v['suggestion'], v['score']) for k, v in suggestions.items()], columns=['Original locator', 'Suggestion', 'Score'])
        df_combined = pd.concat([df_original, df_new, df_empty, df_suggestions], axis=1)
        report_path = 'excel_files/prueba.xlsx'
        df_combined.to_excel(report_path, index=False)
        
        new_report = Reporte(contenido=str(broken_locators_original + broken_locators_new), id_pruebas=id_pruebas, id_codigo=new_code.id_codigo)
        db.session.add(new_report)
        db.session.commit()

        return report_path, broken_locators_original, broken_locators_new, suggestions
    # except Exception as e:
    #     raise RequestException(message=e.messages, code=400)
    finally:
        driver.quit()
