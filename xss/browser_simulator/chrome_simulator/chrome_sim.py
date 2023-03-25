from abc import ABC, abstractmethod, ABCMeta
from threading import Event

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from xss.browser_simulator.payload_injector import PayloadInjecter
from selenium.webdriver.chrome.options import Options

class ChromeSimulator(PayloadInjecter):

	def __init__(self, d="/home/kali/Documents/xss/xss/browser_simulator/chrome_simulator/chromedriver"):
		chrome_options = Options()
		chrome_options.add_argument("ignore-certificate-error")
		chrome_options.add_argument("ignore-ssl-errors")

		caps = webdriver.DesiredCapabilities().CHROME
		caps['acceptInsecureCerts'] = True
		caps['acceptSslCerts'] = True

		self.driver = webdriver.Chrome(d,options=chrome_options, desired_capabilities=caps)
		self.w = WebDriverWait(self.driver, 10)

	def get_driver(self):
		return self.driver

	def get_browser(self):
		self.driver.maximize_window()
		self.driver.get("https://www.google.com/")

	def accept_license(self):
		agree = self.driver.find_element(By.ID, "L2AGLb")
		agree.click()
		print("Accepted License")

	def search(self, query):
		self.submit_payload_by_name("q", query)

	def search_address(self, address):
		self.driver.get(address)

	def get_current_address_url(self):
		return self.driver.current_url

	def halt(self, seconds):
		Event().wait(seconds)
