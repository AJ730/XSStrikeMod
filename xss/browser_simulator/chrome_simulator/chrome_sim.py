from abc import ABC, abstractmethod, ABCMeta
from threading import Event

from selenium import webdriver
from selenium.webdriver.common.by import By

from xss.browser_simulator.payload_injector import PayloadInjecter


class ChromeSimulator(PayloadInjecter):

	def __init__(self, d='/home/kali/WebstormProjects/XSStrike/xss/browser_simulator/chrome_simulator/chromedriver'):
		self.driver = webdriver.Chrome(d)

	def get_driver(self):
		return self.driver

	def get_browser(self):
		self.driver.maximize_window()
		self.driver.get("https://www.google.com/")

	def accept_license(self):
		agree = self.driver.find_element(By.ID, "L2AGLb")
		agree.click()
		print("Accepted License")

	def halt(self, seconds):
		Event().wait(seconds)
