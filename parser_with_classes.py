import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class ProxyLocators:
    SITE_ADDRESS = "https://proxy6.net/"
    USER_PROXY_PAGE = "https://proxy6.net/user/proxy"
    LOCATOR_LOGIN_BTN = "//a[@data-role='login']"
    LOCATOR_EMAIL_FIELD = '//*[@id="form-login"]/div[1]/div/input'
    LOCATOR_PASSWORD_FIELD = '//*[@id="login-password"]'
    LOCATOR_FORM_LOGIN_BTN = "//*[@id='form-login']/div[7]/button"
    LOCATOR_TABLE_ROW = "//*[starts-with(@id,'el-')]"
    LOCATOR_PROXY_IP_PORT = "//*[starts-with(@id,'el-')]/td[3]/ul/li[1]/div[2]/b"
    LOCATOR_EXPIRATION_DATE = "//*[starts-with(@id,'el-')]/td[4]/ul/li[1]/div[2]"


class SearchProxy:
    def __init__(self, login, password):
        self.driver = webdriver.Chrome(service=Service(r'./chromedriver.exe'))
        self.driver.maximize_window()
        self.driver.get(ProxyLocators.SITE_ADDRESS)
        self.driver.implicitly_wait(10)
        self.login = login
        self.password = password

    def login_account(self):
        self.driver.find_element(By.XPATH, ProxyLocators.LOCATOR_LOGIN_BTN).send_keys(Keys.ENTER)
        self.driver.find_element(By.XPATH, ProxyLocators.LOCATOR_EMAIL_FIELD).send_keys(self.login)
        self.driver.find_element(By.XPATH, ProxyLocators.LOCATOR_PASSWORD_FIELD).send_keys(self.password)
        time.sleep(60)
        self.driver.find_element(By.XPATH, ProxyLocators.LOCATOR_FORM_LOGIN_BTN).send_keys(Keys.ENTER)
        time.sleep(10)

        # Если страница со списком прокси не загрузилась по причине
        # дополнительной проверки через ввод с картинки или ввод кода,
        # то приостанавливаем скрипт, проходим проверку и снова жмем кнопку "Войти"
        if self.driver.current_url == ProxyLocators.SITE_ADDRESS:
            time.sleep(60)
            self.driver.find_element(By.XPATH, ProxyLocators.LOCATOR_FORM_LOGIN_BTN).send_keys(Keys.ENTER)

    def get_proxy(self):
        # Проверяем текущий адрес, допуская вероятность его изменения владельцем сайта
        time.sleep(5)
        if self.driver.current_url == ProxyLocators.USER_PROXY_PAGE:
            result = []
            table_rows = self.driver.find_elements(By.XPATH, ProxyLocators.LOCATOR_TABLE_ROW)
            if len(table_rows) > 0:
                for _ in range(len(table_rows)):
                    proxy_ip_port = self.driver.find_element(By.XPATH, ProxyLocators.LOCATOR_PROXY_IP_PORT)
                    expiration_date = self.driver.find_element(By.XPATH, ProxyLocators.LOCATOR_EXPIRATION_DATE)
                    result.append(f"{proxy_ip_port.text} - {expiration_date.text}")
                print(*result, sep="\n")
            else:
                print("Список прокси-портов пуст")
        else:
            print("Не получилось перейти по адресу 'https://proxy6.net/user/proxy'")

SP = SearchProxy("demo-tt1@inet-yar.ru", "rNCV14la")
SP.login_account()
SP.get_proxy()