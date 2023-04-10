from abc import ABC, abstractmethod, ABCMeta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

import requests
from selenium.common import UnexpectedAlertPresentException, TimeoutException

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver


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

	def is_text_blocked(self, text):
		if "blocked" in text:
			return True
		elif "blokkert" in text:
			return True
		return False

	def checkBlocked(self, query):
		try:
			status = requests.get(query, timeout=5)
		except:
			return "Blocked"

		if status.status_code == 403 or status.status_code == 405:
			return "Blocked"

		if str(status.status_code).startswith("5"):
			return "Server Error"

		if self.is_text_blocked(status.text):
			return "Maybe Blocked"

	def accept_cookies(self):
		buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Allow')]")  # Try Finding Cookies
		buttons.extend(
			self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Accepteren')]"))  # Try Finding Cookies
		buttons.extend(
			self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Accept')]"))  # Try Finding Cookies
		for button in buttons:
			button.click()

	def validate_get_attack(self, query):
		"""
        Validates if attack succeeded
        @param query: getQuery
        @type query: query
        @return: true or fulse
        @rtype: boolean
        """

		try:
			blocked = self.checkBlocked(query)
			if blocked is not None:
				return blocked

			self.accept_cookies()

			self.submit_payload_by_query(query)

			blocked = self.checkBlocked(query)
			if blocked is not None:
				return blocked

			pop_up = self.wait_for_alert()
			if pop_up is True:
				return "Succeeded"
			if pop_up == "unknown response":
				return "Unknown Response"

			return "No Change"

		except UnexpectedAlertPresentException:
			return "Succeeded"

		except Exception as e:
			print(e, flush=True)
			return "Unknown Response"

	def hover_on_all_reflections(self):

		self_injected_d3v_tags = self.driver.find_elements(By.TAG_NAME, 'd3v')
		list_links_made = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'v3dm0s')]")
		self_injected_details_tags = self.driver.find_elements(By.TAG_NAME, 'details')
		action = webdriver.common.action_chains.ActionChains(self.driver)

		for i in self_injected_d3v_tags:
			try:
				action.move_to_element_with_offset(i, 5, 5)
				action.perform()

				WebDriverWait(self.driver, 1).until(EC.alert_is_present())
				return True

			except UnexpectedAlertPresentException:
				return True

			except Exception:
				continue

		for i in list_links_made:
			try:
				action.move_to_element_with_offset(i, 5, 5)
				action.perform()

				WebDriverWait(self.driver, 1).until(EC.alert_is_present())
				return True

			except UnexpectedAlertPresentException:
				return True

			except Exception:
				continue

		for i in self_injected_details_tags:
			try:
				action.move_to_element_with_offset(i, 5, 5)
				action.click()
				action.perform()

				WebDriverWait(self.driver, 1).until(EC.alert_is_present())
				return True


			except UnexpectedAlertPresentException:
				return True

			except:
				continue

		return False

	def exists(self, element):
		"""
        Checks if an element exists in webpage
        @return: boolean
        @rtype: true or false
        """

		try:
			self.driver.find_element(By.XPATH, element).is_displayed()
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
			if self.hover_on_all_reflections():
				return True
			return False
		except Exception as e:
			return "unknown response"
