from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from config import Config
from locators.main_login_locators import MainLoginLocators
from pages.base_page import BasePage

class MainLoginPage(BasePage):
    def __init__(self):
        self.driver = Config.get_driver()
        self.driver.get(Config.BASE_URL) 
    
    def enter_username(self, username):
        self.write(MainLoginLocators.USER_NAME_FIELD, username)
        
    def enter_password(self, password):
        self.write(MainLoginLocators.PASSWORD_FIELD, password)

    def click_login_button(self):
        self.clickOn(MainLoginLocators.LOGIN_BUTTON)
        