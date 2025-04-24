rom selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
#from pytest_testconfig import config
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import os
import time 
import platform
from selenium.common.exceptions import ElementClickInterceptedException


                          

class BasePage():
    
    def __init__(self, browser):
        self.browser = browser   
        self.explicit_wait = WebDriverWait(
            timeout=15,
            driver=self.browser,
            poll_frequency=1.0,
            ignored_exceptions={
            },
        )
    
    def scrollDown(self):
        html = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'html')))
        self.repeatSeach(html)
        html.send_keys([Keys.END])
        
  
        
    def test_text(self, element, textok):
        textElement = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, element)))
        self.repeatSeach(textElement)
        textreal = textElement.text.strip().lower()
        assert textok in textreal,f"Expected {textok} and found: {textreal}"
      
    def test_button(self, element, buttonText):
        button = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, element)))
        self.repeatSeach(button)
        assert button, f"Button {buttonText} not found"
    
    def repeatSeach(self, element):
            for i in range(20):
                try:
                        assert element.is_displayed()
                        break
                except:
                        time.sleep(1)
                        pass  

    def find_element_presence(self, locator, element=None, timeout=0):
        ret = None
        if element != None:
            found_element = element.find_element(*locator)
            ret = self.wait_for_element_to_be_clickable(found_element)
        else:
            if timeout:
                custom_explicit_wait = WebDriverWait(
                    driver=self.browser,
                    timeout=timeout,
                    poll_frequency=2.0,
                    ignored_exceptions={
                    })
                ret = custom_explicit_wait.until(EC.element_to_be_clickable(locator))
            else:
                ret = self.explicit_wait.until(EC.element_to_be_clickable(locator))
        return ret

    def wait_for_element_to_be_clickable(self, element):
        return self.explicit_wait.until(EC.element_to_be_clickable(element))

    def force_click_on(self, locator, timeout=15):
         start = time.time()
         cont = True
         while cont:
            try:
                elem = self.find_element_presence(locator=locator)
                elem.click()
                cont = False
            except Exception as e:
                print(e)
                if (time.time()-start)>= timeout:
                    cont = False 
                    raise 
            time.sleep(1)

    def click_until_second_element_is_enabled(self, clickable_element_locator, element_to_wait_locator, timeout=15):
        self.find_element_presence(clickable_element_locator)
        cont = True 
        start = time.time()        
        while cont: 
            try: 
                my_btn = self.browser.find_element(*clickable_element_locator)
                my_btn.click()
            except:
                pass
            try:
                second_element = self.browser.find_element(*element_to_wait_locator)
                ena = second_element.is_enabled()  
                if ena:
                    cont = False 
            except:
                pass
            if time.time() - start >= timeout:
                cont = False             
            time.sleep(0.5)

    def force_select_option(self, locator, option, timeout=15):
         start = time.time()
         cont = True
         while cont:
            try:
                elem = self.find_element_presence(locator=locator)
                select = Select(elem)
                select.select_by_value(option)
                elem.is_selected()
                cont = False
            except Exception as e:
                print(e)
                if (start - time.time())>= timeout:
                    cont = False 
                    raise 
            time.sleep(1)    


    def test_element_presence_repeat(self, locator, max_attempts=3, timeout=10):
        """
        Check element presence with retries
        Args:
            locator: tuple of By and selector
            max_attempts: maximum number of retry attempts
            timeout: seconds to wait for element
        Returns:
            bool: True if element found, False otherwise
        """
        attempt = 0
        while attempt < max_attempts:
            try:
                print(f"Checking for element {locator} (Attempt {attempt + 1}/{max_attempts})")
                
                # Wait for element presence
                element = WebDriverWait(self.browser, timeout).until(
                    EC.presence_of_element_located(locator)
                )
                
                # Wait for element to be visible
                element = WebDriverWait(self.browser, timeout).until(
                    EC.visibility_of_element_located(locator)
                )
                
                if element.is_displayed():
                    print(f"Element {locator} found and visible")
                    return True
                    
            except TimeoutException:
                print(f"Timeout waiting for element {locator}")
            except Exception as e:
                print(f"Error checking element {locator}: {str(e)}")
                
            attempt += 1
            if attempt < max_attempts:
                print(f"Retrying... ({attempt + 1}/{max_attempts})")
                time.sleep(2)  # Short wait between retries
                
        # If we get here, element wasn't found after all attempts
        print(f"Element {locator} not found after {max_attempts} attempts")
        
        return False
        
    def write1(self, locator, text):
        
        try:
            field = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((locator)))
            self.repeatSeach(field)
            field.send_keys([Keys.BACKSPACE] * 200)
            #field.clear()
            field.send_keys(text)
        except Exception as e:
            print(f"Error writing to element: {e}")
            raise
     
    def switch_to_new_tab(self):
        self.browser.switch_to.window(self.browser.window_handles[-1])    
    
    def switch_back_to_previous_tab(self):
        self.browser.switch_to.window(self.browser.window_handles[-2])
        
    def close_tab(self):
        self.browser.close()
        
    def clickOn1(self, locator):
        element = WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((locator)))
        self.repeatSeach(element)
        element.click() 
    
    def test_element_presence(self, element):
        Element =   WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, element)))
        self.repeatSeach(Element)               
        assert Element.is_displayed(), "Element is not displayed"
        
    def type(self, element, text):
        
        Field =  WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, element)))
        self.repeatSeach(Field)
        Field.send_keys(text)         
    
    def pressMenuBtn(self, btnElement):
        
        menuBtn = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, btnElement)))
        self.repeatSeach(menuBtn)
        menuBtn.click()
        
    def selectFromDropDown(self, locator_type, locator_value, option):
        
         x = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((locator_type, locator_value)))
         self.repeatSeach(x)
         drop = Select (x)
         drop.select_by_visible_text(option) 
        
    def select_from_dd_by_value(self, locator, value):
        
        element = WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((locator)))
        drop = Select(element)
        drop.select_by_value(value) 
        
        
    def select_from_dd_by_text(self, locator, text):
        """
        Select option from custom dropdown by visible text
        Args:
            locator: tuple of (By.XXX, 'selector')
            text: text to select from dropdown
        """
        try:
            # Click to open dropdown
            self.clickOn(locator)
            time.sleep(2)  # Increased wait time
            
            # Try different option locators
            option_locators = [
                f"//li[text()='{text}']",  # Exact match
                f"//li[contains(text(), '{text}')]",  # Contains text
                f"//li[normalize-space()='{text}']",  # Normalized text
                f"//div[contains(@class, 'dropdown')]//li[contains(text(), '{text}')]"  # More specific path
            ]
            
            for xpath in option_locators:
                try:
                    option_locator = (By.XPATH, xpath)
                    option = WebDriverWait(self.browser, 5).until(
                        EC.element_to_be_clickable(option_locator)
                    )
                    option.click()
                    print(f"Successfully selected '{text}' using locator: {xpath}")
                    return
                except:
                    continue
                
            raise Exception(f"Could not find option with text: {text}")
            
        except Exception as e:
            print(f"Failed to select '{text}' from dropdown: {str(e)}")
            raise
        
    def select_from_dd_by_index(self, locator, value):
        
        element = WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((locator)))
        drop = Select(element)
        drop.select_by_value(value) 

    def force_click(self, locator):
        """
        Force click an element using JavaScript
        Args:
            locator: tuple of By and selector
        """
        try:
            print(f"Attempting force click on element: {locator}")
            element = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located(locator)
            )
            self.browser.execute_script("arguments[0].click();", element)
            print("Force click successful")
            return True
            
        except Exception as e:
            print(f"Force click failed: {str(e)}")
            
            return False 

    def clickOn(self, locator):
        """
        Click on element with better error handling and multiple click strategies
        Args:
            locator: tuple of (By.XXX, 'selector')
        """
        started = time.time()
        cont = True
        last_exception = None
        
        while cont:
            try:
                time.sleep(1)
                # Wait for element to be present
                element = WebDriverWait(self.browser, 20).until(
                    EC.presence_of_element_located(locator)
                )
                element = WebDriverWait(self.browser, 20).until(
                    EC.element_to_be_clickable(locator)
                )
                # Try to click the element
                element.click()
                cont = False
                
            except Exception as e:
                last_exception = e
                try:
                    # Wait for loading overlay to disappear
                    WebDriverWait(self.browser, 10).until(
                        EC.invisibility_of_element_located((By.CLASS_NAME, "loading-overlay"))
                    )
                except:
                    pass
                    
                if time.time() - started >= 15:
                    cont = False
                    print(f"Failed to click element {locator}")
                    if last_exception:
                        raise last_exception
                    else:
                        raise Exception(f"Failed to click element {locator}")

    def OLD_clickOn(self, locator):
        # DEPRECATED
        """
        Click on element with better error handling and multiple click strategies
        Args:
            locator: tuple of (By.XXX, 'selector')
        """
        try:
            # Wait for element to be present
            element = WebDriverWait(self.browser, 20).until(
                EC.presence_of_element_located(locator)
            )
            
            # Wait for loading overlay to disappear (adjust selector as needed)
            try:
                WebDriverWait(self.browser, 10).until(
                    EC.invisibility_of_element_located((By.CLASS_NAME, "loading-overlay"))
                )
            except:
                pass  # No overlay found or different class name
                
            # Wait for element to be clickable
            element = WebDriverWait(self.browser, 20).until(
                EC.element_to_be_clickable(locator)
            )
            
            # Keep the repeatSearch
            self.repeatSeach(element)
            
            # Scroll element into view and ensure no overlays
            self.browser.execute_script("""
                arguments[0].scrollIntoView(true);
                // Remove any modal backdrops
                var overlays = document.getElementsByClassName('modal-backdrop');
                for(var i=0; i<overlays.length; i++) {
                    overlays[i].remove();
                }
            """, element)
            time.sleep(1)  # Small pause after scroll
            
            # Try regular click first
            try:
                element.click()
            except (ElementClickInterceptedException, Exception):
                # If regular click fails, try JavaScript click with overlay removal
                self.browser.execute_script("""
                    // Remove any remaining overlays
                    var overlays = document.getElementsByClassName('modal-backdrop');
                    for(var i=0; i<overlays.length; i++) {
                        overlays[i].remove();
                    }
                    arguments[0].click();
                """, element)
                
        except Exception as e:
            print(f"Failed to click element {locator}: {str(e)}")
            raise
        
        
    def select_from_dropdown(self, locator, option, select_by='text'):
        """
        Generic dropdown selection method with multiple selection strategies
        Args:
            locator: tuple of (By.XXX, 'selector')
            option: value/text/index to select
            select_by: strategy to use ('text', 'value', or 'index')
        """
        try:
            # Convert option to string if selecting by value
            if select_by == 'value':
                option = str(option)
            
            # Start timer for timeout
            start = time.time()
            cont = True
            
            while cont:
                try:
                    # Wait for element and create Select object
                    element = WebDriverWait(self.browser, 20).until(
                        EC.presence_of_element_located(locator)
                    )
                    self.repeatSeach(element)
                    
                    # Create dropdown handler
                    dropdown = Select(element)
                    
                    # Select based on strategy
                    if select_by == 'text':
                        dropdown.select_by_visible_text(option)
                    elif select_by == 'value':
                        dropdown.select_by_value(option)
                    elif select_by == 'index':
                        dropdown.select_by_index(int(option))
                    else:
                        raise ValueError(f"Invalid selection strategy: {select_by}")
                    
                    # Verify selection was made
                    selected_option = dropdown.first_selected_option
                    if selected_option.is_displayed():
                        print(f"Successfully selected: {option}")
                        cont = False
                        
                except Exception as e:
                    # Wait for any loading overlays to disappear
                    try:
                        WebDriverWait(self.browser, 10).until(
                            EC.invisibility_of_element_located((By.CLASS_NAME, "loading-overlay"))
                        )
                    except:
                        pass
                    
                    # Check timeout
                    if time.time() - start >= 15:
                        print(f"Failed to select {option} from dropdown: {str(e)}")
                        cont = False
                        raise
                    
                    time.sleep(1)  # Small pause before retry
                    
        except Exception as e:
            print(f"Error selecting from dropdown: {str(e)}")
            raise
    
    
    def write(self, locator, text):
        """
        Write text to an input field with improved clearing
        Args:
            locator: tuple of (By.XXX, 'selector')
            text: text to write in the field
        """
        try:
            start = time.time()
            cont = True
            
            while cont and (time.time() - start < 15):  # 15 second timeout
                try:
                    # Wait for element to be present and interactable
                    field = WebDriverWait(self.browser, 10).until(
                        EC.presence_of_element_located(locator)
                    )
                    field = WebDriverWait(self.browser, 10).until(
                        EC.element_to_be_clickable(locator)
                    )
                    self.repeatSeach(field)
                    
                    # Scroll element into view
                    self.browser.execute_script("arguments[0].scrollIntoView(true);", field)
                    time.sleep(1)
                    
                    # Click to ensure focus
                    field.click()
                    
                    # Clear using multiple methods
                    field.clear()  # Standard clear
                    
                    # Select all text
                    if platform.system() == 'Darwin':  # macOS
                        field.send_keys(Keys.COMMAND + 'a')
                    else:  # Windows/Linux
                        field.send_keys(Keys.CONTROL + 'a')
                    field.send_keys(Keys.DELETE)
                    
                    # Additional backspace clearing
                    current_value = field.get_attribute('value')
                    if current_value:
                        field.send_keys([Keys.BACKSPACE] * len(current_value))
                    
                    # Clear using JavaScript
                    self.browser.execute_script("arguments[0].value = '';", field)
                    
                    # Write new text
                    field.send_keys(text)
                    time.sleep(0.5)  # Short wait for text to settle
                    
                    # Verify text was written correctly
                    actual_text = field.get_attribute('value')
                    if actual_text == text:
                        print(f"Successfully wrote: {text}")
                        cont = False
                    else:
                        print(f"Text verification failed. Expected: {text}, Got: {actual_text}")
                        raise ValueError("Text verification failed")
                        
                except Exception as e:
                    if time.time() - start >= 15:
                        print(f"Failed to write text after multiple attempts: {str(e)}")
                        raise
                    time.sleep(1)  # Wait before retry
                    
        except Exception as e:
            print(f"Error writing to element {locator}: {str(e)}")
            raise


    def select_from_custom_dropdown(self, locator, text):
        """
         Select option from custom dropdown by visible text
         Args:
        locator: tuple of (By.XXX, 'selector')
        text: text to select from dropdown
        """         
        try:
            # Click to open dropdown
           # self.clickOn(locator)
            time.sleep(2)
            
            # Create option locator
            option_locator = (By.XPATH, f"//*[contains(text(), '{text}')]")
            
            # Wait for option and click
            option = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable(option_locator)
            )
            option.click()
            print(f"Successfully selected '{text}'")
            
        except Exception as e:
            print(f"Failed to select '{text}' from dropdown: {str(e)}")
            raise

    def wait_until_body_loaded(self, timeout=20):
        """
        Wait for page body to fully load by checking document.readyState
        Args:
            timeout: int - seconds to wait (default 20)
        Returns:
            bool: True if page loads successfully, False if timeout
        """
        try:
            # Wait for document ready state to be complete
            WebDriverWait(self.browser, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            # Wait for body to be present and visible
            WebDriverWait(self.browser, timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Optional: wait for any loading spinners to disappear
            try:
                WebDriverWait(self.browser, 5).until_not(
                    EC.presence_of_element_located((By.CLASS_NAME, "loading-spinner"))
                )
            except:
                # If no spinner found, that's okay
                pass
            
            print("Page body loaded successfully")
            return True
            
        except Exception as e:
            print(f"Error waiting for page body to load: {str(e)}")
            return False

    def click_with_fallback(self, *locators):
        """Try clicking element with multiple locators in sequence"""
        for locator in locators:
            try:
                self.clickOn(locator)
                return
            except:
                continue
        raise Exception("Failed to click element with any provided locator")

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
#from pytest_testconfig import config
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import os
import time 
import platform
from selenium.common.exceptions import ElementClickInterceptedException


                          

class BasePage():
    
    def __init__(self, browser):
        self.browser = browser   
        self.explicit_wait = WebDriverWait(
            timeout=15,
            driver=self.browser,
            poll_frequency=1.0,
            ignored_exceptions={
            },
        )
    
    def scrollDown(self):
        html = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'html')))
        self.repeatSeach(html)
        html.send_keys([Keys.END])
        
  
        
    def test_text(self, element, textok):
        textElement = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, element)))
        self.repeatSeach(textElement)
        textreal = textElement.text.strip().lower()
        assert textok in textreal,f"Expected {textok} and found: {textreal}"
      
    def test_button(self, element, buttonText):
        button = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, element)))
        self.repeatSeach(button)
        assert button, f"Button {buttonText} not found"
    
    def repeatSeach(self, element):
            for i in range(20):
                try:
                        assert element.is_displayed()
                        break
                except:
                        time.sleep(1)
                        pass  

    def find_element_presence(self, locator, element=None, timeout=0):
        ret = None
        if element != None:
            found_element = element.find_element(*locator)
            ret = self.wait_for_element_to_be_clickable(found_element)
        else:
            if timeout:
                custom_explicit_wait = WebDriverWait(
                    driver=self.browser,
                    timeout=timeout,
                    poll_frequency=2.0,
                    ignored_exceptions={
                    })
                ret = custom_explicit_wait.until(EC.element_to_be_clickable(locator))
            else:
                ret = self.explicit_wait.until(EC.element_to_be_clickable(locator))
        return ret

    def wait_for_element_to_be_clickable(self, element):
        return self.explicit_wait.until(EC.element_to_be_clickable(element))

    def force_click_on(self, locator, timeout=15):
         start = time.time()
         cont = True
         while cont:
            try:
                elem = self.find_element_presence(locator=locator)
                elem.click()
                cont = False
            except Exception as e:
                print(e)
                if (time.time()-start)>= timeout:
                    cont = False 
                    raise 
            time.sleep(1)

    def click_until_second_element_is_enabled(self, clickable_element_locator, element_to_wait_locator, timeout=15):
        self.find_element_presence(clickable_element_locator)
        cont = True 
        start = time.time()        
        while cont: 
            try: 
                my_btn = self.browser.find_element(*clickable_element_locator)
                my_btn.click()
            except:
                pass
            try:
                second_element = self.browser.find_element(*element_to_wait_locator)
                ena = second_element.is_enabled()  
                if ena:
                    cont = False 
            except:
                pass
            if time.time() - start >= timeout:
                cont = False             
            time.sleep(0.5)

    def force_select_option(self, locator, option, timeout=15):
         start = time.time()
         cont = True
         while cont:
            try:
                elem = self.find_element_presence(locator=locator)
                select = Select(elem)
                select.select_by_value(option)
                elem.is_selected()
                cont = False
            except Exception as e:
                print(e)
                if (start - time.time())>= timeout:
                    cont = False 
                    raise 
            time.sleep(1)    


    def test_element_presence_repeat(self, locator, max_attempts=3, timeout=10):
        """
        Check element presence with retries
        Args:
            locator: tuple of By and selector
            max_attempts: maximum number of retry attempts
            timeout: seconds to wait for element
        Returns:
            bool: True if element found, False otherwise
        """
        attempt = 0
        while attempt < max_attempts:
            try:
                print(f"Checking for element {locator} (Attempt {attempt + 1}/{max_attempts})")
                
                # Wait for element presence
                element = WebDriverWait(self.browser, timeout).until(
                    EC.presence_of_element_located(locator)
                )
                
                # Wait for element to be visible
                element = WebDriverWait(self.browser, timeout).until(
                    EC.visibility_of_element_located(locator)
                )
                
                if element.is_displayed():
                    print(f"Element {locator} found and visible")
                    return True
                    
            except TimeoutException:
                print(f"Timeout waiting for element {locator}")
            except Exception as e:
                print(f"Error checking element {locator}: {str(e)}")
                
            attempt += 1
            if attempt < max_attempts:
                print(f"Retrying... ({attempt + 1}/{max_attempts})")
                time.sleep(2)  # Short wait between retries
                
        # If we get here, element wasn't found after all attempts
        print(f"Element {locator} not found after {max_attempts} attempts")
        
        return False
        
    def write1(self, locator, text):
        
        try:
            field = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((locator)))
            self.repeatSeach(field)
            field.send_keys([Keys.BACKSPACE] * 200)
            #field.clear()
            field.send_keys(text)
        except Exception as e:
            print(f"Error writing to element: {e}")
            raise
     
    def switch_to_new_tab(self):
        self.browser.switch_to.window(self.browser.window_handles[-1])    
    
    def switch_back_to_previous_tab(self):
        self.browser.switch_to.window(self.browser.window_handles[-2])
        
    def close_tab(self):
        self.browser.close()
        
    def clickOn1(self, locator):
        element = WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((locator)))
        self.repeatSeach(element)
        element.click() 
    
    def test_element_presence(self, element):
        Element =   WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, element)))
        self.repeatSeach(Element)               
        assert Element.is_displayed(), "Element is not displayed"
        
    def type(self, element, text):
        
        Field =  WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, element)))
        self.repeatSeach(Field)
        Field.send_keys(text)         
    
    def pressMenuBtn(self, btnElement):
        
        menuBtn = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, btnElement)))
        self.repeatSeach(menuBtn)
        menuBtn.click()
        
    def selectFromDropDown(self, locator_type, locator_value, option):
        
         x = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((locator_type, locator_value)))
         self.repeatSeach(x)
         drop = Select (x)
         drop.select_by_visible_text(option) 
        
    def select_from_dd_by_value(self, locator, value):
        
        element = WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((locator)))
        drop = Select(element)
        drop.select_by_value(value) 
        
        
    def select_from_dd_by_text(self, locator, text):
        """
        Select option from custom dropdown by visible text
        Args:
            locator: tuple of (By.XXX, 'selector')
            text: text to select from dropdown
        """
        try:
            # Click to open dropdown
            self.clickOn(locator)
            time.sleep(2)  # Increased wait time
            
            # Try different option locators
            option_locators = [
                f"//li[text()='{text}']",  # Exact match
                f"//li[contains(text(), '{text}')]",  # Contains text
                f"//li[normalize-space()='{text}']",  # Normalized text
                f"//div[contains(@class, 'dropdown')]//li[contains(text(), '{text}')]"  # More specific path
            ]
            
            for xpath in option_locators:
                try:
                    option_locator = (By.XPATH, xpath)
                    option = WebDriverWait(self.browser, 5).until(
                        EC.element_to_be_clickable(option_locator)
                    )
                    option.click()
                    print(f"Successfully selected '{text}' using locator: {xpath}")
                    return
                except:
                    continue
                
            raise Exception(f"Could not find option with text: {text}")
            
        except Exception as e:
            print(f"Failed to select '{text}' from dropdown: {str(e)}")
            raise
        
    def select_from_dd_by_index(self, locator, value):
        
        element = WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((locator)))
        drop = Select(element)
        drop.select_by_value(value) 

    def force_click(self, locator):
        """
        Force click an element using JavaScript
        Args:
            locator: tuple of By and selector
        """
        try:
            print(f"Attempting force click on element: {locator}")
            element = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located(locator)
            )
            self.browser.execute_script("arguments[0].click();", element)
            print("Force click successful")
            return True
            
        except Exception as e:
            print(f"Force click failed: {str(e)}")
            
            return False 

    def clickOn(self, locator):
        """
        Click on element with better error handling and multiple click strategies
        Args:
            locator: tuple of (By.XXX, 'selector')
        """
        started = time.time()
        cont = True
        last_exception = None
        
        while cont:
            try:
                time.sleep(1)
                # Wait for element to be present
                element = WebDriverWait(self.browser, 20).until(
                    EC.presence_of_element_located(locator)
                )
                element = WebDriverWait(self.browser, 20).until(
                    EC.element_to_be_clickable(locator)
                )
                # Try to click the element
                element.click()
                cont = False
                
            except Exception as e:
                last_exception = e
                try:
                    # Wait for loading overlay to disappear
                    WebDriverWait(self.browser, 10).until(
                        EC.invisibility_of_element_located((By.CLASS_NAME, "loading-overlay"))
                    )
                except:
                    pass
                    
                if time.time() - started >= 15:
                    cont = False
                    print(f"Failed to click element {locator}")
                    if last_exception:
                        raise last_exception
                    else:
                        raise Exception(f"Failed to click element {locator}")

    def OLD_clickOn(self, locator):
        # DEPRECATED
        """
        Click on element with better error handling and multiple click strategies
        Args:
            locator: tuple of (By.XXX, 'selector')
        """
        try:
            # Wait for element to be present
            element = WebDriverWait(self.browser, 20).until(
                EC.presence_of_element_located(locator)
            )
            
            # Wait for loading overlay to disappear (adjust selector as needed)
            try:
                WebDriverWait(self.browser, 10).until(
                    EC.invisibility_of_element_located((By.CLASS_NAME, "loading-overlay"))
                )
            except:
                pass  # No overlay found or different class name
                
            # Wait for element to be clickable
            element = WebDriverWait(self.browser, 20).until(
                EC.element_to_be_clickable(locator)
            )
            
            # Keep the repeatSearch
            self.repeatSeach(element)
            
            # Scroll element into view and ensure no overlays
            self.browser.execute_script("""
                arguments[0].scrollIntoView(true);
                // Remove any modal backdrops
                var overlays = document.getElementsByClassName('modal-backdrop');
                for(var i=0; i<overlays.length; i++) {
                    overlays[i].remove();
                }
            """, element)
            time.sleep(1)  # Small pause after scroll
            
            # Try regular click first
            try:
                element.click()
            except (ElementClickInterceptedException, Exception):
                # If regular click fails, try JavaScript click with overlay removal
                self.browser.execute_script("""
                    // Remove any remaining overlays
                    var overlays = document.getElementsByClassName('modal-backdrop');
                    for(var i=0; i<overlays.length; i++) {
                        overlays[i].remove();
                    }
                    arguments[0].click();
                """, element)
                
        except Exception as e:
            print(f"Failed to click element {locator}: {str(e)}")
            raise
        
        
    def select_from_dropdown(self, locator, option, select_by='text'):
        """
        Generic dropdown selection method with multiple selection strategies
        Args:
            locator: tuple of (By.XXX, 'selector')
            option: value/text/index to select
            select_by: strategy to use ('text', 'value', or 'index')
        """
        try:
            # Convert option to string if selecting by value
            if select_by == 'value':
                option = str(option)
            
            # Start timer for timeout
            start = time.time()
            cont = True
            
            while cont:
                try:
                    # Wait for element and create Select object
                    element = WebDriverWait(self.browser, 20).until(
                        EC.presence_of_element_located(locator)
                    )
                    self.repeatSeach(element)
                    
                    # Create dropdown handler
                    dropdown = Select(element)
                    
                    # Select based on strategy
                    if select_by == 'text':
                        dropdown.select_by_visible_text(option)
                    elif select_by == 'value':
                        dropdown.select_by_value(option)
                    elif select_by == 'index':
                        dropdown.select_by_index(int(option))
                    else:
                        raise ValueError(f"Invalid selection strategy: {select_by}")
                    
                    # Verify selection was made
                    selected_option = dropdown.first_selected_option
                    if selected_option.is_displayed():
                        print(f"Successfully selected: {option}")
                        cont = False
                        
                except Exception as e:
                    # Wait for any loading overlays to disappear
                    try:
                        WebDriverWait(self.browser, 10).until(
                            EC.invisibility_of_element_located((By.CLASS_NAME, "loading-overlay"))
                        )
                    except:
                        pass
                    
                    # Check timeout
                    if time.time() - start >= 15:
                        print(f"Failed to select {option} from dropdown: {str(e)}")
                        cont = False
                        raise
                    
                    time.sleep(1)  # Small pause before retry
                    
        except Exception as e:
            print(f"Error selecting from dropdown: {str(e)}")
            raise
    
    
    def write(self, locator, text):
        """
        Write text to an input field with improved clearing
        Args:
            locator: tuple of (By.XXX, 'selector')
            text: text to write in the field
        """
        try:
            start = time.time()
            cont = True
            
            while cont and (time.time() - start < 15):  # 15 second timeout
                try:
                    # Wait for element to be present and interactable
                    field = WebDriverWait(self.browser, 10).until(
                        EC.presence_of_element_located(locator)
                    )
                    field = WebDriverWait(self.browser, 10).until(
                        EC.element_to_be_clickable(locator)
                    )
                    self.repeatSeach(field)
                    
                    # Scroll element into view
                    self.browser.execute_script("arguments[0].scrollIntoView(true);", field)
                    time.sleep(1)
                    
                    # Click to ensure focus
                    field.click()
                    
                    # Clear using multiple methods
                    field.clear()  # Standard clear
                    
                    # Select all text
                    if platform.system() == 'Darwin':  # macOS
                        field.send_keys(Keys.COMMAND + 'a')
                    else:  # Windows/Linux
                        field.send_keys(Keys.CONTROL + 'a')
                    field.send_keys(Keys.DELETE)
                    
                    # Additional backspace clearing
                    current_value = field.get_attribute('value')
                    if current_value:
                        field.send_keys([Keys.BACKSPACE] * len(current_value))
                    
                    # Clear using JavaScript
                    self.browser.execute_script("arguments[0].value = '';", field)
                    
                    # Write new text
                    field.send_keys(text)
                    time.sleep(0.5)  # Short wait for text to settle
                    
                    # Verify text was written correctly
                    actual_text = field.get_attribute('value')
                    if actual_text == text:
                        print(f"Successfully wrote: {text}")
                        cont = False
                    else:
                        print(f"Text verification failed. Expected: {text}, Got: {actual_text}")
                        raise ValueError("Text verification failed")
                        
                except Exception as e:
                    if time.time() - start >= 15:
                        print(f"Failed to write text after multiple attempts: {str(e)}")
                        raise
                    time.sleep(1)  # Wait before retry
                    
        except Exception as e:
            print(f"Error writing to element {locator}: {str(e)}")
            raise


    def select_from_custom_dropdown(self, locator, text):
        """
         Select option from custom dropdown by visible text
         Args:
        locator: tuple of (By.XXX, 'selector')
        text: text to select from dropdown
        """         
        try:
            # Click to open dropdown
           # self.clickOn(locator)
            time.sleep(2)
            
            # Create option locator
            option_locator = (By.XPATH, f"//*[contains(text(), '{text}')]")
            
            # Wait for option and click
            option = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable(option_locator)
            )
            option.click()
            print(f"Successfully selected '{text}'")
            
        except Exception as e:
            print(f"Failed to select '{text}' from dropdown: {str(e)}")
            raise

    def wait_until_body_loaded(self, timeout=20):
        """
        Wait for page body to fully load by checking document.readyState
        Args:
            timeout: int - seconds to wait (default 20)
        Returns:
            bool: True if page loads successfully, False if timeout
        """
        try:
            # Wait for document ready state to be complete
            WebDriverWait(self.browser, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            # Wait for body to be present and visible
            WebDriverWait(self.browser, timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Optional: wait for any loading spinners to disappear
            try:
                WebDriverWait(self.browser, 5).until_not(
                    EC.presence_of_element_located((By.CLASS_NAME, "loading-spinner"))
                )
            except:
                # If no spinner found, that's okay
                pass
            
            print("Page body loaded successfully")
            return True
            
        except Exception as e:
            print(f"Error waiting for page body to load: {str(e)}")
            return False

    def click_with_fallback(self, *locators):
        """Try clicking element with multiple locators in sequence"""
        for locator in locators:
            try:
                self.clickOn(locator)
                return
            except:
                continue
        raise Exception("Failed to click element with any provided locator")
