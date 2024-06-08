from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument("--headless")
# options.add_argument("window-size=1400,1500")
# options.add_argument("--disable-gpu")
# options.add_argument("--no-sandbox")
# options.add_argument("start-maximized")
# options.add_argument("enable-automation")
# options.add_argument("--disable-infobars")
# options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

# driver.get("https://www.selenium.dev/selenium/web/web-form.html")
driver.get("http://127.0.0.1:5500/app/tests/selenium/htmlPages/loginPageTest.html")

title = driver.title

assert "Pagina de pruebas" in title

driver.implicitly_wait(0.5)

# text_box_id = driver.find_element(by=By.ID, value="my-text-id")
# text_box_name = driver.find_element(by=By.NAME, value="my-text")
# submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

text_box_user = driver.find_element(by=By.ID, value="user")
text_box_pswd = driver.find_element(by=By.NAME, value="pswd")
submit_button = driver.find_element(by=By.ID, value="submit_btn")

text_box_user.send_keys("admin")
text_box_pswd.send_keys("admin")
submit_button.click()


# message = driver.find_element(by=By.ID, value="message")
# text = message.text

driver.quit()