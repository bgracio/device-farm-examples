import os
import unittest
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestClass(unittest.TestCase):

    WEB_DRIVER_DEFAULT_TIMEOUT = 30

    XPATH_USERNAME = '//input[@id="Input_UsernameVal"]'
    XPATH_PASSWORD = '//input[@id="Input_PasswordVal"]'
    XPATH_LOGIN_BUTTON = '//button[@id="LoginBtn"]'
    XPATH_BORAT_IMAGE = '//img[@id="BoratImg"]'

    def setUp(self):
        desired_caps = {}

        # Uncomment if your want top test in an Android device locally
        # desired_caps['platformName'] = 'Android'
        # desired_caps['deviceName'] = 'aPhone'
        # desired_caps['appPackage'] = 'com.outsystems.rd.SampleApp'
        # desired_caps['appActivity'] = ".MainActivity"

        # Uncomment if your want top test in a iOS device locally
        # desired_caps['platformName'] = 'iOS'
        # desired_caps['platformVersion'] = '11.4'
        # desired_caps['deviceName'] = 'iPhone X'
        # desired_caps['bundleId'] = 'com.outsystems.rd.SampleApp'
        # desired_caps['automationName'] = 'XCUITest'

        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
        print("Desired capabilities: " + str(self.driver.desired_capabilities))

    def test_login(self):
        self.switch_to_webview()

        # Wait to make sure that the login button is visible
        wait = WebDriverWait(self.driver, self.WEB_DRIVER_DEFAULT_TIMEOUT)
        wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, self.XPATH_LOGIN_BUTTON)
            )
        )

        # We are using xpath to locate the elements but we can also use id, name, etc..
        # Check this: https://selenium-python.readthedocs.io/locating-elements.html
        username_field = self.driver.find_element_by_xpath(self.XPATH_USERNAME)
        password_field = self.driver.find_element_by_xpath(self.XPATH_PASSWORD)
        login_button = self.driver.find_element_by_xpath(self.XPATH_LOGIN_BUTTON)

        username_field.click()
        username_field.send_keys("bpc")

        password_field.click()
        password_field.send_keys("mobilizado")

        login_button.click()

        # Wait to make sure that the borat image is visible
        wait = WebDriverWait(self.driver, self.WEB_DRIVER_DEFAULT_TIMEOUT)
        wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, self.XPATH_BORAT_IMAGE)
            )
        )

        self.take_screenshot("Borat.png")

        borat_image = self.driver.find_element_by_xpath(self.XPATH_BORAT_IMAGE)
        self.assertIsNotNone(borat_image, "Missing image")

    def tearDown(self):
        self.driver.quit()
    
    # Returns the first context name who's name starts with WEBVIEW
    def get_webview_context(self, driver):
        print("Available contexts:" + str(driver.contexts))
        for ctx in driver.contexts:
            if ctx.startswith('WEBVIEW'):
                return ctx
    
    # Switch to the webview context
    def switch_to_webview(self):
        webview_context = self.get_webview_context(self.driver)
        
        if webview_context is None:
            raise ValueError("Failed to retrieve a webview context")
        
        print("Webview context:" + webview_context)
        if webview_context != self.driver.context:
            self.driver.switch_to.context(webview_context)
            print("Switched to context:" + webview_context)
    
    # Take a screenshot
    def take_screenshot(self, screenshot_name):
        current_context = self.driver.context
        self.driver.switch_to.context("NATIVE_APP")
        # add SCREENSHOT_PATH to your enviroment to set the destination of your screenshots 
        path = os.getenv('SCREENSHOT_PATH', '')
        self.driver.save_screenshot(path + "/" + screenshot_name)
        self.driver.switch_to.context(current_context)

if __name__ == '__main__':
    unittest.main()