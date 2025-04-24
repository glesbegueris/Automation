from selenium.webdriver.common.by import By

class MainLoginLocators:
    """
    Locators for the main login page.
    """

    USER_NAME_FIELD = (By.XPATH, "//input[@id='username']")
    PASSWORD_FIELD = (By.XPATH, "//input[@id='password']")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), 'Continue')]")
    