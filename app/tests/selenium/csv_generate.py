from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import csv
import logging

# Configuración del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("window-size=1400,1500")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("start-maximized")
options.add_argument("enable-automation")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")

# Configuración del driver de Selenium
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)  # Opciones: Chrome, Firefox, etc.
url = "https://c3.ai/"

try:
    # Acceder a la página web
    driver.get(url)

    # Extraer detalles de un elemento web
    def obtener_detalles_elemento(elemento):
        try:
            detalles = {
                "tag_name": elemento.tag_name,
                "id": elemento.get_attribute("id"),
                "name": elemento.get_attribute("name"),
                "type": elemento.get_attribute("type"),
                "value": elemento.get_attribute("value"),
                "text": elemento.text
            }
            return detalles
        except Exception as e:
            logging.error(f"Error al obtener detalles del elemento: {e}")
            return None

    # Extracción de elementos
    inputs = driver.find_elements(By.TAG_NAME, "input")
    botones = driver.find_elements(By.TAG_NAME, "button")

    detalles_inputs = [obtener_detalles_elemento(input) for input in inputs if input]
    detalles_botones = [obtener_detalles_elemento(boton) for boton in botones if boton]

    # Escribir en el CSV
    with open("detalles_pagina.csv", "w", newline="", encoding="utf-8") as archivo_csv:
        if detalles_inputs:
            writer = csv.DictWriter(archivo_csv, fieldnames=detalles_inputs[0].keys())
            writer.writeheader()
            for detalle in detalles_inputs + detalles_botones:
                if detalle:
                    writer.writerow(detalle)

except Exception as e:
    logging.error(f"Error durante la ejecución del script: {e}")
finally:
    # Cerrar el driver de Selenium
    driver.quit()
