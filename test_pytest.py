import pytest
from selenium import webdriver
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException

@pytest.fixture(scope='session')
def driver():
    driver = webdriver.Edge()
    driver.get("http://127.0.0.1:5500/htmlPages/loginPageTest.html")
    yield driver
    driver.quit()

def test_login_page_title(driver):
    """Verifica que el título de la página de inicio de sesión sea correcto"""
    assert "Pagina de pruebas" in driver.title

# def test_incorrect_page_title(driver):
#     """Verificar que el título de la página de inicio de sesión sea incorrecto"""
#     assert "Título Incorrecto" not in driver.title

def test_login_with_valid_credentials(driver):
    """Prueba que el usuario pueda iniciar sesión con credenciales válidas"""
    text_box_user = driver.find_element(by=By.ID, value="user")
    text_box_pswd = driver.find_element(by=By.NAME, value="pswd")
    submit_button = driver.find_element(by=By.ID, value="submit_btn")

    text_box_user.send_keys("admin")
    text_box_pswd.send_keys("admin")
    submit_button.click()

    try:
        alert = Alert(driver)
        alert_text = alert.text
        assert False, f"Se mostró una alerta inesperada: {alert_text}"
    except NoAlertPresentException:
        assert 1 == 1
        pass

    # expected_url = "http://127.0.0.1:5500/htmlPages/mainPageTest.html"
    # current_url = driver.current_url
    # assert current_url == expected_url, f"La URL actual ({current_url}) no coincide con la URL esperada ({expected_url})"

    # main_page_title = driver.title
    # assert main_page_title == "Main Page"


def test_login_with_invalid_credentials(driver):
    """Prueba que el usuario no pueda iniciar sesión con credenciales inválidas"""
    text_box_user = driver.find_element(by=By.ID, value="user")
    text_box_pswd = driver.find_element(by=By.NAME, value="pswd")
    submit_button = driver.find_element(by=By.ID, value="submit_btn")

    text_box_user.send_keys("invalid_user")
    text_box_pswd.send_keys("invalid_password")
    submit_button.click()

    # Verificar que se muestre un mensaje de error
    alert = Alert(driver)
    alert_text = alert.text
    expected_alert_text = "El usuario o el password no estan correctos. Por favor, verifique los datos."
    assert alert_text == expected_alert_text
    alert.accept()

    current_url = driver.current_url
    print(current_url)
    assert "http://127.0.0.1:5500/htmlPages/loginPageTest.html" in current_url

# def test_detect_changes_in_page_elements(driver):
#     """Prueba que el framework pueda detectar cambios en los elementos de la página"""
#     # Obtener un elemento de referencia
#     element_reference = driver.find_element(by=By.ID, value="my-text-id")

#     # Simular un cambio en el elemento
#     driver.execute_script("arguments[0].id = 'new-id';", element_reference)

#     # Verificar que el framework detecte el cambio
#     assert detect_element_change(driver, element_reference, "new-id")

# def detect_element_change(driver, element, new_locator):
#     """
#     Método auxiliar para comprobar si el framework detecta cambios en los elementos.
#     Devuelve True si se detecta el cambio, False en caso contrario.
#     """
#     try:
#         driver.find_element(by=By.ID, value=new_locator)
#         return True
#     except:
#         return False