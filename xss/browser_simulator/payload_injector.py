from abc import ABC, abstractmethod, ABCMeta
from selenium.webdriver.common.by import By


class PayloadInjecter(ABC):
	__metaclass__ = ABCMeta

	@abstractmethod
	def get_driver(self):
		raise NotImplementedError

	def submit_payload_by_name(self, name, payload):
		element = self.driver.find_element(By.NAME, name)
		element.send_keys(payload)
		element.submit()

	def submit_payload_by_id(self, id, payload):
		element = self.driver.find_element(By.ID, id)
		element.send_keys(payload)
		element.submit()

	def submit_payload_by_Xpath(self, xpath, payload):
		element = self.driver.find_element(By.XPATH, xpath)
		element.send_keys(payload)
		element.submit()

	def submit_payload_by_query(self, query):
		query = self.driver.get(query)
		query.submit()
