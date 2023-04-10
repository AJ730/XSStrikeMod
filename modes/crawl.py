import copy
import re
import time

from selenium.webdriver import chrome

import core
from core.checker import checker
from core.config import xsschecker, minEfficiency
from core.config import xsschecker
from core.filterChecker import filterChecker
from core.generator import generator
from core.htmlParser import htmlParser
from core.requester import requester
from core.log import setup_logger
from core.wafDetector import wafDetector
from xss.browser_simulator.chrome_simulator.chrome_sim import *
from xss.reader.LogStorer import LogStorer

logger = setup_logger(__name__)

logStorer = LogStorer()


def crawl(scheme, host, main_url, form, blindXSS, blindPayload, headers, delay, timeout, encoding, headless):
	chrome = ChromeSimulator(headless=headless)
	if form:
		for each in form.values():
			url = each['action']
			correct_url = main_url+ url
			if str(main_url) in str(url):
				correct_url = url
			if url:
				if url.startswith(main_url):
					pass
				elif url.startswith('//') and url[2:].startswith(host):
					url = scheme + '://' + url[2:]
				elif url.startswith('/'):
					url = scheme + '://' + host + url
				elif re.match(r'\w', url[0]):
					url = scheme + '://' + host + '/' + url
				if url not in core.config.globalVariables['checkedForms']:
					core.config.globalVariables['checkedForms'][url] = []
				method = each['method']
				GET = True if method == 'get' else False
				inputs = each['inputs']
				paramData = {}
				for one in inputs:
					paramData[one['name']] = one['value']
					for paramName in paramData.keys():
						if paramName not in core.config.globalVariables['checkedForms'][url]:
							core.config.globalVariables['checkedForms'][url].append(paramName)
							paramsCopy = copy.deepcopy(paramData)
							paramsCopy[paramName] = xsschecker
							response = requester(
								url, paramsCopy, headers, GET, delay, timeout)
							occurences = htmlParser(response, encoding)
							positions = occurences.keys()
							occurences = filterChecker(
								url, paramsCopy, headers, GET, delay, occurences, timeout, encoding)
							vectors = generator(occurences, response.text)

							WAF = wafDetector(
								url, {list(paramName)[0]: xsschecker}, headers, GET, delay, timeout)

							if correct_url[len(correct_url) - 1] == "/":
								correct_url = correct_url[:-1]

							if vectors:
								global_time = time.time()
								for confidence, vects in vectors.items():
									try:
										local_time = time.time()


										for vector in vects:
											efficiencies = checker(url, paramsCopy, headers, GET, delay, vector,
											                       positions, timeout, encoding)

											if not efficiencies:
												for i in range(len(occurences)):
													efficiencies.append(0)
											bestEfficiency = max(efficiencies)
											logger.info(f'current vector: {vector}')

											if bestEfficiency >= 75:
												payload = f"{correct_url}?{paramName}={vector}"
												logVector(chrome, payload, vector, correct_url, paramName, vector, WAF)
												if time.time() - local_time >= 120:
													print("Timedout for parameter")
													break

											if time.time() -global_time  >= 600:
												print("Timedout for site")
												return

										if time.time()  - global_time>= 600:
											print("Timedout for site")
											return

									except IndexError:
										pass

							# if blindXSS and blindPayload:
							#     paramsCopy[paramName] = blindPayload
							#     requester(url, paramsCopy, headers,
							#               GET, delay, timeout)


def logVector(chrome, payload, loggerVector, url, paramName, vector, WAF):
	popup = chrome.validate_get_attack(payload)
	if popup == "Succeeded":
		logger.red_line()
		logger.good('Payload: %s' % loggerVector)

	logStorer.addVector(popup, url, paramName, vector, payload, WAF)
