from abc import ABC, abstractmethod, ABCMeta
from time import sleep

from selenium.common import UnexpectedAlertPresentException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class PayloadInjecter(ABC):
	__metaclass__ = ABCMeta

	@abstractmethod
	def get_driver(self):
		raise NotImplementedError

	def submit_payload_by_name(self, name, payload):
		"""
        Submit payload by element Name
        @param name: name
        @type payload: query
        @return: go to the query
        @rtype: none
        """

		element = self.driver.find_element(By.NAME, name)
		element.send_keys(payload)
		element.submit()

	def submit_payload_by_id(self, id, payload):
		"""
        Submit payload by  element ID
        @param id: id
        @type payload: payload
        @return: submit payload
        @rtype: none
        """
		element = self.driver.find_element(By.ID, id)
		element.send_keys(payload)
		element.submit()

	def submit_payload_by_Xpath(self, xpath, payload):
		"""
        Submit payload using XPATH
        @param xpath: XPATH
        @type payload: payload
        @return: submit payload
        @rtype: none
        """
		element = self.driver.find_element(By.XPATH, xpath)
		element.send_keys(payload)
		element.submit()

	def submit_payload_by_query(self, query):
		"""
        Submit payload as a query i.e www.google.com?s=payload
        @param query: query
        @type query: query
        @return: go to the query
        @rtype: none
        """
		self.driver.get(query)

	def validate_get_attack(self, query):
		"""
        Validates if attack succeeded
        @param query: getQuery
        @type query: query
        @return: true or fulse
        @rtype: boolean
        """
		try:
			self.submit_payload_by_query(query)
			pop_up = self.wait_for_alert()
			if pop_up:
				return True
		except UnexpectedAlertPresentException:
			return True

	def exists(self, element):
		"""
		Checks if an element exists in webpage
		@return: boolean
		@rtype: true or false
		"""

		try:
			self.driver.find_element(By.NAME, element).is_displayed()
			return True
		except:
			return False

	def wait_for_alert(self):
		"""
        Checks for an alert
        @return: boolean
        @rtype: true or false
        """
		try:
			WebDriverWait(self.driver, 2).until(EC.alert_is_present())
			sleep(2)  # Uncomment this on production code (I just want to see whether alert is present
			alert = self.driver.switch_to.alert
			alert.accept()
			return True

		except TimeoutException:
			if self.exists("deTails"): return True
			return False
