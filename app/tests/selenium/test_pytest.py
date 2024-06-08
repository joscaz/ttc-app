import pytest
from selenium import webdriver
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.keys import Keys

options = Options()
options.add_argument("--headless")
options.add_argument("window-size=1400,1500")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("start-maximized")
options.add_argument("enable-automation")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")

@pytest.fixture(scope='session')
def driver():
    driver = webdriver.Chrome(options=options)
    driver.get("http://127.0.0.1:5500/app/tests/selenium/htmlPages/loginPageTest.html")
    yield driver
    driver.quit()


def test_login_page_title(driver):
    """Verifica que el título de la página de inicio de sesión sea correcto"""
    assert "Pagina de pruebas" in driver.title

# def test_incorrect_page_title(driver):
#     """Verificar que el título de la página de inicio de sesión sea incorrecto"""
#     assert "Título Incorrecto" not in driver.title


#
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

    # current_url = driver.current_url
    # print(current_url)
    # assert "http://127.0.0.1:5500/htmlPages/loginPageTest.html" in current_url


# Comprobar que las imágenes estén cargadas
def test_loading_images(driver):
    driver.get('http://127.0.0.1:5500/app/tests/selenium/htmlPages/mainPageTest.html')
    imagenes = driver.find_elements(by=By.ID, value="img")
    for imagen in imagenes:
        assert imagen.is_displayed(), "La imagen no se ha cargado correctamente"

 
# Comprobar titulo
def test_main_page_title(driver):
    driver.get('http://127.0.0.1:5500/app/tests/selenium/htmlPages/mainPageTest.html')
    elemento_titulo = driver.find_element(by=By.ID, value="titulo")
    texto_esperado = "AutoRefine"
    assert elemento_titulo.text == texto_esperado, f"El texto del título es '{elemento_titulo.text}', pero se esperaba '{texto_esperado}'"

# Comprobar los párrafos
def test_paragraph_quantity(driver):
    driver.get('http://127.0.0.1:5500/app/tests/selenium/htmlPages/mainPageTest.html')
    parrafos_esperados = 2
    parrafos = driver.find_elements(by=By.TAG_NAME, value="p")
    assert len(parrafos) == parrafos_esperados, f"La cantidad de párrafos no es la esperada. Se esperaban {parrafos_esperados}, pero se encontraron {len(parrafos)}"


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