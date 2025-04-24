import time
import pytest
from pages.main_login_page import MainLoginPage

class TestMainLogin:
    @pytest.mark.smoke
    def test_login_successful_C01(self):
        login_page = MainLoginPage()
        login_page.enter_username("starter-dev@calice.ai")
        login_page.enter_password("myPassword1234")
        login_page.click_login_button()
        #login_page.close()

   