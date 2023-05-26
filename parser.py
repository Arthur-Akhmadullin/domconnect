import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


LOGIN = "demo-tt1@inet-yar.ru"
PASSWORD = "rNCV14la"
SITE_ADDRESS = "https://proxy6.net/"
USER_PROXY_PAGE = "https://proxy6.net/user/proxy"
LOCATOR_LOGIN_BTN = "//a[@data-role='login']"
LOCATOR_EMAIL_FIELD = '//*[@id="form-login"]/div[1]/div/input'
LOCATOR_PASSWORD_FIELD = '//*[@id="login-password"]'
LOCATOR_FORM_LOGIN_BTN = "//*[@id='form-login']/div[7]/button"
LOCATOR_TABLE_ROW = "//*[starts-with(@id,'el-')]"
LOCATOR_PROXY_IP_PORT = "//*[starts-with(@id,'el-')]/td[3]/ul/li[1]/div[2]/b"
LOCATOR_EXPIRATION_DATE = "//*[starts-with(@id,'el-')]/td[4]/ul/li[1]/div[2]"


driver = webdriver.Chrome(service=Service(r'./chromedriver.exe'))
driver.maximize_window()
driver.get(SITE_ADDRESS)
driver.implicitly_wait(10)

driver.find_element(By.XPATH, LOCATOR_LOGIN_BTN).send_keys(Keys.ENTER)
driver.find_element(By.XPATH, LOCATOR_EMAIL_FIELD).send_keys(LOGIN)
driver.find_element(By.XPATH, LOCATOR_PASSWORD_FIELD).send_keys(PASSWORD)
time.sleep(60)
driver.find_element(By.XPATH, LOCATOR_FORM_LOGIN_BTN).send_keys(Keys.ENTER)
time.sleep(10)

# Если страница со списком прокси не загрузилась по причине
# дополнительной проверки через ввод с картинки или ввод кода,
# то приостанавливаем скрипт, проходим проверку и снова жмем кнопку "Войти"
if driver.current_url == SITE_ADDRESS:
    time.sleep(60)
    driver.find_element(By.XPATH, LOCATOR_FORM_LOGIN_BTN).send_keys(Keys.ENTER)

# Проверяем текущий адрес, допуская вероятность его изменения владельцем сайта
time.sleep(5)
if driver.current_url == USER_PROXY_PAGE:
    result = []
    table_rows = driver.find_elements(By.XPATH, LOCATOR_TABLE_ROW)
    if len(table_rows) > 0:
        for _ in range(len(table_rows)):
            proxy_ip_port = driver.find_element(By.XPATH, LOCATOR_PROXY_IP_PORT)
            expiration_date = driver.find_element(By.XPATH, LOCATOR_EXPIRATION_DATE)
            result.append(f"{proxy_ip_port.text} - {expiration_date.text}")
        print(*result, sep="\n")
    else:
        print("Список прокси-портов пуст")
else:
    print("Не получилось перейти по адресу 'https://proxy6.net/user/proxy'")
