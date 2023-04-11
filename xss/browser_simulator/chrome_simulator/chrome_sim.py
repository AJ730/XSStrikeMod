from threading import Event

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from xss.browser_simulator.payload_injector import PayloadInjecter


class ChromeSimulator(PayloadInjecter):

	def __init__(self, d="/home/kali/Documents/xss/xss/browser_simulator/chrome_simulator/chromedriver", headless=False):
		"""
		Initialize chrome Driver
		@param d: full path of chrome driver
		@type d: string
		"""
		chrome_options = Options()
		chrome_options.add_argument("ignore-certificate-error")
		chrome_options.add_argument("ignore-ssl-errors")
		chrome_options.headless = headless
		chrome_options.add_experimental_option('prefs', {'profile.default_content_setting_values.cookies': 2})
		chrome_options.add_argument("--lang=en-GB")


		caps = webdriver.DesiredCapabilities().CHROME
		caps['acceptInsecureCerts'] = True
		caps['acceptSslCerts'] = True

		self.driver = webdriver.Chrome(d, options=chrome_options, desired_capabilities=caps)
		self.w = WebDriverWait(self.driver, 10)

	def get_driver(self):
		"""
		Return current driver
		@return: driver
		@rtype: driver
		"""
		return self.driver

	def get_browser(self):
		"""
		Get google
		@return: google search
		@rtype: void
		"""
		self.driver.maximize_window()
		self.driver.get("https://www.google.com/")

	def accept_license(self):
		"""
		Accept google license
		@return: void
		@rtype: void
		"""
		agree = self.driver.find_element(By.ID, "L2AGLb")
		agree.click()
		print("Accepted License")

	def search(self, query):
		"""
		Search google
		@param query: query
		@type query: string
		@return: searched step
		@rtype: void
		"""
		self.submit_payload_by_name("q", query)

	def get_current_address_url(self):
		"""
		Get current webpage url
		@return: url
		@rtype: string
		"""
		return self.driver.current_url

	def halt(self, seconds):
		"""
		Stop current thread in seconds
		@param seconds: time
		@type seconds: int
		@return: halt execution
		@rtype: void
		"""
		Event().wait(seconds)

	def kill_chrome(self):
		"""
		Close Chrome Browser
		@return: stopped Chrome
		@rtype: stopped Chrome
		"""
		self.driver.quit()
