from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def get_firefox_driver():
    options = FirefoxOptions()
    options.headless = True
    service = FirefoxService()
    driver = webdriver.Firefox(service=service, options=options)
    return driver
