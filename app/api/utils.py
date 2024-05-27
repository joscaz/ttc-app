from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def wait_for_page_load(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "body")))

test_mappings = {
    1: 'test_login_page_title',
    2: 'test_login_with_valid_credentials',
    3: 'test_login_with_invalid_credentials',
    4: 'test_loading_images',
    5: 'test_main_page_title',
    6: 'test_paragraph_quantity'
}