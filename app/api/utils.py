from collections import defaultdict
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from deepdiff import DeepDiff
import logging

def wait_for_page_load(driver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

def capture_element_data(elements):
    data = {}
    for el in elements:
        if el.is_displayed():
            el_data = {
                'tag_name': el.tag_name,
                'text': el.text,
                'css_class': el.get_attribute('class') or "",
                'id': el.get_attribute('id') or "",
                'style': el.get_attribute('style') or ""
            }
            el_id = el.get_attribute('id') or f"no-id-{id(el)}"
            data[el_id] = el_data
    return data

def compare_elements(original_data, new_data):
    differences = DeepDiff(original_data, new_data, ignore_order=True, verbose_level=2)
    report = {}

    def filter_changes(changes):
        filtered = {}
        for key, value in changes.items():
            key_clean = key.split('root')[1]  # Limpiar la clave para hacerla más legible
            if 'id' in value or 'css_class' in value or 'tag_name' in value:
                filtered[key_clean] = {
                    'id': value.get('id', 'N/A'),
                    'tag_name': value.get('tag_name', 'N/A'),
                    'css_class': value.get('css_class', 'N/A'),
                    'style': value.get('style', 'N/A'),
                    'text': value.get('text', 'N/A')
                }
        return filtered

    if 'dictionary_item_added' in differences:
        report['archivo_subido'] = filter_changes(differences['dictionary_item_added'])
    if 'dictionary_item_removed' in differences:
        report['archivo_original'] = filter_changes(differences['dictionary_item_removed'])
    if 'values_changed' in differences:
        report['cambios_detectados'] = filter_changes(differences['values_changed'])

    return report


def format_report(differences):
    formatted = defaultdict(dict)
    for category, changes in differences.items():
        for key, value in changes.items():
            formatted[category][key] = value
    return dict(formatted)