from abc import ABC, abstractmethod, ABCMeta
from selenium.webdriver.common.by import By


class PayloadInjecter(ABC):
	__metaclass__ = ABCMeta

	@abstractmethod
	def get_driver(self):
		raise NotImplementedError

	def submit_payload_by_name(self, name, payload):
		search_bar = self.driver.find_element(By.NAME, name)
		search_bar.send_keys(payload)
		search_bar.submit()

	def submit_payload_by_id(self, id, payload):
		search_bar = self.driver.find_element(By.ID, id)
		search_bar.send_keys(payload)
		search_bar.submit()

	def submit_payload_by_Xpath(self, xpath, payload):
		search_bar = self.driver.find_element(By.XPATH, xpath)
		search_bar.send_keys(payload)
		search_bar.submit()
